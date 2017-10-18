# -*- coding: utf-8 -*-
import numpy as np
import re
import pyvitk

class DAG:
    def __init__(self):
        self.PATH = []  # 临时变量
        self.PATHS = []  # 临时变量
        self.graph = []
        self.punctuation = []
        self.sen_lists = []

    def hasWord(self, element, phrase, i=0):
        for child in element.findall('n'):
            char1 = child.get('c').encode('utf-8')
            char2 = phrase[i].encode('utf-8')

            if char1 == char2:
                if i == len(phrase) - 1:
                    if '*' in [item.get('c') for item in child.findall('n')]:
                        return True
                    else:
                        return False
                else:
                    return self.hasWord(element=child, phrase=phrase, i=(i + 1))

        return False

    def makeGraph(self, element, sentence):
        new_sentence = pyvitk.matchPatterns(sentence) + ' '
        lists = re.split(re.compile('(\s[\.,\!\?\-\:;"“”\'/]+\s)+'), new_sentence.replace('_', ' '), )
        self.punctuation = [i.group().replace(' ', '') for i in re.finditer(re.compile('(\s[\.,\!\?\-\:;"“”\'/]+\s)+'), new_sentence.replace('_', ' '))]

        for index in range(len(lists)):
            if lists[index] == '':
                continue
            pun = [i for i in re.finditer(re.compile('(\s[\.,\!\?\-\:;"“”\'/]+\s)+'), lists[index])]
            if len(pun) == 1:
                if pun[0].group() == lists[index]:
                    continue
            if lists[index][-1] == ' ':
                self.sen_lists.append(lists[index][:-1])
            elif lists[index][0] == ' ':
                self.sen_lists.append(lists[index][1:])
            else:
                self.sen_lists.append(lists[index])

        if len(self.punctuation) < len(self.sen_lists):
            for i in range(len(self.sen_lists) - len(self.punctuation)):
                self.punctuation.append('')

        new_sen_list = [item.replace('_', ' ') for item in new_sentence.split(' ')]
        self.graph = [np.array([[float("inf") for k in range(len(self.sen_lists[n].split(' ')) + 1)] for i in range(len(self.sen_lists[n].split(' ')) + 1)]) for n in range(len(self.sen_lists))]

        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                self.graph[i][j, j] = 0.0

        for index in range(len(self.sen_lists)):
            sen_list = self.sen_lists[index].split(' ')
            for i_index in range(len(sen_list)):
                tok = ''
                for j_index in range(len(sen_list) - i_index):
                    tok = tok + ' ' + sen_list[j_index + i_index]
                    if re.match(re.compile('[\.,\!\?\-\:;"“”\'/]+'), tok[1:]) or len(tok) < 2:
                        self.graph[index][i_index, j_index + i_index + 1] = 1.0
                        break
                    if self.hasWord(element=element, phrase=pyvitk.lower(tok).decode('utf-8'), i=1) or tok[1:] in new_sen_list:
                        self.graph[index][i_index, j_index + i_index + 1] = 1.0

            for i_index in reversed(range(len(sen_list))):
                tok = ''
                for j_index in reversed(range(i_index + 1)):
                    tok = sen_list[j_index] + ' ' + tok
                    if re.match(re.compile('[\.,\!\?\-\:;"“”\'/]+'), tok) or len(tok) < 2:
                        break
                    if self.hasWord(element=element, phrase=pyvitk.lower(tok[:-1]).decode('utf-8'), i=0) or tok in new_sen_list:
                        self.graph[index][j_index, i_index + 1] = 1.0

    def find_all_path(self):
        for D in self.graph:
            self.findPath(D, 0)
            yield self.PATHS
            self.PATHS = []

    def findPath(self, D, i):
        length = len(D)
        for j in reversed(range(i + 1, length)):
            if D[i][j] == 1.0:
                self.PATH.append(j)
                self.findPath(D, j)
                self.PATH.pop()
        if i + 1 == len(D):
            PATH_copy = [i for i in self.PATH]  # 深拷贝一个PATH，否则全局变量PATH被递归占用，PATHS无法添加
            self.PATHS.append(PATH_copy)

    def shortPath(self, D):
        P = np.array([list(range(len(D))) for i in range(len(D))])
        for i in range(len(D)):
            for j in range(len(D)):
                for k in range(len(D)):
                    if D[i, j] > D[i, k] + D[j, k]:
                        P[i, j] = P[j, k]
                        D[i, j] = D[i, k] + D[j, k]
        path = []
        next_node = 0
        while next_node + 1 < len(P):
            next_node = max(list(P[:, next_node][next_node:]))
            path.append(next_node)
        return path
