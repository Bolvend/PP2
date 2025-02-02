def has_007(nums):
    sequence = [0, 0, 7]
    for num in nums:
        if int(num) == sequence[0]:
            sequence.pop(0)
        if not sequence:
            return True
    return False

# Считываем ввод пользователя и разбиваем строку по пробелам
nums = input("Enter digits separated by spaces: ").split()

if has_007(nums):
    print("agent 007 here")
else:
    print("agent 007 not here")
