# -*- coding: utf-8 -*-
import pyvitk
import re
import time
import os

DIR = os.path.dirname(os.path.realpath(__file__))
test_list = [re.sub(re.compile('/([A-Za-z0-9]|\S)+'), '', item) for item in open(DIR + '\predict.txt').readlines()]
clean_list = [re.sub(re.compile('/([A-Za-z0-9]|\S)+'), '', item.replace('_', ' ')) for item in test_list]


file = open('C:\Users\ASUS\Desktop\pre.txt', 'w')
for i in range(len(test_list)):
    cut_sen = ''
    # print 'NO.' + str(i + 1)
    # print '原句:', clean_list[i].replace('\n', '')
    start = time.clock()
    for j in pyvitk.cut(clean_list[i].replace('\n', '')):
        cut_sen = cut_sen + ' ' + j.replace(' ', '_')
    end = time.clock()
    numb = len(cut_sen[1:].split(' '))
    # print '切句:', cut_sen[1:]
    print cut_sen[1:]
    # print '共' + str(numb) + '词'
    # print '耗时' + str(end - start) + '秒'
    # print
    file.write(cut_sen[1:]+'\n')
file.close()
