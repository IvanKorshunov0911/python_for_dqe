import re

text = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# letter cases normalization
text_splitted = re.split(r'(	|[.]\s)', text)
text_splitted_capitalized = []
for i in text_splitted:
    text_splitted_capitalized.append(i.capitalize())
text_normalized = "".join(text_splitted_capitalized)

# adding sentence from last words
last_words = re.findall(r'\s\S*[.]', text_normalized)
last_words_cleared = []
for i in last_words:
    last_words_cleared.append(i[1:-1])
last_sentence = " ".join(last_words_cleared).capitalize() + "."
position_to_insert = text_normalized.find("""

	It iz misspelling here.""")
text_with_new_sentence = text_normalized[:position_to_insert] + " " + last_sentence + text_normalized[position_to_insert:]

# fixing iz to is
text_with_fixed_is = text_with_new_sentence.replace(" iz ", " is ").replace("Iz ", "Is ").replace(" iz.", " is.")
number_of_ws = len(re.findall(r'\s', text))

# print results
print(text_with_fixed_is)
print(number_of_ws)
