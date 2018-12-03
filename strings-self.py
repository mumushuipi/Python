

import os
import re

global_list_localizable = 0
global_dict_localizable_key = {}
global_dict_localizable_value = {}
global_dict_localizable_delete_repeat_local = {}
global_dict_localizable_delete_repeat_lineNumber_local = {}
global_dict_delete_repeat_def = {}

global_deleteCount_key_repeat_local = 0

global_deleteCount_local = 0

global_dict_def = {}
global_deleteCount_def = 0
global_repeatCount_def = 0


stringLocalFile = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'CallWatch/CallWatch/SupportingFiles/Resource/Language/zh-Hans.lproj/Localizable.strings')
stringDefFile = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'CallWatch/Pods/EKOStringDefine/EKOStringDefine/StringDef/StringDef.h')
stringDefDir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'CallWatch/Pods/EKOStringDefine/EKOStringDefine')

StringDefBaimingdan = ['EKOStringDefine'] #路径白名单，路径包含这个的，不会处理
StringBaimingdan = [] #路径白名单，路径包含这个的，不会处理
StringDefFileArray = ['EKOStringDefine'] #所有stringDef文件的所在文件夹

#获取"wechat_desc_key7" = "未开启推送通知，你错过了宝贝的视频通话" 双引号部分
def Get_Localizable_String_key_value(value):
    array = re.findall(r'".+?"',value)
    if len(array) > 0:
        return array
    return None
##define kStrClasses                 local(@"classes") 中的"classes"
def getStringDefLocalString(value):
    array = re.findall(r'".+?"',value)
    if len(array) == 1:
        return array
    return None
##define kStrClasses                 local(@"classes") 中的kStrClasses
def getStringDef_KString(value):
    array = re.findall(r'\w+',value)
# 获取一行的单词大于2个，判定是正式的宏
    if len(array) > 2:
        return array[1]
    return None

def isEmptyWithline(line):
    array = re.findall(r'.+',line)
    if array is None or len(array) == 0:
        return True
    return False
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

# 处理localizable.strings文件
def Handle_Localizable_string_OpenFile():
    #打开文件
    global global_list_localizable
    global global_dict_localizable_key
    global global_dict_localizable_value
    global global_dict_localizable_delete_repeat_local
    global global_dict_localizable_delete_repeat_lineNumber_local
    global global_dict_delete_repeat_def
    global global_deleteCount_key_repeat_local
    
    global global_deleteCount_local
    
    with open(stringLocalFile,'r',encoding='utf-8') as f:
        lineNum = 0
        global_list_localizable = f.readlines()
        for line in global_list_localizable:
            lineNum = lineNum + 1
            array = re.findall(r'.+',line)
            # 0、删除空行
            if isEmptyWithline(line):
                global_list_localizable[lineNum-1] = ""
                continue
            #获取当前行前面部分有效代码
            line = line.split('//')[0]
            result = Get_Localizable_String_key_value(line)
            #偷个懒，只筛选正常字符串内不含双引号
            if result is None or len(result) != 2:
                continue
            if result is not None:
                #1、判断key是否有重复的
                key = result[0]
                if global_dict_localizable_key.get(key) is not None:
                    global_deleteCount_key_repeat_local = global_deleteCount_key_repeat_local + 1
                    print("key重复:",key,"第",lineNum,"行和第",global_dict_localizable_key[key],"行重复，可以删除")
                    global_list_localizable[lineNum-1] = ""
                    continue
                global_dict_localizable_key[key] = lineNum
                #2、判断value是否有重复的
                value = result[1]
                if global_dict_localizable_value.get(value) is not None:
                    print("value重复:",value,"第",lineNum,"行和第",global_dict_localizable_value[value],"行重复，需要处理")
                    #2.1 不能直接变成空行，因为有的是用local("string")的方式在主工程展示，在4.1处理
