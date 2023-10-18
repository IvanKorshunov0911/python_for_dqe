import csv
import re


def preprocess_word(word):
    return re.sub(r'[^a-zA-Z]', '', word)


def create_statistics(file_path):
    word_count = {}
    letter_count = {}

    total_letters = 0

    with open(file_path, 'r') as file:
        text = file.read()
        words = text.split()

        for word in words:
            preprocessed_word = preprocess_word(word)
            if preprocessed_word:
                preprocessed_lowered_word = preprocessed_word.lower()
                if preprocessed_lowered_word in word_count:
                    word_count[preprocessed_lowered_word] += 1
                else:
                    word_count[preprocessed_lowered_word] = 1

                for letter in preprocessed_word:
                    total_letters += 1
                    if letter.lower() in letter_count:
                        letter_count[letter.lower()][0] += 1
                    else:
                        letter_count[letter.lower()] = [1, 0]

                    if letter.isupper():
                        letter_count[letter.lower()][1] += 1

    for letter, counts in letter_count.items():
        counts.append(counts[0] / total_letters * 100)

    with open('word_count.csv', 'w', newline='') as word_csv:
        csv_writer = csv.writer(word_csv, delimiter='-')
        for word, count in word_count.items():
            csv_writer.writerow([word, count])

    with open('letter_count.csv', 'w', newline='') as letter_csv:
        headers = ['letter', 'count_all', 'count_uppercase', 'percentage']
        csv_writer = csv.DictWriter(letter_csv, delimiter=',', fieldnames=headers)
        csv_writer.writeheader()
        for letter, counts in letter_count.items():
            csv_writer.writerow({'letter': letter, 'count_all': counts[0], 'count_uppercase': counts[1], 'percentage': round(counts[2], 2)})


if __name__ == "__main__":
    create_statistics('magazine.txt')
