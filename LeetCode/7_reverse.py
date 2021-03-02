def reser_num(num):
    '''
    逆转数字
    '''
    num=str(num)
    l=len(num)
    n=0
    for i in range(l):
        l0=pow(10,i)
        l1=int(num[i])
        n+=l0*l1
    if n > 2 ** 31 - 1 or n < -2 ** 31:
        print(0)
    else:
        print(n)
reser_num(145670)