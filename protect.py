def reverse_list(nums):
    nums2 = []
    for x in reversed(nums):
        nums2.append(x)
    return nums2
nums = [1, 2, 3, 4, 5]
print(reverse_list(nums))