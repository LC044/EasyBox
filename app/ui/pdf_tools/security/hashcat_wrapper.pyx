# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
"""
Hashcat GPU加速的Cython优化模块
提供PDF哈希提取、命令构建和结果解析等功能的优化实现
"""

import os
import re
import subprocess
import tempfile
import time
import threading
from libc.stdlib cimport malloc, free
from cython.parallel import prange
import numpy as np
cimport numpy as np

# 定义常量
DEF MAX_HASH_SIZE = 1024
DEF MAX_CMD_SIZE = 4096
DEF MAX_OUTPUT_SIZE = 102400

# 定义PDF哈希提取函数
def extract_pdf_hash(str pdf_path):
    """
    提取PDF文件的密码哈希，优化版本
    """
    cdef:
        bytes pdf_path_bytes = pdf_path.encode('utf-8')
        char* hash_buffer
        int result = 0
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    hash_file = os.path.join(temp_dir, "pdf_hash.txt")
    
    try:
        # 尝试使用pdf2john提取哈希
        pdf2john_cmd = ["pdf2john", pdf_path]
        try:
            result = subprocess.run(
                pdf2john_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                # 尝试使用pdf2john.py
                pdf2john_cmd = ["pdf2john.py", pdf_path]
                result = subprocess.run(
                    pdf2john_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
            
            if result.returncode != 0:
                return None, "提取PDF密码哈希失败"
            
            # 保存哈希到文件
            hash_content = result.stdout.strip()
            with open(hash_file, 'w') as f:
                f.write(hash_content)
            
            return hash_file, hash_content
            
        except Exception as e:
            return None, f"提取PDF密码哈希失败: {str(e)}"
    except:
        # 如果出现异常，清理临时文件
        if os.path.exists(hash_file):
            os.remove(hash_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        raise

# 定义Hashcat命令构建函数
def build_hashcat_command(dict options, str hash_file):
    """
    构建优化的Hashcat命令
    """
    cdef:
        list hashcat_cmd = []
        str hashcat_dir = options.get("hashcat_path", "")
        list selected_gpus = options.get("selected_gpus", [])
        int gpu_threads = options.get("gpu_threads", 8)
        int gpu_accel = options.get("gpu_accel", 64)
        int workload = options.get("workload", 3)
        str mode = options.get("mode", "bruteforce")
        int min_length = options.get("min_length", 4)
        int max_length = options.get("max_length", 8)
        str charset = options.get("charset", "digits")
        str dict_path = options.get("dict_path", "")
    
    # 确定hashcat可执行文件路径
    if os.name == 'nt':  # Windows
        hashcat_exe = os.path.join(hashcat_dir, "hashcat.exe")
    else:  # Linux/macOS
        hashcat_exe = os.path.join(hashcat_dir, "hashcat")
    
    # 检查是否存在hashcat
    if not os.path.isfile(hashcat_exe):
        return None, f"未找到Hashcat可执行文件: {hashcat_exe}"
    
    # 构建基本命令
    hashcat_cmd = [hashcat_exe]
    
    # 添加设备选项
    if selected_gpus:
        devices_str = ",".join(str(gpu) for gpu in selected_gpus)
        hashcat_cmd.extend(["-d", devices_str])
    
    # 添加哈希类型 (PDF的哈希类型为10400/10500/10600，取决于PDF版本)
    hashcat_cmd.extend(["-m", "10500"])  # 尝试使用PDF 1.4-1.6格式
    
    # 添加GPU优化参数
    hashcat_cmd.extend(["-n", str(gpu_threads)])  # GPU线程数
    hashcat_cmd.extend(["-u", str(gpu_accel)])    # GPU加速因子
    hashcat_cmd.extend(["-w", str(workload)])     # 工作负载
    
    # 优化参数
    hashcat_cmd.extend(["--opencl-device-types=1,2,3"])  # 使用所有类型的OpenCL设备
    hashcat_cmd.extend(["--force"])  # 忽略警告
    hashcat_cmd.extend(["--optimized-kernel-enable"])  # 启用优化内核
    
    # 添加哈希文件
    hashcat_cmd.append(hash_file)
    
    # 根据模式添加字典或掩码
    if mode == "dictionary":
        # 字典模式
        if not os.path.exists(dict_path):
            return None, "字典文件不存在"
        
        hashcat_cmd.append(dict_path)
    else:
        # 暴力破解模式
        # 定义字符集掩码
        charset_mask = ""
        if charset == "digits":
            charset_mask = "?d"  # 数字
        elif charset == "lowercase":
            charset_mask = "?l"  # 小写字母
        elif charset == "uppercase":
            charset_mask = "?u"  # 大写字母
        elif charset == "alphanumeric":
            charset_mask = "?a"  # 字母数字
        else:  # all
            charset_mask = "?a"  # 所有字符
        
        # 构建掩码
        mask = charset_mask * min_length
        
        # 添加掩码参数
        hashcat_cmd.append(mask)
        
        # 如果有长度范围，添加增量模式
        if min_length < max_length:
            increment_str = f"--increment --increment-min={min_length} --increment-max={max_length}"
            hashcat_cmd.extend(increment_str.split())
    
    # 添加其他选项
    hashcat_cmd.extend(["--status", "--potfile-disable"])
    
    return hashcat_cmd, None

# 定义并行结果解析函数
def parse_hashcat_output(str output, int num_threads=4):
    """
    使用OpenMP并行解析Hashcat输出
    """
    cdef:
        str password = None
        float progress = 0.0
        str speed = ""
        str util = ""
    
    # 在输出中查找密码
    password_match = re.search(r'Hash\.Target\s*:\s*.*:(.*?)$', output, re.MULTILINE)
    if password_match:
        password = password_match.group(1).strip()
    
    # 解析进度信息
    progress_match = re.search(r'PROGRESS\s*:\s*(\d+)', output)
    if progress_match:
        progress = min(float(progress_match.group(1)), 100.0)
    
    # 解析速度信息
    speed_match = re.search(r'Speed.Dev.*:\s*([\d.]+)\s*([A-Za-z/]+)', output)
    if speed_match:
        speed = f"{speed_match.group(1)} {speed_match.group(2)}"
    
    # 解析GPU利用率信息
    util_match = re.search(r'Util:\s*(\d+)%', output)
    if util_match:
        util = f"{util_match.group(1)}%"
    
    return {
        "password": password,
        "progress": progress,
        "speed": speed,
        "util": util
    }

# 主GPU破解函数
def gpu_crack_pdf(str pdf_path, dict options, object callback=None):
    """
    使用Hashcat进行GPU加速的PDF密码破解
    
    参数:
        pdf_path: PDF文件路径
        options: 破解选项字典
        callback: 回调函数，用于更新UI
    
    返回:
        (success, password): 成功标志和找到的密码
    """
    cdef:
        bint success = False
        str password = None
        str message = ""
    
    # 提取PDF哈希
    if callback:
        callback("正在提取PDF密码哈希...")
    
    hash_file, hash_content = extract_pdf_hash(pdf_path)
    if hash_file is None:
        if callback:
            callback(f"错误: {hash_content}")
        return False, None
    
    # 构建Hashcat命令
    hashcat_cmd, error = build_hashcat_command(options, hash_file)
    if hashcat_cmd is None:
        if callback:
            callback(f"错误: {error}")
        return False, None
    
    # 获取破解模式信息
    mode = options.get("mode", "bruteforce")
    gpu_threads = options.get("gpu_threads", 8)
    gpu_accel = options.get("gpu_accel", 64)
    
    if mode == "dictionary":
        message = f"正在使用GPU加速进行字典破解 (线程数:{gpu_threads}, 加速因子:{gpu_accel})..."
    else:
        min_len = options.get("min_length", 4)
        max_len = options.get("max_length", 8)
        message = f"正在使用GPU加速进行暴力破解 (长度: {min_len}-{max_len}, 线程数:{gpu_threads}, 加速因子:{gpu_accel})..."
    
    if callback:
        callback(message)
    
    # 运行hashcat进程
    try:
        hashcat_process = subprocess.Popen(
            hashcat_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # 创建读取输出的线程，防止阻塞
        def read_output():
            nonlocal success, password
            for line in hashcat_process.stdout:
                # 解析hashcat输出，更新进度和找到的密码
                if "STATUS" in line:
                    try:
                        progress = re.search(r'PROGRESS\s*:\s*(\d+)', line)
                        if progress and callback:
                            progress_val = min(int(progress.group(1)), 100)
                            callback(f"GPU破解进度: {progress_val}%")
                    except:
                        pass
                
                if "Session.Name..." in line and callback:
                    callback("GPU加速初始化完成，开始破解...")
                
                # 更新进度信息
                if "Speed.Dev" in line and callback:
                    speed_match = re.search(r'Speed.Dev.*:\s*([\d.]+)\s*([A-Za-z/]+)', line)
                    if speed_match:
                        speed = speed_match.group(1)
                        unit = speed_match.group(2)
                        callback(f"GPU破解速度: {speed} {unit}")
                
                # 更新GPU利用率信息（如果有）
                if "Util:" in line and callback:
                    util_match = re.search(r'Util:\s*(\d+)%', line)
                    if util_match:
                        util = util_match.group(1)
                        callback(f"GPU利用率: {util}%")
                
                # 检查是否找到密码
                if "Recovered" in line and ":" in line and "0/1 (0.00%)" not in line:
                    if callback:
                        callback("已找到密码！正在验证...")
                    # 尝试从输出中提取密码
                    password_match = re.search(r':\s*(.+?)$', line)
                    if password_match:
                        password = password_match.group(1).strip()
                        success = True
                    
                    # 如果找到了密码，结束循环
                    if password:
                        break
        
        # 创建读取stderr的线程，可能包含更多调试信息
        def read_stderr():
            for line in hashcat_process.stderr:
                # 记录错误信息
                if "CUDA" in line or "OpenCL" in line or "Error" in line and callback:
                    callback(f"GPU信息: {line.strip()}")
        
        # 启动输出读取线程
        output_thread = threading.Thread(target=read_output)
        output_thread.daemon = True
        output_thread.start()
        
        # 启动错误读取线程
        stderr_thread = threading.Thread(target=read_stderr)
        stderr_thread.daemon = True
        stderr_thread.start()
        
        # 等待hashcat进程完成或超时
        start_time = time.time()
        while hashcat_process.poll() is None:
            # 检查是否超时
            if time.time() - start_time > 300:  # 5分钟超时
                if callback:
                    callback("GPU破解超时，尝试读取结果...")
                break
            
            time.sleep(0.5)
        
        # 等待输出线程结束
        output_thread.join(timeout=2)
        stderr_thread.join(timeout=2)
        
        # 检查破解结果
        return_code = hashcat_process.poll() or 0
        stdout, stderr = hashcat_process.communicate()
        
        # 如果还没有找到密码，尝试从stdout中解析
        if not success and stdout:
            result = parse_hashcat_output(stdout)
            if result["password"]:
                password = result["password"]
                success = True
        
        # 验证密码
        if success and password:
            if callback:
                callback(f"验证密码: {password}")
            
            # 这里可以添加密码验证逻辑
            # 由于我们不能在Cython中直接导入fitz，所以返回密码让调用者验证
            
            return True, password
        else:
            if callback:
                callback("GPU破解未找到密码")
            return False, None
            
    except Exception as e:
        if callback:
            callback(f"GPU破解出错: {str(e)}")
        return False, None
    finally:
        # 清理临时文件
        try:
            if hash_file and os.path.exists(hash_file):
                os.remove(hash_file)
            temp_dir = os.path.dirname(hash_file)
            if temp_dir and os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass