# libs import
import string
import random

# define empty list
rand_list = []
# define rand_number_of_dicts as a random int between 2 and 10, calculated by randint function
rand_number_of_dicts = random.randint(2, 10)
# iterator for will run rand_number_of_dicts times
for i in range(rand_number_of_dicts):
    # define rand_number_of_keys as a random int between 2 and 10, calculated by randint function
    rand_number_of_keys = random.randint(2, 10)
    # define empty dict for list elements
    rand_dict = {}
    # iterator for will run rand_number_of_keys times
    for j in range(rand_number_of_keys):
        # calculate key as a str element of string.ascii_lowercase, randomly choiced by random.choice
        rand_letter = random.choice(string.ascii_lowercase)
        # calculate value as a random int between 0 and 100, calculated by randint function
        rand_number = random.randint(0, 100)
        # update dict with calculated key and value
        rand_dict.update({rand_letter: rand_number})
    # append list with dict
    rand_list.append(rand_dict)

# define empty result dict
result_dict = {}

# iterator for each letter in string.ascii_lowercase
for letter in string.ascii_lowercase:
    # define empty dict for comparison between different dicts but for same letter
    letter_dict = {}
    # iterator for each dict in rand_list
    for dict in rand_list:
        # if this letter exists as a key in dict from rand_list
        if letter in dict:
            # update letter_dict with corresponding key-value but key is updated with dict number in rand_list
            letter_dict.update({letter + '_' + str(rand_list.index(dict) + 1): dict[letter]})
    # if only one element in letter_dict
    if len(letter_dict) == 1:
        # change key back to letter without dict number
        letter_dict.update({letter: letter_dict.popitem()[1]})
    # elif letter_dict has more than 1 element
    elif len(letter_dict) > 1:
        # calculate key corresponding to max_value: pass letter_dict as iterable and letter_dict.get function as a key
        max_key = max(letter_dict, key=letter_dict.get)
        # redefine letter_dict as one element with calculated key-value
        letter_dict = {max_key: letter_dict[max_key]}
    # update result_dict with letter_dict
    result_dict.update(letter_dict)
# print result_dict
print(result_dict)
