import random

list_nums = []
while True:
    num = random.randint(1,14)
    if num not in list_nums:
        list_nums.append(num)
    
    if len(list_nums) == 14: break

print(list_nums)