#                    global_list_localizable[lineNum-1] = ""
                    #2.2 记录下已删除的重复local的key,作为key。正确的loca作为value
                    correctLineNumber = global_dict_localizable_value.get(value)
                    correctKey = list (global_dict_localizable_key.keys()) [list (global_dict_localizable_key.values()).index (correctLineNumber)]
                    global_dict_localizable_delete_repeat_local[key] = correctKey
                    global_dict_localizable_delete_repeat_lineNumber_local[key] = lineNum
                else:
                    global_dict_localizable_value[value] = lineNum

        startpath = os.path.abspath(os.path.dirname(os.getcwd()))

        #3、主工程寻找是否有使用，或者需要替换的，进行遍历编辑
        searUselessWord_LocalString_Project_OpenFile(startpath)
        if len(global_dict_localizable_key) > 0:
            for dic_key in global_dict_localizable_key:
                dic_key_lineNumber = global_dict_localizable_key[dic_key]
                global_deleteCount_local = global_deleteCount_local + 1
                print("localString无人使用，第",dic_key_lineNumber,"行可以删除：%s" % dic_key)
                global_list_localizable[dic_key_lineNumber-1] = ""
                if dic_key in global_dict_localizable_delete_repeat_local.keys():
                    global_dict_localizable_delete_repeat_local.pop(dic_key)
        #4、去宏文件删除重复的local宏，找到正确的宏，形成字典{重复宏，正确宏}
        delete_stringDef_local_repeat_file()
        #4.1 除了剩下的未处理的local，其他都变成空行
        for key in global_dict_localizable_delete_repeat_lineNumber_local.keys():
            if key in global_dict_localizable_delete_repeat_local.keys():
                print("key:%s不作处理，在主工程中是以local形式存在" % key)
            else:
                global_list_localizable[global_dict_localizable_delete_repeat_lineNumber_local[key] - 1] = ""
        #5、去主工程替换重复的local宏
        search_repeat_defString_Project_OpenFile(startpath)

        f.close()
    print("一共有",global_deleteCount_key_repeat_local,"个local_key重复，已删除")
    print("一共有",global_deleteCount_local,"个local（在主工程中未使用）已删除")
    with open(stringLocalFile,'w',encoding = 'utf-8') as f_w:
        f_w.writelines(global_list_localizable)
        f_w.close()
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
def delete_stringDef_local_repeat_file():
    if len(global_dict_localizable_delete_repeat_local) > 0:
        print(global_dict_localizable_delete_repeat_local)
        print("一共有",len(global_dict_localizable_delete_repeat_local),"个local_value重复，待处理")
        # 遍历stringDef文件夹下所有的宏文件
        for fileName in os.listdir(stringDefDir):
            filePath = os.path.join(stringDefDir,fileName)
            if os.path.isfile(filePath) and os.path.splitext(filePath)[1] in ['.h']:
                #1、开始删除重复的local宏
                handle_delete_StringDef_repeat_Local_file(filePath)
    
        # 遍历stringDef文件夹下所有的宏文件
        for fileName in os.listdir(stringDefDir):
            filePath = os.path.join(stringDefDir,fileName)
            if os.path.isfile(filePath) and os.path.splitext(filePath)[1] in ['.h']:
            #2、找到正确local对应的宏
                handle_search_StringDef_repeat_Local_file(filePath)
    
        print(global_dict_delete_repeat_def)
        print("一共有%s个宏需要替换" % len(global_dict_delete_repeat_def))
        if len(global_dict_localizable_delete_repeat_local) > 0:
            print("这里要留意下,还有部分在工程不是用宏表示%s" % global_dict_localizable_delete_repeat_local)
            print("剩下有",len(global_dict_localizable_delete_repeat_local),"个local_value重复，待处理")
    else:
        print("恭喜，localizable.string没有重复的单词")
#开始删除重复的local宏
def handle_delete_StringDef_repeat_Local_file(filePath):
    with open(filePath,'r',encoding = 'utf-8') as f:
        lineNumber = 0
        lines = f.readlines()
        for line in lines:
            lineNumber = lineNumber + 1
            line = line.split('#import')[0]
            line = line.split('//')[0]
            result = getStringDefLocalString(line)
            if result is not None and result[0] in global_dict_localizable_delete_repeat_local.keys():
                oldDefString = getStringDef_KString(line)
                #1、找到需要删除的local对应的宏，作为新dict的key
                global_dict_delete_repeat_def[oldDefString] = global_dict_localizable_delete_repeat_local[result[0]]
                #2、删除需要删除字典的key-value
                global_dict_localizable_delete_repeat_local.pop(result[0])
                #3、删除该行
                lines[lineNumber-1] = ""
        f.close()
    with open(filePath,'w',encoding = 'utf-8') as f_w:
        f_w.writelines(lines)
        f_w.close()

#找到正确local对应的宏
def handle_search_StringDef_repeat_Local_file(filePath):
    with open(filePath,'r',encoding = 'utf-8') as f:
        lineNumber = 0
        lines = f.readlines()
        for line in lines:
            lineNumber = lineNumber + 1
            line = line.split('#import')[0]
            line = line.split('//')[0]
            result = getStringDefLocalString(line)
            if result is not None and result[0] in global_dict_delete_repeat_def.values():
                newDefString = getStringDef_KString(line)
                #遍历是因为可能存在同时存在两个或以上相同的value值
                for oldKey in global_dict_delete_repeat_def:
                    if global_dict_delete_repeat_def[oldKey] == result[0]:
                        global_dict_delete_repeat_def[oldKey] = newDefString;
