import threading
import time

import PySimpleGUI as sg

from file.MoveReader import MoveReader
from file.MoveWriter import MoveWriter
from models.AI import AILvl1, AILvl2, AILvl3
from models.Builder import Builder
from models.Game import Game

# Get new Game instance
game = Game()
# Initialize MoveWriter (set (default) writing location)
MoveWriter.init()

# Set PySimpleGUI theme -> Dark or Light + Color + Number
sg.change_look_and_feel('DarkBlack1')

# Wait after move
wait = 0.5

# Depth for MiniMax algorithm
depth = 3

# Play-by-play between two bots
play_by_play = False

# Main Menu ======================================================================================
# Make main menu layout
menu_layout = [ #matrica sa svim izborima
    [sg.Text(size=(10, 1)), sg.Text("Main menu", size=(10, 1), justification='center'), sg.Text(size=(10, 1))],
    [sg.Text("Player 1:", size=(10, 1)), sg.Text(size=(12, 1)), sg.Text("Player 2:", size=(10, 1))],
    [sg.Combo(['Human', 'AI Lvl1', 'AI Lvl2', 'AI Lvl3'], size=(10, 1), enable_events=True), sg.Text(size=(10, 1)),
     sg.Combo(['Human', 'AI Lvl1', 'AI Lvl2', 'AI Lvl3'], size=(10, 1), enable_events=True)],
    [sg.InputText("Name", size=(12, 1), disabled=True, key='p1name'), sg.Text(size=(10, 1)),
     sg.InputText("Name", size=(12, 1), disabled=True, key='p2name')],
    [sg.Text(size=(10, 1))],
    [sg.Text(size=(10, 1)), sg.Text("Difficulty:", size=(10, 1), key='diff'), sg.Text(size=(10, 1))],
    [sg.Text(size=(10, 1)), sg.Combo(['1', '2', '3', '4'], size=(10, 1)), sg.Text(size=(10, 1))],
    [sg.Text(size=(10, 1))],
    [sg.Text(size=(7, 1)), sg.Checkbox('Load moves from file'), sg.Text(size=(7, 1))],
    [sg.Text(size=(6, 1)), sg.Checkbox('Delay moves (' + str(wait) + ' sec)', disabled=True), sg.Text(size=(7, 1))],
    [sg.Text(size=(10, 1)), sg.Checkbox('Play-by-Play', disabled=True), sg.Text(size=(8, 1))],
    [sg.Text(size=(10, 1))],
    [sg.Text(size=(10, 1)), sg.OK(size=(10, 1)), sg.Text(size=(10, 1))]
]

# Create main menu window from layout
menu_window = sg.Window('Santorini - Main menu', menu_layout, icon='res/logo.ico')

# Menu flags
player1_type = None
player2_type = None
player1_name = None
player2_name = None
read_moves = None

