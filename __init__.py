import os

import struct
import os, time, re
import xlsxwriter as wx

def fileFunction(path,suffix,newpath,newsuffix):
    """
    一个文件夹下面有多个文件，将这些文件放到一个文件夹下面
    :param path: 需要查询的文件夹
    :param suffix: 需要查询文件夹下面文件的后缀
    :param newpath: 新文件的路径
    :param newsuffix: 新文件的后缀
    :return:

    eg:fileFunction("D:/test",".csv","D:/test",".csv")
    """
    "把相关目录的文件夹中后缀都遍历一遍"
    result = []
    for dp, dn, fs in os.walk(path):
        for f in fs:
            if (os.path.splitext(f)[1] == suffix):
                result.append(os.path.join(dp, f))

    count = 0
    for fname in result:
        count += 1
        print(fname)
        if os.path.exists(newpath + "/newPic"):
            print("enter1")
            pass
        else:
            print("enter 2")
            os.mkdir(newpath + "/newPic")
        newNamePath = newpath + "/newPic/"
        newFileName = str("000000" + str(count) + newsuffix)[-10:]
        os.rename(fname, newNamePath + newFileName)

def getCurrentPath():
    "获取当前文件夹路径"
    currentpath = os.getcwd()
    return currentpath

def getDirList(path):
    """
    获取某指定路径下所有子目录的列表
    :param path: 需要查询的文件路径
    :return:
    """
    if path =="":
        return []
    path = path.replace("/","\\")
    if path[-1]!= "\\":
        path = path +"\\"
    a = os.listdir(path)
    b= [x for x in a if os.path.isdir(path+x)]
    return b

def getFileList(path):
    """
    获取某指定目录下所有文件列表
    :param path:
    :return:
    """
    if path == "":
        return []
    path = path.replace("/","\\")
    if path[-1]!= "\\":
        path = path +"\\"
    a = os.listdir(path)
    b = [x for x in a if os.path.isfile(path+x)]
    return b

# 找出文件夹下所有xml后缀的文件
def listfiles(rootdir, prefix='.xml'):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    file.append(rootdir + '/' + filename)
            return file
        else:
            pass

#将数据写入到Excel
def writeexcel(path,dealcontent=[]):
    workbook = wx.Workbook(path)
    top = workbook.add_format(
        {'border': 1, 'align': 'center', 'bg_color': 'white', 'font_size': 11, 'font_name': '微软雅黑'})
    red = workbook.add_format(
        {'font_color': 'white', 'border': 1, 'align': 'center', 'bg_color': '800000', 'font_size': 11,
         'font_name': '微软雅黑', 'bold': True})
    image = workbook.add_format(
        {'border': 1, 'align': 'center', 'bg_color': 'white', 'font_size': 11, 'font_name': '微软雅黑'})
    formatt = top
    formatt.set_align('vcenter')  # 设置单元格垂直对齐
    worksheet = workbook.add_worksheet()  # 创建一个工作表对象
    width = len(dealcontent[0])
    worksheet.set_column(0, width, 38.5)  # 设定列的宽度为22像素
    for i in range(0, len(dealcontent)):
        if i == 0:
            formatt = red
        else:
            formatt = top
        for j in range(0, len(dealcontent[i])):
            if dealcontent[i][j]:
                worksheet.write(i, j, dealcontent[i][j].replace(' ', ''), formatt)
            else:
                worksheet.write(i, j, '', formatt)
    workbook.close()


# 文件格式 文件头(十六进制)
# JPEG (jpg) FFD8FF
# PNG (png) 89504E47
# GIF (gif) 47494638
# TIFF (tif) 49492A00
# Windows Bitmap (bmp) 424D
# CAD (dwg) 41433130
# Adobe Photoshop (psd) 38425053
# Rich Text Format (rtf) 7B5C727466
# XML (xml) 3C3F786D6C
# HTML (html) 68746D6C3E
# Email [thorough only] (eml) 44656C69766572792D646174653A
# Outlook Express (dbx) CFAD12FEC5FD746F
# Outlook (pst) 2142444E
# MS Word/Excel (xls.or.doc) D0CF11E0
# MS Access (mdb) 5374616E64617264204A

# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少则2字符，长则8字符
def typeList():
    return {
        "FFD8FF": "jpeg",
        "89504E47": "png",
        "47494638": "gif",
        "D0CF11E0": "doc"}


# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取文件类型，传入文件名
def filetype(filename):
    binfile = open(filename, 'br')  # 必需二制字读取
    tl = typeList()
    ftype = 'error'
    for hcode in tl.keys():
        numOfBytes = len(hcode) // 2  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype




fileFunction("D:/test",".csv","D:/test",".csv")
print(getDirList("D:/test"))
print(getFileList("D:"))