############################################################################################################################################
###################################    用来替换主工程重复使用local对应的宏   #####################################################################
############################################################################################################################################
def search_repeat_defString_Project_OpenFile(filePath):
    if len(global_dict_delete_repeat_def) == 0:
        print(">>>>>>>>>>>>>>>>>>>>>>>>没有需要替换重复local的宏了>>>>>>>>>>>>>>>>>>>>>>>>")
        return
    
    for dir in os.listdir(filePath):
        if xtc_is_repeat_defString_BaiMingDan(dir):
            continue
        path = os.path.join(filePath,dir)
        if os.path.isdir(path):
            search_repeat_defString_Project_OpenFile(path)
        else:
            if os.path.splitext(path)[1] in ['.m','.h']:
                handel_replace_project_file(path)

def handel_replace_project_file(filePath):
    needWrite = False
    with open(filePath,'r',encoding = 'utf-8') as f:
        fileListLines = f.readlines()
        for line in fileListLines:
            if len(isExist_Replace_StringDef_in_project_line(line)) > 0:
                needWrite = True
                break
        f.close()
    if needWrite:
        with open(filePath,'w',encoding = 'utf-8') as f_w:
            for line in fileListLines:
                array = isExist_Replace_StringDef_in_project_line(line)
                if len(array) > 0:
                    # 这里有个缺陷，就是不是单词的也会被替换掉，例如：需要替换Test为APPle，原句是BBBTestCCC,替换后为BBBAPPleCCC
                    for obj_key in array:
                        line = line.replace(obj_key,global_dict_delete_repeat_def[obj_key])
                # TODO，为什么只能单行写？？？？
                f_w.write(line)
            f_w.close()

# 是否含有需要替换的宏,可能一行存在多个需要替换的宏
def isExist_Replace_StringDef_in_project_line(line):
    array = re.findall(r'\w+',line)
    existArray = []
    for string in array:
        if string in global_dict_delete_repeat_def.keys():
            existArray.append(string)
    return existArray

def xtc_is_repeat_defString_BaiMingDan(path):
    if path in StringDefFileArray:
        return True
    return False

############################################################################################################################################
###################################    用来搜索主工程是否用到localString   #####################################################################
############################################################################################################################################
def searUselessWord_LocalString_Project_OpenFile(filePath):

    for dir in os.listdir(filePath):
        if xtc_isBaiMingDan(dir):
            continue
        path = os.path.join(filePath,dir)
        if os.path.isdir(path):
            if searUselessWord_LocalString_Project_OpenFile(path) == True:
                return True
        else:
            if os.path.splitext(path)[1] in ['.m','.h']:
                if open_localString_project_file(path) == True:
                    return True

