# !usr/bin/env python
# coding=utf-8

import ctypes
from ctypes import wintypes
import os

'''
This package helps us to login ProjectWise and use API functions by PYTHON.
It did not wrap any api functions. You need to check up the functions from api document of ProjectWise.
'''


class PW(object):
    """
    :param ds: data source of PW
    :param user: user account
    :param pwd: user password
    :param pwbin: path to pw bin folder. Ignore it if install by default.
    """

    def __init__(self, ds, user, pwd, pwbin=r'C:\Program Files\Bentley\ProjectWise\bin', schema=''):
        self.ds = ds
        self.user = user
        self.pwd = pwd
        self.schema = schema

        dllpath = os.path.join(pwbin, 'dmscli.dll')
        if os.path.exists(dllpath):
            os.environ['path'] += ';'+pwbin
        else:
            raise Exception('Can not find pw bin path.')

        self.cli = ctypes.WinDLL("dmscli.dll")

    def __enter__(self):
        self.login()
        return self

    def test(self):
        res = self.cli.aaApi_SelectTopLevelProjects()
        if res in [0, 1]:
            print('error')
        else:
            print('%s projects at your root dir' % res)

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()

    def login(self):
        self.cli.aaApi_GetProjectStringProperty.restype = ctypes.c_uint64
        self.cli.aaApi_GetDocumentStringProperty.restype = ctypes.c_uint64
        self.cli.aaApi_GetWorkflowStringProperty.restype = ctypes.c_uint64
        self.cli.aaApi_GetStateStringProperty.restype = ctypes.c_uint64

        self.cli.aaApi_Initialize(1)
        self.cli.aaApi_Login.argtypes = [
            wintypes.LONG, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR]

        # login pw
        res = self.cli.aaApi_Login(
            0, self.ds, self.user, self.pwd, self.schema)
        if not res:
            raise Exception('Login failed')
        # if not res:
        #     err_id=self.cli.aaApi_GetLastErrorId()
        #     if err_id:
        #         h_msg=self.cli.aaApi_GetMessageByErrorId(err_id)
        #         msg=ctypes.wstring_at(h_msg)
        #         raise(msg)
        #     else:
        #         raise('login failed')

    def logout(self):
        # logout pw
        self.cli.aaApi_Logout(self.ds)
        self.cli.aaApi_Uninitialize()
        print('Logged out')


if __name__ == '__main__':
    # 使用示例
    import getpass
    
    ds = input('请输入数据源(xxx.xxx.xxx.xxx:abc):')
    user = input('请输入用户名:')
    pwd = getpass.getpass('请输入密码:')

    with PW(ds, user, pwd) as pw:
        pw.test()
