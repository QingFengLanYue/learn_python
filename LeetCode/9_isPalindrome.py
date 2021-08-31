def isPalindrome(x: int) -> bool:
    result = True
    if x >= 0:
        x = str(x)
        m = len(x)
        for i in range(m // 2):
            if x[i] != x[m - 1 - i]:
                result = False
                break
        return result
    else:
        return False


# def isPalindrome(x: int) -> bool:
#     lst = list(str(x))
#     L, R = 0, len(lst)-1
#     while L <= R:
#         if lst[L] != lst[R]:
#             print(False)
#         L += 1
#         R -= 1
#     print(True)

a = isPalindrome(334334)
print(a)
