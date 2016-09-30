#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import argparse
import cPickle
import os
import pinyin
#files that saved cpicke dump map data
chinese_pinyin = '__chinese_pinyin'
chinese_wubi = '__chinese_wubi'
wubi_chinese = '__wubi_chinese'

class W_trans():

    def __init__(self):
        self.__dict={
            chinese_pinyin:'',
            chinese_wubi:'',
            wubi_chinese:'',
        }
        self.__biaodian_table = {ord(f):ord(t) \
                                 for f,t in zip(u'，。！？【】（）％＃＠＆１２３４５６７８９０；'\
                                                ,u',.!?[]()%#@&1234567890;')}
        self.__biaodian_table_ = {ord(f):ord(t) \
                                 for f,t in zip(u',.!?[]()%#@&1234567890;'\
                                                ,u'，。！？【】（）％＃＠＆１２３４５６７８９０；')}
    #检查输入文件是否合法以及对应的字典是否加载到内存

    def __check_prepare(self, infile, type):
        if not os.path.isfile(infile):
            print 'input file not a raedable file'
            return False
        if self.__dict[type] == '':
            print 'init ' + type + ' dict ...'
            self.__dict[type] = cPickle.load(open(type, 'r'))

    #五笔紧跟标点符号的时候将二者分开
    def __get_real_word(self,str):
        ret = ''
        _index = 0
        for char in str:
            if not char.isalpha():
                break
            _index += 1
            ret+=char
        return [ret,str[_index:]]

    #根据type执行 str to str 的转换
    def __m_t(self, instr='', type=''):
        if type==chinese_wubi:
            re = ''
            num_of_teshuzifu = 0
            for word in instr:
                try:
                    a = self.__dict[type][word]
                    re += a
                    num_of_teshuzifu = 0
                except:
                    if num_of_teshuzifu ==0 and word in u'0123456789':
                        re +=' '
                    num_of_teshuzifu+=1
                    re += word
            return re
        if type==chinese_pinyin:
            return pinyin.get(instr,format='strip',delimiter=' ')
        if  type==wubi_chinese:
            re = ''
            for _word in instr.split(' '):
                if _word=='':
                    re += ' '
                try:
                    _w = self.__get_real_word(_word)
                    re += self.__dict[type][_w[0]]+_w[1]
                except :
                    re += _word
            return re.translate(self.__biaodian_table_)

    #控制输入输出文件的读写以及控制缓存写入操作
    def __m_translate(self, infile, outfile, type):
        if outfile=='':
            outfile = infile + '.out'
        outfile_ = open(outfile,'w')
        with open(infile,'r') as infile:
            i = 1
            for line in infile.readlines():
                i+=1
                line = line.decode('utf-8')
                a = line.translate((self.__biaodian_table))

                a = self.__m_t(a, type)
                outfile_.write(a.encode('utf-8'))
                if(i%1000==0):
                    outfile_.flush()
        outfile_.close()
        return outfile

    #开放三个方法方便外部调用
    def chinese_pinyin(self, infile, outfile):
        type = chinese_pinyin
        self.__check_prepare(infile, type)
        return self.__m_translate(infile, outfile, type)

    def chinese_wubi(self, infile, outfile):
        type = chinese_wubi
        self.__check_prepare(infile, type)
        return self.__m_translate(infile, outfile, type)

    def wubi_chinese(self, infile, outfile):
        type = wubi_chinese
        self.__check_prepare(infile, type)
        return self.__m_translate(infile, outfile, type)

#方便命令行调用
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='', help=' input file path')
    parser.add_argument('--output', type=str, default='', help=' output file path')
    parser.add_argument('--type', type=int, default=0, help=\
        '0: chinese to wubi; 1: wubi to chinese; 2 chinese to pinyin')
    args = parser.parse_args()
    assert os.path.isfile(args.input), 'input must be a readable file'
    assert args.type in[0,1,2] ,'type must be 0 1 2'
    w_trans = W_trans()

    map = {
        0:w_trans.chinese_wubi,
        1:w_trans.wubi_chinese,
        2:w_trans.chinese_pinyin
    }

    outfile = map[args.type](args.input,args.output)

    print 'file saved in '+outfile

if __name__ == '__main__':
    main()