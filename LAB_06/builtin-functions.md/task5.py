
def are_all_true(tup):
    return all(tup)

my_tuple = (1, True, 3.5)
print(are_all_true(my_tuple)) 

my_tuple2 = (0, True, 3.5) 
print(are_all_true(my_tuple2)) 
