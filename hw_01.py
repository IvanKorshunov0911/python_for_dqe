# import randint function from random library
from random import randint

# define empty list
rand_list = []

# iterator for will run 100 times
for i in range(100):
    # define rand_number as a random int between 0 and 1000, calculated by randint function
    rand_number = randint(0, 1000)
    # append rand_number to rand_list
    rand_list.append(rand_number)

# iterate len(rand_list)-1 times
for i in range(len(rand_list)-1):
    # last i items are in place
    for j in range(len(rand_list)-i-1):
        # if j element less than j+1 element
        if rand_list[j] > rand_list[j+1]:
            # swap elements
            temp = rand_list[j]
            rand_list[j] = rand_list[j+1]
            rand_list[j+1] = temp

# define odd_list as an empty list
odd_list = []
# define even_list as an empty list
even_list = []
# iterate through rand_list elements
for i in range(len(rand_list)):
    # if list element has division to 2 addition 1
    if rand_list[i] % 2 == 1:
        # add this element to odd_list
        odd_list.append(rand_list[i])
    else:
        # else add to even_list
        even_list.append(rand_list[i])

# try to calculate even_list_average
try:
    # calculate average as division of sum of elements to number of elements
    even_list_average = sum(even_list)/len(even_list)
    # print result
    print(f"Average of even numbers is {even_list_average}")
# except option when where is no elements so len(even_list) is zero
except ZeroDivisionError:
    # print that there are no even numbers
    print("There are no even numbers")

# do the same for odd_list
try:
    odd_list_average = sum(odd_list)/len(odd_list)
    print(f"Average of odd numbers is {odd_list_average}")
except ZeroDivisionError:
    print("There are no odd numbers")