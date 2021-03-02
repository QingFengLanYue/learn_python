#使用递归函数，计算阶乘

def factorial(n):

    if n==1:
        return 1
    else:
        return n*factorial(n-1)


result = factorial(5)
print(result)

#分形几何