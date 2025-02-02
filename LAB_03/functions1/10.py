def list_of_unique(items):
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items

cinlist = input("Enter list: ").split()
print("List of Unique elements:")
print(list_of_unique(cinlist))
