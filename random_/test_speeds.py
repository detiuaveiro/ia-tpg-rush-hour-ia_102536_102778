from Functions import *
import time
import sys
from functools import reduce

str1 = "BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo"
lst1 = [*str1]
m1 = get_grid(str1, 6)

def get_grid_num(grid_str):
    """
    Get grid number
    """
    grid_num = 0
    letters = {'o':0, 'x': 1}
    temp = 1
    for idx, letter in enumerate(grid_str):
        if letter not in letters:
            temp += 1
            letters[letter] = temp
            
        grid_num += letters[letter] << 8*idx

    return grid_num , letters


num1 = 0
letters = {'o':0, 'x': 1}
temp = 1
for idx, letter in enumerate(str1):
    if letter not in letters:
        temp += 1
        letters[letter] = temp
        
    num1 += letters[letter] << 8*idx

nums = { v:k for k, v in letters.items() }

def print_num():
    for y in range(6):
        for x in range(6):
            print(nums[num1 >> 8*(y*6+x) & 0xFF], end=" ")
        print()

# print(f"Size of str: {sys.getsizeof(str1)}")
# print(f"Size of num: {sys.getsizeof(num1)}")
# print(f"Num hex: {hex(num1)}")

set1 = set()
set2 = set()

for i in range(10000):
    set1.add(str(i))
    set2.add(i)


# N -> s
c1 = [5,1]
c2 = [5,3]

# print_num()

# num1 -= letters['N'] << 8*(c1[0] + c1[1]*6)
# num1 += letters['N'] << 8*(c2[0] + c2[1]*6)

# print()
# print_num()


# start = time.time()
# for i in range(1000000):
#     m2 = [[*row] for row in m1]
#     m2[c1[1]][c1[0]] = 'o'
#     m2[c2[1]][c2[0]] = 'N'
#     str_ = "".join(["".join(row) for row in m2])
#     res = str_ in set1
# end = time.time()
# print(end-start)

# start = time.time()
# for i in range(1000000):
#     lst2 = [*str1]
#     lst2[c1[0] + c1[1]*6] = 'o'
#     lst2[c2[0] + c2[1]*6] = 'N'
#     str_ = "".join(lst2)
#     res = str_ in set1
# end = time.time()
# print(end-start)

# start = time.time()
# for i in range(1000000):
#     str2 = str1
#     str2 = str2[:c1[0] + c1[1]*6] + 'o' + str2[c1[0] + c1[1]*6 + 1:]
#     str2 = str2[:c2[0] + c2[1]*6] + 'N' + str2[c2[0] + c2[1]*6 + 1:]
#     res = str2 in set1
# end = time.time()
# print(end-start)

# num2 = num1

# start = time.time()
# for i in range(1000000):
#     num2 = num1
#     num2 -= letters['N'] << 8*(c1[0] + c1[1]*6)
#     num2 += letters['N'] << 8*(c2[0] + c2[1]*6)
#     res = num2 in set2
# end = time.time()
# print(end-start)


lst = [*"BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo"]

start = time.time()
for i in range(1000000):
    x = ''.join(lst)
end = time.time()
print(end - start)

start = time.time()
for i in range(1000000):
    x = reduce(lambda a,b: a+b, lst)
end = time.time()
print(end - start)

start = time.time()
for i in range(1000000):
    x = ''
    for j in lst:
        x += j
end = time.time()
print(end - start)

start = time.time()
for i in range(1000000):
    x = str(lst)
end = time.time()
print(end - start)

