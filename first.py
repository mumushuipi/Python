#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /除法计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数;//取结果的整数部分;%取余数
print(10 // 3)
# 逗号隔开，输出的时候中间默认为会加一个空格
print('dou','dou')
print('100 + 200 =',100 + 200)
print('100 + 200 = %s' % (100 + 200))
# 如果有单引号，可以用双引号把字符串扩起来
print("I'm OK!")
# 如果既有单引号又有双引号，可以用转义字符\来标识
print('I\'m \"OK\"')
# 换行显示，可以用三个单引号扩起来（也可以用\n方式）
print('''line1
line2
line3''')
# 如果字符串里面有很多字符都需要转义，就需要加很多\，为了简化，Python还允许用r''表示''内部的字符串默认不转义
print(r'I "OK"')
print(r'''hello,I'm "OK"\n
world''')
# 对于【单】个字符的编码，Python提供了ord()函数获取字符的整数表示,ps:ord('A') = 65;ord('中')=20013
# chr(66) = ‘B’；chr(25991) = '文'
#a = 'ABC'.encode('ascii')# b'ABC'
#a = '中文'.encode('utf-8')# b'\xe4\xb8\xad\xe6\x96\x87'
#a = b'ABC'.decode('ascii')# 'ABC'
#a = b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore') #‘中’ 如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节
a = b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
b = a
a = 'XYZ'
print('b =',b) 
#对于不变对象str来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的
b = a.replace('X','L') 
print('b =',b) 
# name = input('please input your birth:')
# name = int(name)
# if name >= 2000:
# 	print('00后')
# elif name >= 1990:
# 	print('90后')	
# else:
# 	print('90前')	

# 布尔值可以用and、or和not运算
a = 100e3
if not a < -10:
	print(a)
else:
	print(-a)
#如果要取最后一个元素，除了计算索引位置外，还可以用-1做索引，直接获取最后一个元素:classmates[-1],以此类推计算倒数第二个第三个【-2】，【-3】	
classmates = [123,['asp', 'php'],'Love','XML']
print(classmates[1][1])
classmates.insert(1,'lin')
classmates.append('none')
#删除list末尾的元素
classmates.pop()
#删除指定索引
classmates.pop(2)
print(classmates)
classmates = ['c','b','a','1']
#sort可进行数组进行排序
classmates.sort()
print(classmates)
#tuple:和数组的区别，是tuple不可变
classmates = ('Lin',520,'XML')
print(classmates)
#只有一个元素的时候要加上逗号做一区分，因为，会识别为括号，默认就是里面的元素
a = ('abc',)
print(len(a))
# range(101)生成0-100的整数序列
sum = 0
for x in range(101):
	sum = sum + x
print(sum)	
# 生成数组
sum = list(range(5))
print(sum)
#死循环可用control+c退出
# while True:
# 	print('1')
testDict = {'lin':1,'Bo':2}#如果找不到key会报错testDict['XML']
#可以使用in方法判断是不是存在key
isExit = 'XML' in testDict
print(isExit)
#如果找不到，可以使用get方法，自定义value值，也可以不写，testDict.get('XML')返回None
print(testDict.get('XML',-1))
# 要删除一个key，用pop(key)方法，对应的value也会从dict中删除
testDict.pop('lin')
# 添加key
testDict['XML'] = 3
# 请务必注意，dict内部存放的顺序和key放入的顺序是没有关系的。

# 和list比较，dict有以下几个特点：

# 查找和插入的速度极快，不会随着key的增加而变慢；
# 需要占用大量的内存，内存浪费多。
# 而list相反：

# 查找和插入的时间随着元素的增加而增加；
# 占用空间小，浪费内存很少。
# 所以，dict是用空间来换取时间的一种方法。
# 要创建一个set，需要提供一个list作为输入集合：
s1 = set([4,1,1,2,2,3,3])
s1.add(3)
s1.remove(2)
print(s1)
s2 = set([1,3,5])
# 两个set可以做数学意义上的交集、并集等操作
print((s1 & s2))

		