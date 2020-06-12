from models.Builder import Builder

#za citanje poteza
class MoveReader:
    filename = ''

    @classmethod
    def init(cls, game, filename='saved_state.txt'):
        cls.filename = filename
        cls.game = game

        with open(filename, encoding='utf8', mode='r') as file:
            lines = file.readlines()
            # First two lines create builders
            p1_builders = lines[0]
            p2_builders = lines[1]

            game.player1_builders = [Builder(0, 1, p1_builders.split(' ')[0].strip()), Builder(1, 1, p1_builders.split(' ')[1].strip())]
            game.player2_builders = [Builder(0, 2, p2_builders.split(' ')[0].strip()), Builder(1, 2, p2_builders.split(' ')[1].strip())]

            game.find_field(p1_builders.split(' ')[0].strip()).player = 1
            game.find_field(p1_builders.split(' ')[1].strip()).player = 1

            game.find_field(p2_builders.split(' ')[0].strip()).player = 2
            game.find_field(p2_builders.split(' ')[1].strip()).player = 2

            # Other lines are moves
            for line in lines[2:]:
                builder_field = line.split(' ')[0].strip()
                to = line.split(' ')[1].strip()
                build_spot = line.split(' ')[2].strip()

                builder = game.get_builder(1 if game.turn else 2, builder_field)

                game.find_field(builder_field).player = None
                game.find_field(to).player = 1 if game.turn else 2
                game.find_field(build_spot).build()

                builder.position = to
                game.turn = not game.turn


