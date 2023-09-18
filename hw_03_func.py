import re


def letter_case_normalization(text):
    text_splitted = re.split(r'(	|[.]\s)', text)
    text_splitted_capitalized = []
    for i in text_splitted:
        text_splitted_capitalized.append(i.capitalize())
    text_normalized = "".join(text_splitted_capitalized)
    return text_normalized


def adding_sentence_from_last_words_in_paragraph(text, insert_before):
    last_words = re.findall(r'\s\S*[.]', text)
    last_words_cleared = []
    for i in last_words:
        last_words_cleared.append(i[1:-1])
    last_sentence = " ".join(last_words_cleared).capitalize() + "."
    position_to_insert = text.find(insert_before)
    text_with_new_sentence = text[:position_to_insert] + " " + last_sentence + text[position_to_insert:]
    return text_with_new_sentence


def fix_typo_iz(text):
    text_with_fixed_is = text.replace(" iz ", " is ").replace("Iz ", "Is ").replace(" iz.", " is.")
    return text_with_fixed_is


def count_ws_in_string(text):
    number_of_ws = len(re.findall(r'\s', text))
    return number_of_ws


input_text = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""


insert_sentence_before = """

        It iz misspelling here."""

# print results
print(fix_typo_iz(adding_sentence_from_last_words_in_paragraph(letter_case_normalization(input_text), insert_sentence_before)))
print(count_ws_in_string(input_text))
