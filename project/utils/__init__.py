import os

import re

from project import settings


def mvImage(filePath, dstDir):
    '''
    将filePath位置的文件，移动到dstDir目录下
    :param filePath:
    :param dstDir:
    :return:
    '''
    # 读取到文件名
    tmpDir, fileName = os.path.split(filePath)

    with open(filePath, 'rb') as rf:
        with open(os.path.join(dstDir, fileName), 'wb') as wf:
            wf.write(rf.read())

    # 清空临时目录
    for tmpFileName in os.listdir(tmpDir):
        os.remove(os.path.join(tmpDir, tmpFileName))

    return fileName


# 针对ajax上传文件，且被用户注册使用后，将图片文件移动到/static/users/目录
# 同时将上传图片存储的目录的临时清空
def mvImageFromTmp(filePath):
    dstDir = os.path.join(settings.BASE_DIR, 'static/users')

    srcPath = os.path.join(settings.BASE_DIR, filePath[1:])

    return os.path.join('/static/users/', mvImage(srcPath, dstDir))

def check_sql_inject(str):
    '''
    验证字符串是否包含特殊字符，如 =,'
    :param str:
    :return:  返回True,则表示安全，False存在SQL注入的非法字符
    '''
    return not re.findall(r'([=\']+)', str)