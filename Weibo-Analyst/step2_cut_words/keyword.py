#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
jieba.load_userdict("SogouLabDic.txt")
jieba.load_userdict("dict_baidu_utf8.txt")
jieba.load_userdict("dict_pangu.txt")
jieba.load_userdict("dict_sougou_utf8.txt")
jieba.load_userdict("dict_tencent_utf8.txt")
jieba.load_userdict("my_dict.txt")

jieba.analyse.set_stop_words('Stopword.txt')

USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)

content = open(file_name, 'rb').read()
tags = jieba.analyse.extract_tags(content, topK=topK,withWeight=False, allowPOS=('n','nr','ns'))
print(",".join(tags))
tags = jieba.analyse.textrank(content, topK=topK, withWeight=False, allowPOS=('n','nr','ns'))
print(",".join(tags))