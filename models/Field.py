class Field:
#klasa za teren
    def __init__(self, row_letter, col_number):
        self.row = row_letter
        self.col = col_number

        self.key = str(self.row) + str(self.col)

        self.level = 0
        self.player = None

    def update_look(self, window):
        img_name = str(self.level)
        if self.player is not None:
            img_name += str(self.player)
        else:
            img_name += '0'

        img_name += '.png'

        btn = window.find_element(self.key)
        btn.Update(image_filename='res/' + img_name, text=self.key)

    def build(self):
        if self.level < 4:
            self.level += 1
            return True
        return False

    def has_player(self):
        if self.player is not None:
            return True
        else:
            return False

    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player
