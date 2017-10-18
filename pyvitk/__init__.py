# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .prob_ugram import P as P_ugram
from .prob_bgram import P as P_bgram
import xml.etree.cElementTree as ET
import re
from . import DAG
import os

DIR = os.path.dirname(os.path.realpath(__file__))
tree = ET.parse(DIR + '\lexicon.xml')
root = tree.getroot()


def lower(string):
    from .viet_char import cap2lowList
    viet_char = cap2lowList
    low_string = ''
    for s in string.decode('utf-8'):
        try:
            low_s = viet_char[s.encode('utf-8')]
        except:
            low_s = s.encode('utf-8')
        low_string += low_s
    return low_string


def matchPatterns(sentence):
    regexpfile = open(DIR + '\\regexp.txt')
    patterns = regexpfile.readlines()
    regexpfile.close()
    for index in range(len(patterns)):
        item = patterns[index][:-1].split()
        patterns[index] = item

    replace_stock = []
    for pattern in patterns:
        match = re.finditer(re.compile(pattern[1].decode('utf-8')), sentence.decode('utf-8'))
        for item in match:
            # print pattern[0]
            # print item.group()
            # print re.sub(re.compile('(?!换)' + ))
            if pattern[0] == 'numberMixChar' or pattern[0] == 'phraseMixNumber':
                replace_stock.append({'dash': False, 'content': item.group().encode('utf-8')})
                sentence = re.sub(re.compile(item.group().encode('utf-8') + '(?!\d*换)'), '换' + str(replace_stock.index(
                    {'dash': False, 'content': item.group().encode('utf-8')})) + '换', sentence)
            elif pattern[0] == 'allcaps' or pattern[0] == 'capsMixLower':
                replace_stock.append({'dash': True, 'content': item.group().encode('utf-8')})
                sentence = re.sub(re.compile(item.group().encode('utf-8') + '(?!\d*换)'), '换' + str(replace_stock.index(
                    {'dash': True, 'content': item.group().encode('utf-8')})) + '换', sentence)
            elif pattern[0] == 'name':
                replace_stock.append({'dash': True, 'content': item.group().encode('utf-8')})
                sentence = re.sub(re.compile(item.group().encode('utf-8') + '(?!\d*换)'), '换' + str(replace_stock.index(
                    {'dash': True, 'content': item.group().encode('utf-8')})) + '换', sentence)
            elif pattern[0].count('date') != 0 or pattern[0] == 'hour' or pattern[0] == 'number' or pattern[0] == \
                    'order' or pattern[0] == 'percentage':
                replace_stock.append({'dash': False, 'content': item.group().encode('utf-8')})
                sentence = re.sub(re.compile(item.group().encode('utf-8')+'(?!\d*换)'), '换' + str(replace_stock.index(
                    {'dash': False, 'content': item.group().encode('utf-8')})) + '换', sentence)
            elif pattern[0] == 'domain' or pattern[0] == 'url':
                replace_stock.append({'dash': False, 'content': item.group().encode('utf-8')})
                sentence = re.sub(re.compile(item.group().encode('utf-8') + '(?!\d*换)'), '换' + str(replace_stock.index(
                    {'dash': False, 'content': item.group().encode('utf-8')})) + '换', sentence)
            elif pattern[0] == 'punctuation' or pattern[0] == 'parentheses' or pattern[0] == 'special':
                sentence = sentence.replace('  ', ' ').replace(item.group().encode('utf-8'), ' ' +
                                                               item.group().encode('utf-8') + ' ').replace('  ', ' ')
                if sentence[-1] == ' ':
                    sentence = sentence[:-1]
    for item in replace_stock:
        content = item['content']
        if item['dash']:
            content = item['content'].replace(' ', '_')
        sentence = sentence.replace('换' + str(replace_stock.index(item)) + '换', content)
    if sentence[-1] == ' ':
        return sentence.replace('  ', '')[:-1]
    return sentence.replace('  ', '')


def logProb(word):
    """
    该词出现的概率，返回以10为底的 log(P(word))
    :param word:
    :return: 以10为底的 log(P(word))
    """
    if word in P_ugram:
        return P_ugram[word]['prob']
    else:
        return P_ugram['<unk>']['prob']

def logConditionalProb(last_word, word):
    """
    在前词的条件下，后词出现的条件概率，返回以10为底的 log(P(word | last_word))
    :param last_word:
    :param word:
    :return: 返回以10为底的 log(P(word | last_word))
    """
    if (last_word, word) in P_bgram:
        return P_bgram[(last_word, word)]
    else:
        x = logProb(word)
        if last_word in P_ugram:
            x += P_ugram[last_word]['back']
        return x


def logJointProb(last_word, word):
    """
    前词和该词共同出现的概率 log(P(a,b))
    :param last_word:
    :param word:
    :return:
    """
    return logConditionalProb(last_word, word) + logProb(last_word)


def path2sent(PATHS, sent, numb):
    senlist = sent.split(' ')
    tok = ''
    for i in range(len(senlist)):
        if i in PATHS[numb]:
            result = tok
            tok = senlist[i]
            yield result
        else:
            if tok == '':
                tok += senlist[i]
            else:
                tok = tok + ' ' + senlist[i]
    yield tok


def cut(sentence):
    maxProb = - float('inf')
    bestPath = 0
    DAGraph = DAG.DAG()
    DAGraph.makeGraph(root, sentence)

    # for i in DAGraph.graph:
    #     for j in i:
    #         for k in j:
    #             print k,
    #         print
    #     print

    index = 0
    for PATHS in DAGraph.find_all_path():
        if index == 0:
            last_word = '<start>'
        else:
            last_word = DAGraph.punctuation[index - 1]
        for i in range(len(PATHS)):
            ConditionalProb = 0.0
            for word in path2sent(PATHS, DAGraph.sen_lists[index], i):
                ConditionalProb += logConditionalProb(last_word, word)
                last_word = word
            ConditionalProb += logConditionalProb(last_word, DAGraph.punctuation[index])
            if maxProb < ConditionalProb:
                maxProb = ConditionalProb
                bestPath = i
        senlist = DAGraph.sen_lists[index].split(' ')
        tok = ''

        for i in range(len(senlist)):
            if i in PATHS[bestPath]:
                result = tok
                tok = senlist[i]
                yield result
            else:
                if tok == '':
                    tok += senlist[i]
                else:
                    tok = tok + ' ' + senlist[i]
        yield tok
        yield DAGraph.punctuation[index]
        index += 1
        bestPath = 0
