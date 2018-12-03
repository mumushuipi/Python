#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 该脚本用来查找Objective-C *.m文件里面的中文字符串（NSLog,EKOLogDebug等Log的除外）
# 找到后，需要输入一个key，会自动放入Localizable.strings中（如果没有的话）。再在StringDef.h中生成kStr+key，最后在该文件中用StringDef.h里面的define
import os
import re

count = 0  # 统计的处理文件个数
stringcount = 0
stringcount2 = 0
keykey = 0

# StringDef.h 的路径
stringdefPath = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'CallWatch/Pods/EKOStringDefine/EKOStringDefine/StringDef.h')


#Localizable.strings 的路径

localizablePath = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'CallWatch/CallWatch/SupportingFiles/Resource/Language/zh-Hans.lproj/Localizable.strings')



baimingdan = ['Pods','Third','UMEvents.h','EKP','CallWatchTests','Testo','Logger','SettingViewController.m','LoginViewController.m','DomainViewController.m','SWViewControllerIntercepter.m','PushMessageMgr.m','EKAExtendLocation.h'] #路径白名单，路径包含这个的，不会处理
log = ['NSAssert','Log','@brief','EKAnalysis','DebugToast','deprecated','EKAClickEvent']

def addkeyInlocalizable(newkey,value,path,lineNum):

	definekey = 'kStr%s' % (newkey.capitalize())

	with open(localizablePath,'a') as f:
		f.write('"%s" = "%s";\n' %(newkey,value))

	with open(stringdefPath,'a') as f:
		f.write('#define %s    local(@"%s")\n' %(definekey,newkey))

	modityFile(path,'@"%s"'%(value),definekey,lineNum)



def modityFile(path,oldString,newString,lineNum):
		#将文件读取到内存中

	with open(path,"r",encoding="utf-8") as f:
		lines = f.readlines() 
	#写的方式打开文件
	linecount = 0
	with open(path,"w",encoding="utf-8") as f_w:
		for line in lines:

			if linecount == lineNum-1 and oldString in line:
				line = line.replace(oldString,newString)

			linecount = linecount + 1
		
			f_w.write(line)


def getDefineKey(key):
	print('findKey key',key)
	key = key.replace('"','')

	with open(stringdefPath,'r') as f:
		for line in f.readlines():

			if line.startswith('//') or r'*' in line:
				continue

			line1 = re.findall(r'kStr[^ ]*',line)
			if len(line1) != 1:
				continue

			val1 = re.findall(r'[^\\]?\"(.*?[^\\])["]',line)

			if len(val1) != 1:
				continue

			if key == val1[0]:
				print('line10 = '+line1[0])
				return line1[0]

	return None


def findKey(key):

	with open(localizablePath,'r') as f:
		for line in f.readlines():
			res = line.split('=')[1:]

			if len(res) > 0:
				str1 = res[0].replace(' ','').replace('\n','').replace(';','').replace('"','')
				if str1 == key:
					return line.split('=')[0:][0]
#				else:
#				 	print("str1:%s  key:%s" % (str1,key))

	return None



def openFile(path):
	global stringcount
	global stringcount2
	global keykey
	with open(path, 'r') as f:
		linenum = 0
		for line in f.readlines():
			linenum = linenum + 1
			
			line = line.split('//')[0]

			shouldcontinue = False

			for key in log:
				if key in line:
					shouldcontinue = True
					break


			if shouldcontinue:
				continue

			for str1 in re.findall(r'[^\\]?\"(.*?[^\\])["]',line):

				if re.search(r'[\u4e00-\u9fa5]',str1) is not None:
				
					# print(str1)

					if len(str1) == 0:
						continue

					key1 = findKey(str1)
					if len(str1) == 0:
						continue

					if key1 is not None:
						print('该字符串已经有了:' + str1)
						stringcount = stringcount + 1

						s = definekey = 'kStr%s' % (key1.replace('"','').capitalize())
						str1 = '@"'+str1 + '"'
						# print(path,str1,s,linenum)

						# print('+++++++++++',str1,s)
						modityFile(path,str1,s,linenum)


					else:
						newKey = 'newkey_String' + str(keykey)
						keykey = keykey + 1
						if newKey == '':
							#print('跳过')
							continue
						else:
							stringcount2 = stringcount2 + 1
							print('该字符串没有做本地化:' + str1)
							addkeyInlocalizable(newKey,str1,path,linenum)




def getAllFile(path):

	global count
	
	for x in os.listdir(path):
		if xtc_isBaiMingDan(x):
			continue
		path1 = os.path.join(path,x)

		if os.path.isdir(path1):
			getAllFile(path1)
		else:
			if os.path.splitext(path1)[1] == '.m' or os.path.splitext(path1)[1] == '.h' :
				count = count + 1
				openFile(path1)
				# print(path1)
	
def xtc_isBaiMingDan(path):
	for bmd in baimingdan:
		if bmd == path:
			return path
	return None 
	

if __name__ == '__main__':

	print('stringdefPath = ' + stringdefPath)
	print('localizablePath = ' + localizablePath)

	startpath = os.path.abspath(os.path.dirname(os.getcwd()))

	getAllFile(startpath)
	print("一共有",stringcount,"个字符串已经有key，全局搜一下，替换一下")
	print("一共有",stringcount2,"个字符串没有key")
	print("一共有",count,"个*.m文件")
