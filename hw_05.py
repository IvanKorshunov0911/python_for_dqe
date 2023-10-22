import os
import json
import xml.etree.ElementTree as ET
import hw_03_func
import hw_07
from datetime import datetime
from random import randint


class Publication:
    def __init__(self, text):
        self.text = text
        self.publication_text = ''

    def preparation(self):
        self.publication_text = self.text + '\n'

    def publish(self):
        with open('magazine.txt', 'a') as f:
            f.write(self.publication_text)


class MagazineHandler:
    def __init__(self, publication_type, text, attribute):
        self.publication_type = publication_type
        self.text = text
        self.attribute = attribute
        self.publication_producer()

    def publication_producer(self):
        if self.publication_type == '1':
            publication = News(self.text, self.attribute)
        elif self.publication_type == '2':
            publication = PrivateAd(self.text, self.attribute)
        elif self.publication_type == '3':
            publication = Joke(self.text)
        elif self.publication_type == '4':
            publication = FileProcessorTxt()
        elif self.publication_type == '5':
            publication = FileProcessorJson()
        elif self.publication_type == '6':
            publication = FileProcessorXml()
        else:
            print("Publication type is not correct. Please restart.")
            exit()
        publication.preparation()
        publication.publish()


class News(Publication):
    def __init__(self, text, attribute):
        super().__init__(text)
        self.location = attribute
        self.current_datetime = None

    def current_datetime_calculation(self):
        self.current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")

    def preparation(self):
        self.current_datetime_calculation()
        self.publication_text = '\nNews ------------------------\n' \
                                f'{self.text}\n' \
                                f'{self.location}, {self.current_datetime}\n' \
                                f'-----------------------------\n'


class PrivateAd(Publication):
    def __init__(self, text, attribute):
        super().__init__(text)
        self.actual_until = attribute
        self.days_left = None

    def days_left_calculation(self):
        self.days_left = datetime.strptime(self.actual_until, '%d/%m/%Y') - datetime.now()

    def preparation(self):
        self.days_left_calculation()
        self.publication_text = '\nPrivate Ad ------------------\n' \
                                f'{self.text}\n' \
                                f'Actual until: {self.actual_until}, {self.days_left.days} days left\n' \
                                f'-----------------------------\n'


class Joke(Publication):
    def preparation(self):
        self.publication_text = '\nJoke of the day -------------\n' \
                                f'{self.text}\n' \
                                f'Funny meter - {randint(0, 10)} / 10\n' \
                                f'-----------------------------\n'


class FileProcessorTxt(Publication):
    def __init__(self):
        self.directory = input("Enter file path:")
        self.default_directory = os.getcwd() + '/test_publication_input.txt'
        if self.directory == "":
            self.directory = self.default_directory

    def preparation(self):
        try:
            with open(self.directory, 'r') as f:
                raw_publications = f.read()
                splitted_publications = raw_publications.split("\n")
                for i in range(0, len(splitted_publications), 3):
                    handler = MagazineHandler(splitted_publications[i],
                                              hw_03_func.letter_case_normalization(splitted_publications[i + 1]),
                                              hw_03_func.letter_case_normalization(splitted_publications[i + 2]))
            os.remove(self.directory)
        except FileNotFoundError:
            print("There is no TXT file in directory")
        except IsADirectoryError:
            print("Directory is not valid")

    def publish(self):
        pass


class FileProcessorJson(Publication):
    def __init__(self):
        self.directory = input("Enter file path:")
        self.default_directory = os.getcwd() + '/test_publication_input.json'
        if self.directory == "":
            self.directory = self.default_directory

    def preparation(self):
        try:
            with open(self.directory, 'r') as f:
                raw_publications = json.load(f)
                for dictionary in raw_publications:
                    handler = MagazineHandler(str(dictionary['type']),
                                              str(dictionary['text']),
                                              str(dictionary['attribute']))
            os.remove(self.directory)
        except FileNotFoundError:
            print("There is no JSON file in directory")
        except (json.decoder.JSONDecodeError, KeyError):
            print("JSON structure is not correct")
        except IsADirectoryError:
            print("Directory is not valid")

    def publish(self):
        pass


class FileProcessorXml(Publication):
    def __init__(self):
        self.directory = input("Enter file path:")
        self.default_directory = os.getcwd() + '/test_publication_input.xml'
        if self.directory == "":
            self.directory = self.default_directory

    def preparation(self):
        try:
            tree = ET.parse(self.directory)
            root = tree.getroot()
            for row in root.findall('row'):
                handler = MagazineHandler(row.find('type').text,
                                          row.find('text').text,
                                          row.find('attribute').text)
            os.remove(self.directory)
        except FileNotFoundError:
            print("There is no XML file in directory")
        except (ET.ParseError, AttributeError):
            print("XML structure is not correct")
        except IsADirectoryError:
            print("Directory is not valid")

    def publish(self):
        pass

class UserInputs:
    def __init__(self):
        self.publication_type = input("Enter publication type:\n"
                                      "1 for News\n"
                                      "2 for Private Ad\n"
                                      "3 for Joke\n"
                                      "4 if you want to process txt file\n"
                                      "5 if you want to process json file\n"
                                      "6 if you want to process xml file\n")
        if self.publication_type == '1':
            self.text = input("Enter text:")
            self.attribute = input("Enter location:")
        elif self.publication_type == '2':
            self.text = input("Enter text:")
            self.attribute = input("Actual until (enter date in dd/mm/yyyy format):")
        elif self.publication_type == '3':
            self.text = input("Enter text:")
            self.attribute = ""
        elif self.publication_type == '4':
            self.text = ""
            self.attribute = ""
        elif self.publication_type == '5':
            self.text = ""
            self.attribute = ""
        elif self.publication_type == '6':
            self.text = ""
            self.attribute = ""
        else:
            print("Publication type is not correct. Please restart.")
            exit()

    def get_user_input(self):
        return [self.publication_type, self.text, self.attribute]


if __name__ == "__main__":
    user_inputs = UserInputs()
    user_inputs_list = user_inputs.get_user_input()
    magazine_handler = MagazineHandler(user_inputs_list[0], user_inputs_list[1], user_inputs_list[2])
    hw_07.create_statistics('magazine.txt')
