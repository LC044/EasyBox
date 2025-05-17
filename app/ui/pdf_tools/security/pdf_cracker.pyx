# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import cython
from cython.parallel import prange, parallel
import numpy as np
import fitz
import os
import time
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strlen

# 定义字符集常量
DIGITS = "0123456789"
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHANUMERIC = DIGITS + LOWERCASE + UPPERCASE
ALL_CHARS = ALPHANUMERIC + "!@#$%^&*()_+-=[]{}|;:,.<>?/"

# 定义结果结构体
ctypedef struct CrackResult:
    bint success
    char password[100]  # 假设密码最长不超过100个字符


def get_charset(charset_type):
    """根据字符集类型返回对应的字符集"""
    if charset_type == "digits":
        return DIGITS
    elif charset_type == "lowercase":
        return LOWERCASE
    elif charset_type == "uppercase":
        return UPPERCASE
    elif charset_type == "alphanumeric":
        return ALPHANUMERIC
    else:  # "all"
        return ALL_CHARS


@cython.boundscheck(False)
@cython.wraparound(False)
def generate_passwords(int length, str charset):
    """生成指定长度和字符集的所有可能密码"""
    cdef int charset_len = len(charset)
    cdef int i, j
    cdef list passwords = []
    cdef list current = [charset[0]] * length
    cdef list indices = [0] * length
    
    # 初始密码
    passwords.append(''.join(current))
    
    # 生成所有可能的密码
    while True:
        # 从最后一位开始，找到可以增加的位置
        for i in range(length-1, -1, -1):
            indices[i] += 1
            if indices[i] < charset_len:
                current[i] = charset[indices[i]]
                # 重置后面的位置
                for j in range(i+1, length):
                    indices[j] = 0
                    current[j] = charset[0]
                break
        else:
            # 如果没有找到可以增加的位置，说明已经生成了所有密码
            break
            
        passwords.append(''.join(current))
    
    return passwords


@cython.boundscheck(False)
@cython.wraparound(False)
def batch_generate_passwords(int start_idx, int batch_size, int length, str charset):
    """生成指定范围内的密码批次"""
    cdef int charset_len = len(charset)
    cdef int total = charset_len ** length
    cdef int end_idx = min(start_idx + batch_size, total)
    cdef int i, j, idx
    cdef list passwords = []
    cdef list current = [0] * length
    
    # 将起始索引转换为密码
    idx = start_idx
    for i in range(length-1, -1, -1):
        current[i] = idx % charset_len
        idx //= charset_len
    
    # 生成指定范围内的密码
    for idx in range(start_idx, end_idx):
        # 将当前索引转换为密码
        pwd = ''
        for i in range(length):
            pwd += charset[current[i]]
        passwords.append(pwd)
        
        # 更新到下一个密码
        for i in range(length-1, -1, -1):
            current[i] += 1
            if current[i] < charset_len:
                break
            current[i] = 0
    
    return passwords


@cython.boundscheck(False)
@cython.wraparound(False)
def check_password_batch(list passwords, str pdf_path):
    """检查一批密码是否能解密PDF"""
    cdef int i
    cdef int n = len(passwords)
    cdef str password
    cdef bint success = False
    cdef str found_password = ""
    
    for i in range(n):
        password = passwords[i]
        try:
            with fitz.open(pdf_path) as pdf:
                if pdf.authenticate(password):
                    success = True
                    found_password = password
                    break
        except Exception:
            continue
    
    return success, found_password


def crack_pdf_password(str pdf_path, int min_length=4, int max_length=8, 
                      str charset_type="digits", int num_threads=4, 
                      int batch_size=1000, callback=None):
    """使用Cython优化的暴力破解PDF密码"""
    cdef str charset = get_charset(charset_type)
    cdef int length, charset_len, total_combinations, batches, i
    cdef bint success = False
    cdef str found_password = ""
    
    # 检查PDF是否加密
    try:
        with fitz.open(pdf_path) as pdf:
            if not pdf.is_encrypted:
                return False, "PDF文件未加密，无需解密"
    except Exception as e:
        return False, f"无法打开PDF文件: {str(e)}"
    
    # 尝试一些常见密码
    common_passwords = ['', '1234', '0000', '1111', '9999', '123456', 'password', 'admin', 'qwerty']
    for pwd in common_passwords:
        if callback:
            callback(f"尝试常见密码: {pwd}")
        try:
            with fitz.open(pdf_path) as pdf:
                if pdf.authenticate(pwd):
                    return True, pwd
        except Exception:
            continue
    
    # 按照密码长度逐一尝试
    charset_len = len(charset)
    for length in range(min_length, max_length + 1):
        total_combinations = charset_len ** length
        if callback:
            callback(f"尝试长度为 {length} 的密码，组合总数: {total_combinations}")
        
        # 计算批次数
        batches = (total_combinations + batch_size - 1) // batch_size
        
        # 分批处理密码
        for i in range(batches):
            if callback and i % 10 == 0:
                progress = (i / batches) * 100
                callback(f"暴力破解(长度{length}): 进度 {progress:.2f}%")
            
            # 生成当前批次的密码
            start_idx = i * batch_size
            passwords = batch_generate_passwords(start_idx, batch_size, length, charset)
            
            # 检查密码批次
            success, found_password = check_password_batch(passwords, pdf_path)
            if success:
                return True, found_password
    
    return False, "所有可能的密码组合尝试均失败"


# 并行版本的密码检查（使用OpenMP）
@cython.boundscheck(False)
@cython.wraparound(False)
def parallel_check_password_batch(list passwords, str pdf_path, int num_threads=4):
    """并行检查一批密码是否能解密PDF"""
    cdef int i, n = len(passwords)
    cdef CrackResult result
    result.success = False
    strcpy(result.password, "")
    
    # 使用OpenMP并行处理
    with nogil, parallel(num_threads=num_threads):
        for i in prange(n):
            # 这里需要GIL，因为fitz库不是线程安全的
            with gil:
                if not result.success:  # 如果还没找到密码
                    try:
                        with fitz.open(pdf_path) as pdf:
                            if pdf.authenticate(passwords[i]):
                                result.success = True
                                strcpy(result.password, passwords[i].encode('utf-8'))
                    except Exception:
                        pass
    
    return result.success, result.password.decode('utf-8') if result.success else ""


# 优化的字典破解函数
def dictionary_crack(str pdf_path, str dict_path, int num_threads=4, callback=None):
    """使用Cython优化的字典破解PDF密码"""
    cdef bint success = False
    cdef str found_password = ""
    cdef list passwords = []
    cdef int batch_size = 1000
    cdef int total_passwords, batches, i, j
    
    # 检查字典文件是否存在
    if not os.path.exists(dict_path):
        return False, "字典文件不存在"
    
    # 读取字典文件
    try:
        with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return False, f"无法读取字典文件: {str(e)}"
    
    if not passwords:
        return False, "字典文件为空或格式不正确"
    
    total_passwords = len(passwords)
    if callback:
        callback(f"字典中共有 {total_passwords} 个密码")
    
    # 计算批次数
    batches = (total_passwords + batch_size - 1) // batch_size
    
    # 分批处理密码
    for i in range(batches):
        if callback and i % 10 == 0:
            progress = (i / batches) * 100
            callback(f"字典破解: 进度 {progress:.2f}%")
        
        # 获取当前批次的密码
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, total_passwords)
        batch_passwords = passwords[start_idx:end_idx]
        
        # 并行检查密码批次
        success, found_password = parallel_check_password_batch(batch_passwords, pdf_path, num_threads)
        if success:
            return True, found_password
    
    return False, "字典中所有密码尝试均失败"