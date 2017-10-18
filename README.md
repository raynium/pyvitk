pyvitk越南语分词器
===================
#####作者: 黄瑞滨#####
#####时间: 2017-10-19 06:38#####

#这是一个用python写的越南语分词器#
####使用的算法为n最短路径####
####概率数据取自Phuonglh先生的vn.vitk项目: https://github.com/phuonglh/vn.vitk####
####该开源项目是用java写的, 基于spark平台, 提供多线程的分词, 分词精度高且分词速度快####
####本分词器的概率数据和词典树取自该vn.vitk, 从某种意义来说, pyvitk是vn.vitk的python改写####

#分词思路:
##+根据句子生成DAG##
##+根据词典计算概率选择DAG的最右路径##
##+用法:##
<pre><code>
import pyvitk
    sentence = 句子
    pyvitk.cut(sentence)  # 该句的词语生成器
</code></pre>
##+精度:##

##F值: 0.890503181119##
###详细数据###
<pre><code>
             precision    recall  f1-score   support

          B      0.934     0.810     0.867      5793
          E      0.947     0.820     0.879      5782
          M      0.567     0.467     0.512       379
          S      0.867     0.973     0.917     13079

avg / total      0.896     0.892     0.891     25033
</code></pre>