def open_localString_project_file(filePath):
    with open(filePath,'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            if isExist_localString_in_project_line(line):
                if len(global_dict_localizable_key) == 0:
                    print("恭喜，所有本地localString都用到了,不需要往下遍历了。。。。。。。。。")
                    f.close()
                    return True
        f.close()
    return False

def isExist_localString_in_project_line(line):
    array = re.findall(r'".+?"',line)
    for string in array:
        if string in global_dict_localizable_key.keys():
            global_dict_localizable_key.pop(string)
            return True
    return False

def xtc_isBaiMingDan(path):
    if path in StringBaimingdan:
        return True
    return False
############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
def Handle_all_stringDef_openFile():
    for fileName in os.listdir(stringDefDir):
        filePath = os.path.join(stringDefDir,fileName)
        if os.path.isfile(filePath) and os.path.splitext(filePath)[1] in ['.h'] and filePath.split('/')[-1] not in ['UMEvents.h','EKOStringDefine.h','EKOStringDefineLocalMacros.h']:
            print("宏文件名：%s" % filePath)
            Handle_StringDef_OpenFile(filePath)

# 找寻无用的宏并删除
def Handle_StringDef_OpenFile(filePath):
    global global_deleteCount_def
    global global_repeatCount_def
    global global_dict_def
    
    global_deleteCount_def = 0
    global_repeatCount_def = 0
    global_dict_def = {}
    
    with open(filePath,'r',encoding='utf-8') as f:
        stringDefLineNum = 0
        global_list_def = f.readlines()
        for line in global_list_def:
            stringDefLineNum = stringDefLineNum + 1
            # 0、删除空行
            if isEmptyWithline(line):
#                global_list_def[stringDefLineNum-1] = ""
                continue
            #获取当前行前面部分有效代码
            line = line.split('#import')[0]
            line = line.split('//')[0]
            # 1、获取宏文件，和localString结合起来看，在localString有无使用key，无用key基本断定该宏可以删除
            result = getStringDefLocalString(line)
            if result is not None:
                if searUselessWordOpen_LocalString_File(result[0]) == False:
                    global_deleteCount_def = global_deleteCount_def + 1
                    print("第%s行宏不存在本地化文案，可以删除，local：%s" % (stringDefLineNum,result[0]))
                    global_list_def[stringDefLineNum-1] = ""
                    continue
            # 2、获取宏文件，看有无在主工程中使用，如果没有使用，也可以删除该宏
            kstring = getStringDef_KString(line)
            if kstring is not None:
                # 去掉重复宏定义，这里严谨一点应该还要判断loacl里面的字段一样
                if global_dict_def.get(kstring) is not None:
                    global_repeatCount_def = global_repeatCount_def + 1
                    print("第%s行的宏与第%s行宏命名重复:%s 可以删除" % (stringDefLineNum,global_dict_def[kstring],kstring))
                    global_list_def[stringDefLineNum-1] = ""
                else:
                    global_dict_def[kstring] = stringDefLineNum
    #3、开始去主工程中找没有用到的宏
        startpath = os.path.abspath(os.path.dirname(os.getcwd()))
        if searUselessWord_StringDef_Project_OpenFile(startpath) == False:
            if len(global_dict_def) > 0:
                for key in global_dict_def:
                    global_deleteCount_def = global_deleteCount_def + 1
                    print("宏无人使用，可以删除：%s" % key)
                    global_list_def[global_dict_def[key] - 1] = ""
        f.close()
    print("一共有",global_repeatCount_def,"个宏（重命名）可以删除")
    print("一共有",global_deleteCount_def,"个宏（在主工程中未使用）可以删除")
    with open(filePath,'w',encoding = 'utf-8') as f_w:
        f_w.writelines(global_list_def)
        f_w.close()



# 根据在宏文件找出来的本地化key去本地文件匹配是否存在，不存在说明该宏无用
def searUselessWordOpen_LocalString_File(key):
    with open(stringLocalFile,'r',encoding='utf-8') as f:
        currentLineNum = 0
        existWord = False
        for line in f.readlines():
            currentLineNum = currentLineNum + 1
            #获取当前行前面部分有效代码
            line = line.split('//')[0]
            result = Get_Localizable_String_key_value(line)
            if result is not None:
                if result[0] == key:
                    existWord = True
                    break
        return existWord
############################################################################################################################################
######################################  用来搜索主工程是否用到宏文件的宏     #####################################################################
############################################################################################################################################
def searUselessWord_StringDef_Project_OpenFile(filePath):
    
    for dir in os.listdir(filePath):
        if xtc_isStringDefBaiMingDan(dir):
            continue
        path = os.path.join(filePath,dir)
        if os.path.isdir(path):
            if searUselessWord_StringDef_Project_OpenFile(path) == True:
                return True
        else:
# os.path.splitext()将文件名和扩展名分开
            if os.path.splitext(path)[1] in ['.m','.h']:
                if open_project_file(path) == True:
                    return True
    return False


def open_project_file(filePath):
    with open(filePath,'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            isExist_StringDef_in_project_kString(line)
            if len(global_dict_def) == 0:
                print("恭喜，所有宏都用到了，不需要往下遍历了。。。。。。。。。")
                f.close()
                return True
        f.close()
    return False

def isExist_StringDef_in_project_kString(line):
    array = re.findall(r'\w+',line)
    for string in array:
        if string in global_dict_def.keys():
            global_dict_def.pop(string)


def xtc_isStringDefBaiMingDan(path):
    if path in StringDefBaimingdan:
        return True
    return False

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

if __name__ == '__main__':

#    currentWorkPath = os.getcwd()
#    print("当前工作目录 : %s" %  currentWorkPath)

#    if os.path.isdir(string2Path):
#        print("当前路径是文件夹 %s " % string2Path)
#    else:
#        print("当前路径是文件 %s" % string2Path)

#第一步：处理宏文件，删除无用的、重复的宏（key重复、kStrTitle）
# 0、删除空行
# 1、获取宏文件，和localString结合起来看，在localString有无使用key，无用key基本断定该宏可以删除
# 2、获取宏文件，判断有无重复的宏，重复的删除，只保留第一次出现的宏
# 3、获取宏文件，看有无在主工程中使用，如果没有使用，也可以删除该宏
    Handle_all_stringDef_openFile()

#第二步：处理本地化文件localizable.strings,删除无用的、重复的（key重复、value重复）
# 0、删除空行

    Handle_Localizable_string_OpenFile()

    print("完美结束")


