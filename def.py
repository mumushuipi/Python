#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#函数篇
import math

def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('自定义错误描述')
    if x >= 0:
        return x
    else:
        return -x
#angle参数可以不用传，默认是0---->>>必选参数必须在默认参数前面
def move(x,y,step,angle = 0):
	nx = x + step * math.cos(angle)
	ny = y - step * math.sin(angle)
# 返回多个函数的时候其实返回的是一个tuple，例如(151.96152422706632, 70.0)	
	return nx,ny

def quadratic(a,b,c):
	d = b*b - 4 * a * c	
	if d < 0:
		print('无实根')
		return None
	else:
		x1 = (-b + math.sqrt(d))/(2*a)
		x2 = (-b - math.sqrt(d))/(2*a)
		return x1,x2

#加个*可变参数，参数numbers接收到的是一个tuple。可以这么调用calc(1,2,3)，简化calc（[1,2,3])
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    print('sum = ',sum)
    return sum

#关键字参数，这些关键字参数在函数内部自动组装为一个dict
#kw将获得一个dict，注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

my_abs(4)
#可以单独一个个赋值，也可以直接赋值一个，结果是一个tuple
x, y = move(100, 100, 60, math.pi / 6)
print(x, y) 
#如果有两个默认参数，可以依次传参数，也可以指定参数传参
print(quadratic(1,3,c = -4))
calc(1,2,3)
#参数前面加*，可以把该list的所有参数转化为可变参数传进去
calc(*[1,2,3])
person('Michael', 30)
person('Adam', 45, gender='M', job='Engineer')
extra = {'city': 'Beijing', 'job': 'Engineer'}
#**extra表示把extra这个dict的所有key-value用关键字参数传入到函数的**kw参数
person('Jack', 24, **extra)