while True:
    event, values = menu_window.read()
    # event - 0 for first combo, 1 for second
    if str(event) == '0':  # Player 1 type changed
        if menu_window.find_element(event).Get() == 'Human':  # if Player 1 is Human
            menu_window.find_element('p1name').Update(disabled=False)  # Enable name field
            menu_window.find_element(5).Update(disabled=True)  # Disable Play by Play checkbox
            if menu_window.find_element(1).Get() == 'Human':  # if other player is also Human
                menu_window.find_element(4).Update(disabled=True)  # Disable delay checkbox
        else:  # if Player 1 is not Human
            menu_window.find_element('p1name').Update(value="Name", disabled=True)  # Reset and disable name field
            menu_window.find_element(4).Update(disabled=False)  # Enable delay checkbox
            if menu_window.find_element(0).Get() != 'Human':  # if other player is also a bot
                menu_window.find_element(5).Update(disabled=False)  # Enable Play by Play checkbox
    elif str(event) == '1':  # Player 2 type changed
        if menu_window.find_element(event).Get() == 'Human':  # if Player 2 is Human
            menu_window.find_element('p2name').Update(disabled=False)  # Enable name field
            menu_window.find_element(5).Update(disabled=True)  # Disable Play by Play checkbox
            if menu_window.find_element(0).Get() == 'Human':  # if other player is also Human
                menu_window.find_element(4).Update(disabled=True)  # Disable delay checkbox
        else:  # if Player 2 is not Human
            menu_window.find_element('p2name').Update(value="Name", disabled=True)  # Reset and disable name field
            menu_window.find_element(4).Update(disabled=False)  # Enable delay checkbox
            if menu_window.find_element(0).Get() != 'Human':  # if other player is also a bot
                menu_window.find_element(5).Update(disabled=False)  # Enable Play by Play checkbox

    if event in (None, 'Cancel'):
        exit(1)
    if event == 'OK':
        # If any of the fields are empty, show warning
        if len([True for k, v in values.items() if v == '']) > 0:
            sg.PopupOK('All fields are required!', 'Please fill all of the fields!')
        else:
            game.player1_type = values[0]
            game.player2_type = values[1]
            read_moves = values[3]

            play_by_play = values[5]

            if game.player1_type == 'Human':
                player1_name = values['p1name']
            else:
                player1_name = game.player1_type

            if game.player2_type == 'Human':
                player2_name = values['p2name']
            else:
                player2_name = game.player2_type

            depth = int(values[2])

            if not values[4]:
                wait = 0

            if read_moves:
                read_moves = None
                while read_moves is None:
                    read_moves = sg.PopupGetFile('Read moves from a file', 'Choose a file:', multiple_files=False)
                    if read_moves is None or read_moves == '':
                        read_moves = None
                        if sg.PopupGetText('Continue without reading from file? (Y/N)', 'Continue?') in ['y', 'Y']:
                            read_moves = None
                            break
            else:
                read_moves = None

            break

if read_moves is not None:
    # Start MoveReader from chosen file
    MoveReader.init(game, read_moves)
# Main Menu ======================================================================================


# Generate fields
fields = [[sg.Text('', size=(1, 2), justification='center'),
           sg.Text('1', size=(13, 2), justification='center'),
           sg.Text('2', size=(11, 2), justification='center'),
           sg.Text('3', size=(12, 2), justification='center'),
           sg.Text('4', size=(12, 2), justification='center'),
           sg.Text('5', size=(10, 2), justification='center')]]

for i in ['A', 'B', 'C', 'D', 'E']:
    row_of_fields = []
    for j in range(1, 6):
        if len(row_of_fields) == 0:
            row_of_fields.append(sg.Text(str(i)))
        row_of_fields.append(sg.Button(i + str(j), image_filename='res/00.png', auto_size_button=False))
    fields.append(row_of_fields)

turn_label = sg.Text('Player 1\'s turn...' if game.turn else 'Player 2\'s turn...', size=(70, 1))

layout = fields + [[turn_label]]

window = sg.Window('Santorini - ' + player1_name + ' vs ' + player2_name, layout, icon='res/logo.ico')
window.finalize()

# If a bot has to start the game
if game.player1_type != "Human":
    success = False
    while not success:
        field = game.random_field()
        if not field.has_player():
            p1_builder = Builder(len(game.player1_builders), 1, field.key)
            game.player1_builders.append(p1_builder)
            field.set_player(1)
            if len(game.player1_builders) == 2:
                MoveWriter.write(
                    game.player1_builders[0].position + ' ' + game.player1_builders[1].position + '\n')
            success = True
    game.turn = not game.turn
    turn_label.Update(value='Player 2\'s turn...', text_color='Red')

    if game.player2_type != 'Human':
        # Player two has to be started by pressing one button due to GUI rules after the window.read is called
        if not play_by_play:
            def thread_func():
                time.sleep(1.5)
                window.find_element('A1').TKButton.invoke()

            t = threading.Thread(target=thread_func)
            t.start()

window.finalize()
for field in game.all_fields:
    field.update_look(window)

