#encoding=utf-8
import jieba
seq_list=jieba.cut("我来到北京大学",cut_all=True)
#print("Full mode"+ "/ ".join(seq_list))

seq_list=jieba.cut("我来到北京大学吃了一碗牛肉拉面，然后研究生命的起源，使用户满意",cut_all=False)
print("Full mode : "+ "/  ".join(seq_list))