def has_33(nums):
    for i in range(0, len(nums)-1):
        if int(nums[i]) == 3 and int(nums[i+1]) == 3:
            return True
    return False

nums = input("Enter digits separated by spaces: ").split()
if has_33(nums):
    print("3 is next to 3")
else:
    print("No, there are no 3s next to each other")