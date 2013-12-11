import win32api
import sys

def RegisterOnExit(callBackOnExit):
    win32api.SetConsoleCtrlHandler(callBackOnExit, True)

def UnRegisterOnExit(callBackOnExit):
    win32api.SetConsoleCtrlHandler(callBackOnExit, False)
