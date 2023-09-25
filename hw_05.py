from datetime import datetime
from random import randint


class Publication:
    def __init__(self):
        self.text = input("Enter text:")
        self.publication_text = ''

    def preparation(self):
        self.publication_text = self.text + '\n'

    def publish(self):
        with open('magazine.txt', 'a') as f:
            f.write(self.publication_text)


class MagazineHandler:
    def __init__(self):
        self.publication_type = input("Enter publication type:\n"
                                      "1 for News\n"
                                      "2 for Private Ad\n"
                                      "3 for Joke\n")

    def publication_producer(self):
        if self.publication_type == '1':
            publication = News()
        elif self.publication_type == '2':
            publication = PrivateAd()
        elif self.publication_type == '3':
            publication = Joke()
        else:
            print("Publication type is not correct. Please restart.")
            exit()
        publication.preparation()
        publication.publish()


class News(Publication):
    def __init__(self):
        super().__init__()
        self.location = input("Enter location:")
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
    def __init__(self):
        super().__init__()
        self.actual_until = input("Actual until (enter date in dd/mm/yyyy format):")
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


magazine_handler = MagazineHandler()
magazine_handler.publication_producer()
