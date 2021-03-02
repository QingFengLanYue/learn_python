def isPalindrome(x: int) -> bool:
    result = 'True'
    if x >= 0:
        x=str(x)
        l=len(x)
        for i in range(int(l/2)):
            if x[i] != x[l-1-i] :
                result='False'
                break
        print(result)
    else :
        print('False')
# def isPalindrome(x: int) -> bool:
#     lst = list(str(x))
#     L, R = 0, len(lst)-1
#     while L <= R:
#         if lst[L] != lst[R]:
#             print(False)
#         L += 1
#         R -= 1
#     print(True)

isPalindrome(303031)

