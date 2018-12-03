#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import re

#获取所有的.m文件,key是文件名，不包含后缀（.m）,value是文件路径
all_files = {}
#未使用的.m/.h文件的白名单
unused_files_baimingdan = ['Aspects','SWViewControllerIntercepter','main','EKWebCommonApi+EKOLaunchMiniPro','EKWebCommonApi+EKOPay','XTCMenuView','SWMMapKit','SWMMapInclude','SWMGeometry','MBProgressHUD','KLCPopup','VantagesRecordTableView','VantagesCostTableView','ModifyPasswordViewController','LocationFloorView','ABCRowCell','ContactModel','ContactsCells','ContactDetailCell','ContactAddedCell','PushNotificationObject','H5PerformanceInfo','EKOLoggerMgr','EXAExtendBase','EKCWWatchContactResponseData','EKSecurityAlgorithm','AVAudioManager','DDGMacros','EKWebData','SWDAddressBook','SWDDialogFamilyChatEntity','SWDSchoolGuardJsonObject','EKCArrearsReminderResponse','EKConstantResponse','EKMessageRecordResponse','EKCWMobileWatchResponse','EkPhoneParadiseResponse','PushToWatchFrequencyData','EKThemeControlResponse','EKCWWatchAccountResponse','EKCWWatchContactData','H5PerformanceModel','WebViewJavascriptBridge_JS']
unused_fileFolder_baimingdan = ['EKP','AlertViewEx','RETableViewManager','BaiduLoc_iOSSDK_Libs_No_Bitcode_No_IDFA_v1.1']


#递归查询所有的.m文件并加到all_files数组
def find_all_point_M_file(files_array):

    for file in files_array:
        
        file_inner = glob.glob(r'%s/*' % file)

        if len(file_inner) == 0:
            if file[len(file)-2:len(file)] in ['.h','.m']:
                #1、os.path.basename(file)获取文件名（无路径）ReportLostController.m
                #2、[:-2]，去除".m"
                last_str = os.path.basename(file)[:-2]
                if last_str not in unused_files_baimingdan:
                    all_files[last_str] = file
        elif file.split('/')[-1] not in unused_fileFolder_baimingdan:
            find_all_point_M_file(file_inner)

#def find_unUsed_file(array):
#    file_names = [os.path.basename(file) for file in array]
#    unused_count = 0
#    swizz_count = 0
#    for i in range(0,len(array)):
#        file_name = file_names[i]
        #ag命令好像不能查询分类
#        commond = 'ag "%s" %s' % (file_name,path)
#        result = os.popen(commond).read()
#        if result == '':
#            print(file_name)

#去整个工程遍历文件
def search_if_file_used(path_array):
    for file in path_array:
        file_inner = glob.glob(r'%s/*' % file)
        
        if len(file_inner) == 0:
            #如果文件不是.h,.m文件，就不做处理
            if os.path.splitext(file)[1] not in ['.m','.h','.plist']:
                continue
            open_file_search_if_used(file)
        else:
            if len(all_files) == 0:
                print('所有文件都用到了，不需要再遍历了')
            else:
                search_if_file_used(file_inner)

#查看文件中是否有import该文件
def open_file_search_if_used(filePath):
    with open(filePath,'r',encoding = 'utf-8',) as f:
        for line in f.readlines():
            line = line.split('//')[0]
            line = line.split('/*')[0]
            array = re.findall(r'^#import "(.+?)"',line)
            if len(array) > 0:
                string = array[0][:-2]
#                #如果是文件自己，就不做处理
#                if string in all_files.keys() and os.path.basename(filePath)[:-2] != string:
#                    all_files.pop(string)
            else:
                array = re.findall(r'\w+',line)
                for fileName in array:
                    if fileName in all_files.keys() and os.path.basename(filePath)[:-2] != fileName:
                        all_files.pop(fileName)
        f.close()

#判断是否是用load方法做swizz
def judge_is_swizz_file(filePath):
    is_use_swizz = False
    with open(filePath,'r',encoding = 'utf-8',) as f:
        for line in f.readlines():
            array = re.findall(r'^\+\s*\(\s*void\s*\)\s*load[^\w]',line)
            if len(array) > 0:
                is_use_swizz = True
                break
        f.close()
    return is_use_swizz

if __name__ == '__main__':
#    path = input('请输入所有项目的.h和.m文件的所在的上层文件夹:\n')
    path = '/Users/linbo/Desktop/CallWatch/Watch/CallWatch/CallWatch'
    #输出该文件下的所有文件（文件夹）全路径：只遍历一层
    files = glob.glob(r'%s/*' % path)

    find_all_point_M_file(files)
    print('一共有几个.m文件：',len(all_files))
    search_if_file_used(files)
    if len(all_files) > 0:
        print('一共有%s个文件没有用到，需要判断是否用了swizz' % len(all_files))
        for filePath in all_files.values():
            split_text_array = filePath.split('+')
            if len(split_text_array) > 1:
                print(filePath)
                continue;
            filePath = filePath[:-2] + '.m'
            if not os.path.exists(filePath):
                print('不存在.m文件，看来只是个头文件而已')
                continue
            else:
#                print(filePath)
                if judge_is_swizz_file(filePath) == True:
                    print('用了swizz方法，可以排除')
                else:
                    print('基本可以删除，可以再手动确认一下')



