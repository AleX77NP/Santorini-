class MoveWriter:
#za upis poteza
    filename = ''

    @classmethod
    def init(cls, filename='santorini_gamelog.txt'):
        cls.filename = filename

    @classmethod
    def write(cls, message):
        with open(cls.filename, encoding='utf8', mode='a+') as file:
            file.write(message)
