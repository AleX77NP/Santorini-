import random as rnd
#klasa za igranje
from models.Field import Field


class Game:

    def __init__(self):
        self.all_fields = []

        for i in ['A', 'B', 'C', 'D', 'E']:
            for j in range(1, 6):
                self.all_fields.append(Field(i ,j))

        self.player1_type = None
        self.player1_builders = []
        self.player1_selected = None

        self.player2_type = None
        self.player2_builders = []
        self.player2_selected = None

        self.winner = None
        self.turn = True

    def random_field(self):
        return rnd.choice(self.all_fields)

    def check_winner(self):
        if self.winner is not None:
            import PySimpleGUI as sg
            sg.PopupOK("GAME OVER", "Winner is: " + ('Player 1!' if self.winner == 1 else 'Player 2!'))
            exit(0)

    def get_builder(self, player, key):
        if player == 1:
            if self.player1_builders[0].position == key:
                return self.player1_builders[0]
            elif self.player1_builders[1].position == key:
                return self.player1_builders[1]
        else:
            if self.player2_builders[0].position == key:
                return self.player2_builders[0]
            elif self.player2_builders[1].position == key:
                return self.player2_builders[1]

        return None

    def find_field(self, key):
        for field in self.all_fields:
            if field.key == key:
                return field

    def get_fields_list(self):
        fields = []

        for field in self.all_fields:
            fields.append(field.key + ',' + str(field.level) + ('0' if field.player is None else str(field.player)))

        return fields
