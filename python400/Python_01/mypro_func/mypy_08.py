#测试参数传递，不可变对象
a = 100
def f1(n):
    print("n:",id(n))        #传递进来的是a对象的地址
    n = n+200            #由于a是不可变对象，因此创建新的对象n，值和a一致
    print("n:",id(n))    #n已经变成了新的对象
    print(n)
f1(a)
print("a:",id(a))