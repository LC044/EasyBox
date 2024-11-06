import sys,os
import traceback
from app.config import version


class ExceptionHanding:
    def __init__(self, exc_type, exc_value, traceback_):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.traceback = traceback_
        self.error_message = ''.join(traceback.format_exception(exc_type, exc_value, traceback_))

    def parser_exc(self):
        return (f'{self.error_message}\n未知错误类型，可参考 https://memotrace.cn/doc/posts/error/faq.html '
                    f'解决该问题\n温馨提示：重启电脑可解决80%的问题')

    def __str__(self):
        errmsg = f'version:{version}\n{self.parser_exc()}'
        return errmsg


def excepthook(exc_type, exc_value, traceback_):
    # 将异常信息转为字符串

    # 在这里处理全局异常

    error_message = ExceptionHanding(exc_type, exc_value, traceback_)
    txt = '您可添加QQ群发送log文件以便解决该问题'
    msg = f"Exception Type: {exc_type.__name__}\nException Value: {exc_value}\ndetails: {error_message}\n\n{txt}"
    print(msg)

    # 调用原始的 excepthook，以便程序正常退出
    sys.__excepthook__(exc_type, exc_value, traceback_)
