##五笔字型码与汉字转换工具
 > 背景：当前自然语言处理模型中单词级模型效果很好，但是由于英文单词天然由空格隔开，中文只有连续的字与标点，为了将各种单词级语言模型应用于中文，中文分词成了中文自然语言处理领域一个基础性研究。近来研究表明，在很多神经网络模型中，字符级语言模型效果也很好，而且从长远来看，由于字符级语言模型比单词级语言模型保留了更多的原始信息，随着神经网络模型的发展以及计算能力的提高，字符级语言模型的效果应该会更好。

 > 将每一个中文汉字当做一个字符输入字符级语言模型会导致很多问题，实验效果相对英文语料来说并不理想，经实，验先将中文汉字转化为五笔字型码，输入模型计算后再将五笔字型码转换回汉字直观效果与英文语料相近。

 > 本着分享的精神将这一想法供广大的中文自然语言处理的童鞋一起分享，同时将我自己写的小工具开源出来。欢迎各位试用,有任何问题麻烦各位发issues。
 
 > 喜欢就star一下 

## 依赖
    pip install pinyin
    
##使用
    git clone git@github.com:arcsecw/chinese_wubi.git
    cd chinese_wubi
    python w_trans.py --input your.input.file
## 参数
    --input 输入文件
    --output 指定输出文件 不指定的话默认为input文件后加个后缀.out
    --type 0 中文转化为五笔字形码 1 五笔转化回中文 2 中文转化为拼音
##程序中使用
    from w_trans import W_trans
    m_trans = W_trans()
    outputfile = m_trans.chinese_wubi('chinese.txt', 'chinese_wubi.txt')