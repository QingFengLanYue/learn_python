import jieba
from nltk.classify import NaiveBayesClassifier


def write_dict():
    li_txt = open(r"D:/work2/李白.txt", "rb").read()
    words  = jieba.lcut(li_txt)
    #print(words)
    # 需要提前把杜甫的诗收集一下，放在dufu.txt文本中。
    counts = {}
    cs = ["!","，","。","《","》","·"," ","\n","(","）","（","？","."," ",")","【","】","\r\n","□","com"]
    for word in words:
        if word not in cs:
            counts[word] = counts.get(word,0) + 1

    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)

    dict={}
    for i in range(100):
        dict[items[i][0]] = 100 - i
    with open("D:/work2/analibai.txt","w+",encoding='utf-8') as f:
            f.write(str(dict))

    du_txt = open(r"D:/work2/杜甫.txt", "rb").read()
    words  = jieba.lcut(du_txt)
    #print(words)
    # 需要提前把杜甫的诗收集一下，放在dufu.txt文本中。
    counts = {}
    cs = ["!","，","。","《","》","·"," ","\n","(","）","（","？","."," ",")","【","】","\r\n","〔","〕","“","”","：","！","］","［","□","、"]
    for word in words:
        if word not in cs:
                counts[word] = counts.get(word,0) + 1

    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)

    dict={}
    for i in range(100):
        dict[items[i][0]] = 100 - i
    with open("D:/work2/anadufu.txt","w+",encoding='utf-8') as f:
            f.write(str(dict))



def anay(s):
    txt_li=open("D:/work2/analibai.txt",encoding="utf-8-sig").read()
    txt_du=open("D:/work2/anadufu.txt",encoding="utf-8-sig").read()
    dict_li=eval(txt_li)
    dict_du=eval(txt_du)

    words = jieba.lcut(s,cut_all = True)
    puns = "，。？！"
    for pun in puns:
        while pun in words:
            words.remove(pun)
    while "" in words:
            words.remove("")
    sum_li = 0
    sum_du = 0
    for i in words:
        if i in dict_li:
            sum_li += dict_li[i]
        if i in dict_du:
            sum_du += dict_du[i]
    print("李白相似度：%.1f"%(sum_li/len(words)))
    print("杜甫相似度：%.1f"%(sum_du/len(words)))

#write_dict()
anay("我本将心向明月，奈何明月照沟渠")

