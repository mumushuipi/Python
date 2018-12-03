#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#注意：需要将翻译汇总表和当前python放在一个路径下
#1.0 目前支持的功能，从翻译汇总表读取工程的中文已经翻译了的文案，并替换

import math
import os
import re
import sys
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font,colors,Alignment

global_dict_chinese = {}

def read_to_excel_file():
    global global_dict_chinese
    handle_excel_file()

def handle_excel_file():
    xlsx = openpyxl.load_workbook('英文翻译汇总20181121.xlsx')
    #获取所有sheet的名称
    sheetNameArray = xlsx.sheetnames
    if len(sheetNameArray) == 0:
        print("当前的excel无sheet")
        return None
    #获取第一个sheet的名称
    firstSheetName = sheetNameArray[0]
    #根据sheet名获取sheet
    firstSheet = xlsx[firstSheetName]
    row_count = 0
    for row in firstSheet.rows:
        row_count = row_count + 1
        if row_count == 1:
            continue
        if row_count % 2 == 0:
            key = row[1].value
        else:
            value = row[1].value
            global_dict_chinese[key] = value

def search_all_strings_file(filePath,encodeingType = 'utf-8'):
    for dir in os.listdir(filePath):
        path = os.path.join(filePath,dir)
        if os.path.isdir(path):
            #因为bundle里面的文件用【utf-8】读取会越界，所以需要更改读取方式为【utf-16LE】
            if (os.path.splitext(path)[1] in ['.bundle','.framework']):
                if path.split('/')[-1] in ['emojiBase.bundle']:
                    return
#                print('手动确认下，这个bundle文件下的是不是需要整理：' + path)
                search_all_strings_file(path,'utf-16LE')
            else:
                search_all_strings_file(path,encodeingType)
        else:
            #1、获取英文的string文件路径
            if os.path.splitext(path)[1] in ['.strings']:
                abspath = os.path.abspath(path)
                if abspath.split('/')[-2] == 'en.lproj': #and  abspath.split('/')[-1] != 'Root.strings':
                    print(path)
                    #2、获取文件内部的中文字符串
                    open_localString_project_file(path,encodeingType)

def open_localString_project_file(filePath,encodeingType = 'utf-8'):
    lineNumber = 0
    translate_none_count = 0
    translate_none_new_count = 0
    with open(filePath,'r',encoding = encodeingType) as f:
        lines = f.readlines()
        f.close()
    
    with open(filePath,'w',encoding = encodeingType) as f_w:
        for line in lines:
            lineNumber = lineNumber + 1
            string = string_localString_in_project_line(line)
            if string is not None:
                if string in global_dict_chinese.keys():
                    value = global_dict_chinese[string]
                    if value is not None:
                        line = line.replace(string,global_dict_chinese[string])
                    else:
                        translate_none_count = translate_none_count + 1
                        print('该字符串没有找到对应的翻译：第%s行:%s' % (lineNumber,string))
                else:
                    translate_none_count = translate_none_count + 1
                    translate_none_new_count = translate_none_new_count + 1
                    print('该字符串在库中无法找到，是新加的字符串？？？第%s行:%s' % (lineNumber,string))
            f_w.write(line)
        f_w.close()
    print('一共有%s个没有翻译的文案,其中有%s个是新增的单词' % (translate_none_count,translate_none_new_count))

def string_localString_in_project_line(line):
    array = re.findall(r'"(.+?)"',line)
    if len(array) == 1 or len(array) == 2:
        string = array[-1]
        if re.search(r'[\u4e00-\u9fa5]',string) is not None:
            return string
        return None
    elif len(array) > 2:
        #1、先取出带双引号部分，非贪婪模式
        array = re.findall(r'".+?"',line)
        firstString = array[0]
        #2、去掉第一个带双引号部分
        line = line.replace(firstString,"")
        #3、以贪婪模式，获取双引号内部的内容
        array = re.findall(r'"(.+)"',line)
        string = array[0]
        if re.search(r'[\u4e00-\u9fa5]',string) is not None:
            return string
        return None

if __name__ == '__main__':

#1、读取excel文案
    read_to_excel_file()

#2、搜索工程中的所有中文.string文件,找到对应的中文字符串，并替换成翻译文案
    startpath = os.path.abspath(os.path.dirname(os.getcwd()))
    search_all_strings_file(startpath)
#3、如果需要重新导出一份翻译excel文案，再执行一次strins_xlsx_write，注意改一下输出excel的名称


