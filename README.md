pyvitk-The Vietnamese word segmenter
===================
##### Author: Ray Huang #####
##### Date time: 2017-10-19 06:38 #####
##### Email: ruibinwong@qq.com #####


## This is a Vietnamese word segmenter written in Python. ##
#### Algorithm: N-Shortest Path ####
#### The probability data is taken from Mr. Phuonglh's vn.vitk project: https://github.com/phuonglh/vn.vitk ####
#### vn.vitk is a spark project using Java. It provides multithreading work segmentation for high-speed word segmentation solution ####
#### The probability data and dictionary tree of the tokenizer is taken from the vn.vitk. ####



## 3. Usage: ##
<pre><code>
import pyvitk
sentence = 'Vietnamese sentence'
pyvitk.cut(sentence)  # word segmentation generator
</code></pre>

## 4. Performance: ##

### 5. F1 score: 0.890503181119 ###
#### Specific data ####
<pre><code>
             precision    recall  f1-score   support

          B      0.934     0.810     0.867      5793
          E      0.947     0.820     0.879      5782
          M      0.567     0.467     0.512       379
          S      0.867     0.973     0.917     13079

avg / total      0.896     0.892     0.891     25033
</code></pre>
BEMS represent the position tag in a word: B (Begin), E (End), M (Middle), and S (Single). 