# Main loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break

    btn = window.find_element(event)
    field = game.find_field(event)

    turn_finished = False
    if game.turn:  # If Player 1 is on the move
        if game.player1_type == 'Human':
            # HUMAN ====================================================================
            if len(game.player1_builders) < 2:  # start phase | positioning phase
                if not field.has_player():
                    p1_builder = Builder(len(game.player1_builders), 1, field.key)
                    game.player1_builders.append(p1_builder)
                    field.set_player(1)
                    turn_finished = True
                    if len(game.player1_builders) == 2:
                        MoveWriter.write(
                            game.player1_builders[0].position + ' ' + game.player1_builders[1].position + '\n')
            else:  # move / build phase
                # Select a builder
                if field.has_player() and field.get_player() == 1:
                    game.player1_selected = game.get_builder(1, event)
                    turn_label.Update(value='Player 1 selected builder at ' + field.key + ' (Move phase)',
                                      text_color='LightBlue')
                elif game.player1_selected is not None:
                    curr_field = game.find_field(game.player1_selected.position)
                    if not game.player1_selected.has_moved:
                        if game.player1_selected.move(event, game):
                            curr_field.set_player(None)
                            field.set_player(1)
                            game.player1_selected.has_moved = True
                            turn_label.Update(value='Player 1 selected builder at ' + field.key + ' (Build phase)',
                                              text_color='LightBlue')
                            MoveWriter.write(curr_field.key + ' ' + field.key + ' ')
                    elif not game.player1_selected.has_built:
                        if game.player1_selected.build(event, game):
                            game.player1_selected.has_built = True
                            turn_finished = True
                            MoveWriter.write(event + '\n')
            # HUMAN ====================================================================
        else:
            if len(game.player1_builders) < 2:
                success = False
                while not success:
                    field = game.random_field()
                    if not field.has_player():
                        p1_builder = Builder(len(game.player1_builders), 1, field.key)
                        game.player1_builders.append(p1_builder)
                        field.set_player(1)
                        if len(game.player1_builders) == 2:
                            MoveWriter.write(
                                game.player1_builders[0].position + ' ' + game.player1_builders[1].position + '\n')
                        success = True
                turn_finished = True
                turn_label.Update(value='Player 2\'s turn...', text_color='Red')
            else:
                move = ''
                if game.player1_type == 'AI Lvl1':
                    move = AILvl1.get_minimax_result(1, game.get_fields_list(), depth)
                elif game.player1_type == 'AI Lvl2':
                    move = AILvl2.get_minimax_result(1, game.get_fields_list(), depth, -9999, 9999)
                elif game.player1_type == 'AI Lvl3':
                    move = AILvl3.get_minimax_result(1, game.get_fields_list(), depth, -9999, 9999)

                # print('Player 1')
                # print(move)

                move_builder = move[0].split(' ')[0].strip()
                move_to = move[0].split(' ')[1].strip()
                move_build = move[0].split(' ')[2].strip()

                field_builder = game.find_field(move_builder)
                field_move_to = game.find_field(move_to)
                field_move_build = game.find_field(move_build)

                game.get_builder(1, field_builder.key).move(field_move_to.key, game)

                field_builder.set_player(None)
                field_move_to.set_player(1)

                field_builder.update_look(window)
                field_move_to.update_look(window)

                field_move_build.build()
                field_move_build.update_look(window)

                turn_finished = True
                window.finalize()

                MoveWriter.write(move[0] + '\n')

                time.sleep(wait)

        if turn_finished:
            window.finalize()
            if len(game.player2_builders) == 2:
                if not game.player2_builders[0].can_move(game) and not game.player2_builders[1].can_move(game):
                    sg.PopupOK("GAME OVER", "Winner is: Player 1!")
                    exit(0)
            if game.player1_selected is not None:
                game.player1_selected.reset()
                game.player1_selected = None
            game.turn = False
            turn_label.Update(value='Player 2\'s turn...', text_color='Red')

            if game.player2_type != 'Human':
                if not play_by_play:
                    window.find_element('A1').TKButton.invoke()
    else:
        if game.player2_type == 'Human':
            # HUMAN ====================================================================
            if len(game.player2_builders) < 2:  # start phase
                if not field.has_player():
                    p2_builder = Builder(len(game.player2_builders), 2, field.key)
                    game.player2_builders.append(p2_builder)
                    field.set_player(2)
                    turn_finished = True
                    if len(game.player2_builders) == 2:
                        MoveWriter.write(
                            game.player2_builders[0].position + ' ' + game.player2_builders[1].position + '\n')
            else:  # move / build phase
                # Select a builder
                if field.has_player() and field.get_player() == 2:
                    game.player2_selected = game.get_builder(2, event)
                    turn_label.Update(value='Player 2 selected builder at ' + field.key + ' (Move phase)',
                                      text_color='Red')
                elif game.player2_selected is not None:
                    curr_field = game.find_field(game.player2_selected.position)
                    if not game.player2_selected.has_moved:
                        if game.player2_selected.move(event, game):
                            curr_field.set_player(None)
                            field.set_player(2)
                            game.player2_selected.has_moved = True
                            turn_label.Update(value='Player 2 selected builder at ' + field.key + ' (Build phase)',
                                              text_color='Red')
                            MoveWriter.write(curr_field.key + ' ' + field.key + ' ')
                    elif not game.player2_selected.has_built:
                        if game.player2_selected.build(event, game):
                            game.player2_selected.has_built = True
                            turn_finished = True
                            MoveWriter.write(event + '\n')
            # HUMAN ====================================================================
        else:
            if len(game.player2_builders) < 2:
                success = False
                while not success:
                    field = game.random_field()
                    if not field.has_player():
                        p2_builder = Builder(len(game.player2_builders), 2, field.key)
                        game.player2_builders.append(p2_builder)
                        field.set_player(2)
                        if len(game.player2_builders) == 2:
                            MoveWriter.write(
                                game.player2_builders[0].position + ' ' + game.player2_builders[1].position + '\n')
                        success = True
                turn_finished = True
                turn_label.Update(value='Player 1\'s turn...', text_color='Red')
            else:
                move = ''
                if game.player2_type == 'AI Lvl1':
                    move = AILvl1.get_minimax_result(2, game.get_fields_list(), depth)
                elif game.player2_type == 'AI Lvl2':
                    move = AILvl2.get_minimax_result(2, game.get_fields_list(), depth, -9999, 9999)
                elif game.player2_type == 'AI Lvl3':
                    move = AILvl3.get_minimax_result(2, game.get_fields_list(), depth, -9999, 9999)

                print('Player 2')
                print(move)

                move_builder = move[0].split(' ')[0].strip()
                move_to = move[0].split(' ')[1].strip()
                move_build = move[0].split(' ')[2].strip()

                field_builder = game.find_field(move_builder)
                field_move_to = game.find_field(move_to)
                field_move_build = game.find_field(move_build)

                game.get_builder(2, field_builder.key).move(field_move_to.key, game)

                field_builder.set_player(None)
                field_move_to.set_player(2)

                field_builder.update_look(window)
                field_move_to.update_look(window)

                field_move_build.build()
                field_move_build.update_look(window)

                turn_finished = True
                window.finalize()

                MoveWriter.write(move[0] + '\n')

                time.sleep(wait)

        if turn_finished:
            window.finalize()
            if len(game.player1_builders) == 2:
                if not game.player1_builders[0].can_move(game) and not game.player1_builders[1].can_move(game):
                    sg.PopupOK("GAME OVER", "Winner is: Player 2!")
                    exit(0)
            if game.player2_selected is not None:
                game.player2_selected.reset()
                game.player2_selected = None
            game.turn = True
            turn_label.Update(value='Player 1\'s turn...', text_color='LightBlue')

            if game.player1_type != 'Human':
                if not play_by_play:
                    window.find_element('A1').TKButton.invoke()

    game.check_winner()
    for field in game.all_fields:
        field.update_look(window)

window.close()
