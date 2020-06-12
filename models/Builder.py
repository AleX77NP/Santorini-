class Builder:
#klasa za graditelje
    def __init__(self, no, player, position):
        self.no = no
        self.player = player
        self.position = position
        self.has_built = False
        self.has_moved = False

    def move(self, field, game):
        if abs(ord(field[0]) - ord(self.position[0])) <= 1 and abs(ord(field[1]) - ord(self.position[1])) <= 1:
            if not game.find_field(field).has_player():
                if game.find_field(field).level < 4:
                    if game.find_field(field).level <= game.find_field(self.position).level + 1:
                        if game.find_field(field).level == 3:
                            game.winner = self.player
                        self.position = field
                        return True
        return False

    def build(self, field, game):
        if abs(ord(field[0]) - ord(self.position[0])) <= 1 and abs(ord(field[1]) - ord(self.position[1])) <= 1:
            if not game.find_field(field).has_player():
                return game.find_field(field).build()
        return False

    def reset(self):
        self.has_built = False
        self.has_moved = False

    def can_move(self, game):
        for i in [chr(ord(self.position[0]) - 1) if self.position[0] != 'A' else 'A', self.position[0], chr(ord(self.position[0]) + 1) if self.position[0] != 'E' else 'E']:
            for j in range(int(self.position[1]) - 1 if self.position[1] != '1' else 1, int(self.position[1]) + 2 if int(self.position[1]) <= 4 else 6):
                if not game.find_field(i+str(j)).has_player():
                    if game.find_field(i+str(j)).level < 4:
                        if game.find_field(i+str(j)).level <= game.find_field(self.position).level + 1:
                            return True
        return False
