import os
import json
import xml.etree.ElementTree as ET
import sqlite3
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

    def publish_txt(self):
        with open('magazine.txt', 'a') as f:
            f.write(self.publication_text)

    def publish_db(self):
        db = SQLiteDB('magazine.db')
        db.connect()
        query = f"CREATE TABLE IF NOT EXISTS {self.__class__.__name__}" \
                f"(Record VARCHAR(255)," \
                f"PRIMARY KEY (Record));"
        db.execute_query(query)
        query = f"INSERT INTO {self.__class__.__name__} (Record)" \
                f"VALUES ('{self.publication_text}');"
        db.execute_query(query)
        query = f"SELECT * FROM {self.__class__.__name__}"
        db.execute_query(query)
        results = db.fetch_data()
        for row in results:
            print(row)
        db.disconnect()


class MagazineHandler:
    def __init__(self, publication_type, text, attribute, publication_target):
        self.publication_type = publication_type
        self.text = text
        self.attribute = attribute
        self.publication_target = publication_target
        self.publication_producer()

    def publication_producer(self):
        if self.publication_type == '1':
            publication = News(self.text, self.attribute)
        elif self.publication_type == '2':
            publication = PrivateAd(self.text, self.attribute)
        elif self.publication_type == '3':
            publication = Joke(self.text)
        elif self.publication_type == '4':
            publication = FileProcessorTxt(self.publication_target)
        elif self.publication_type == '5':
            publication = FileProcessorJson(self.publication_target)
        elif self.publication_type == '6':
            publication = FileProcessorXml(self.publication_target)
        else:
            print("Publication type is not correct. Please restart.")
            exit()
        publication.preparation()
        if self.publication_target == '1':
            publication.publish_txt()
        elif self.publication_target == '2':
            publication.publish_db()
        else:
            print("Publication target is not correct. Please restart.")


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
    def __init__(self, publication_target):
        self.directory = input("Enter file path:")
        self.publication_target = publication_target
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
                                              hw_03_func.letter_case_normalization(splitted_publications[i + 2]),
                                              self.publication_target)
            os.remove(self.directory)
        except FileNotFoundError:
            print("There is no TXT file in directory")
        except IsADirectoryError:
            print("Directory is not valid")

    def publish_txt(self):
        pass

    def publish_db(self):
        pass


class FileProcessorJson(Publication):
    def __init__(self, publication_target):
        self.directory = input("Enter file path:")
        self.publication_target = publication_target
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
                                              str(dictionary['attribute']),
                                              self.publication_target)
            os.remove(self.directory)
        except FileNotFoundError:
            print("There is no JSON file in directory")
        except (json.decoder.JSONDecodeError, KeyError):
            print("JSON structure is not correct")
        except IsADirectoryError:
            print("Directory is not valid")

    def publish_txt(self):
        pass

    def publish_db(self):
        pass


class FileProcessorXml(Publication):
    def __init__(self, publication_target):
        self.directory = input("Enter file path:")
        self.publication_target = publication_target
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
                                          row.find('attribute').text,
                                          self.publication_target)
            os.remove(self.directory)
        except FileNotFoundError:
            print("There is no XML file in directory")
        except (ET.ParseError, AttributeError):
            print("XML structure is not correct")
        except IsADirectoryError:
            print("Directory is not valid")

    def publish_txt(self):
        pass

    def publish_db(self):
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
        self.publication_target = input("Enter publication target:\n"
                                        "1 for magazine.txt\n"
                                        "2 for magazine.db\n")
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
        return [self.publication_type, self.text, self.attribute, self.publication_target]


class SQLiteDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print("Connected to SQLite database.")
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print("Disconnected from SQLite database.")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_data(self):
        return self.cursor.fetchall()


if __name__ == "__main__":
    user_inputs = UserInputs()
    user_inputs_list = user_inputs.get_user_input()
    magazine_handler = MagazineHandler(user_inputs_list[0], user_inputs_list[1], user_inputs_list[2],
                                       user_inputs_list[3])
    hw_07.create_statistics('magazine.txt')
