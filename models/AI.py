# Multiplier for Lvl3 AI
multiplier = 20

#Klasa za AI igraca

class AILvl3:
    @classmethod
    def get_minimax_result(cls, player, fields, level, alpha, beta, maximizer=True):
        combinations = []

        builders = []

        for field in fields:
            if field[4] == str(player):
                builders.append(field[0] + field[1])

        for builder in builders:
            neighbors = []
            for i in [chr(ord(builder[0]) - 1) if builder[0] != 'A' else 'A', builder[0],
                      chr(ord(builder[0]) + 1) if builder[0] != 'E' else 'E']:
                for j in range(int(builder[1]) - 1 if builder[1] != '1' else 1,
                               int(builder[1]) + 2 if int(builder[1]) <= 4 else 6):
                    if not cls.find_field(fields, i + str(j))[4] != '0':
                        if cls.find_field(fields, i + str(j))[3] < '4':
                            if ord(cls.find_field(fields, i + str(j))[3]) <= ord(
                                    cls.find_field(fields, builder)[3]) + 1:
                                neighbors.append(i + str(j))

            neighbors_pairs = []
            for n in neighbors:
                for i in [chr(ord(n[0]) - 1) if n[0] != 'A' else 'A', n[0],
                          chr(ord(n[0]) + 1) if n[0] != 'E' else 'E']:
                    for j in range(int(n[1]) - 1 if n[1] != '1' else 1,
                                   int(n[1]) + 2 if int(n[1]) <= 4 else 6):
                        if not cls.find_field(fields, i + str(j))[4] != '0':
                            if cls.find_field(fields, i + str(j))[3] < '4':
                                if n + ' ' + i + str(j) not in neighbors_pairs:
                                    neighbors_pairs.append(n + ' ' + i + str(j))

            for np in neighbors_pairs:
                if np.split(' ')[0] != np.split(' ')[1]:
                    combinations.append(builder + ' ' + np)

        # print(str(level) + ' - ' + str(len(combinations)))
        if level == 1:
            if maximizer:
                max = -10000
                max_combo = ''

                for combo in combinations:
                    res = cls.static_eval_func(player, fields, combo.split(' ')[1].strip(), combo.split(' ')[2].strip(), maximizer)
                    if res > max:
                        max = res
                        max_combo = combo
                        # ALPHA
                        if max > alpha:
                            alpha = max
                        if beta <= alpha:
                            break
                        # END ALPHA
                return max_combo, max
            else:
                min = 10000
                min_combo = ''

                for combo in combinations:
                    res = cls.static_eval_func(player, fields, combo.split(' ')[1].strip(), combo.split(' ')[2].strip(), maximizer)
                    if res < min:
                        min = res
                        min_combo = combo
                        # BETA
                        if min < beta:
                            beta = min
                        if beta <= alpha:
                            break
                        # END BETA
                return min_combo, min
        else:
            if maximizer:
                max = -10000
                max_combo = ''

                for combo in combinations:
                    old = combo.split(' ')[0].strip()
                    new = combo.split(' ')[1].strip()
                    build = combo.split(' ')[2].strip()

                    new_fields = []

                    for field in fields:
                        new_f = field

                        if field[0] + field[1] == old:
                            new_f = new_f[:-1] + '0'
                        if field[0] + new_f[1] == new:
                            new_f = new_f[:-1] + str(player)
                        if field[0] + field[1] == build:
                            new_f = new_f[:-2] + str(int(new_f[-2]) + 1) + new_f[-1]

                        new_fields.append(new_f)

                    best, res = cls.get_minimax_result(1 if player == 2 else 2, new_fields, level - 1, alpha, beta, False)
                    if res > max:
                        max = res
                        max_combo = combo
                        # ALPHA
                        if max > alpha:
                            alpha = max
                        if beta <= alpha:
                            break
                        # END ALPHA

                return max_combo, max
            else:
                min = 10000
                min_combo = ''

                for combo in combinations:
                    old = combo.split(' ')[0].strip()
                    new = combo.split(' ')[1].strip()
                    build = combo.split(' ')[2].strip()

                    new_fields = []

                    for field in fields:
                        new_f = field

                        if field[0] + field[1] == old:
                            new_f = new_f[:-1] + '0'
                        if field[0] + new_f[1] == new:
                            new_f = new_f[:-1] + str(player)
                        if field[0] + field[1] == build:
                            new_f = new_f[:-2] + str(int(new_f[-2]) + 1) + new_f[-1]

                        new_fields.append(new_f)

                    best, res = cls.get_minimax_result(1 if player == 2 else 2, new_fields, level - 1, alpha, beta)

                    if res < min:
                        min = res
                        min_combo = combo
                        # BETA
                        if min < beta:
                            beta = min
                        if beta <= alpha:
                            break
                        # END BETA

                return min_combo, min

    @classmethod
    def static_eval_func(cls, player, fields, exam_move_field, exam_build_field, maximizer=True):

        m = int(cls.find_field(fields, exam_move_field)[3]) + 1
        l = int(cls.find_field(fields, exam_build_field)[3]) + 1
        # pomnožen razlikom rastojanja sopstvenih i protivničkih igrača od tog polja

        my_builders = []
        enemy_builders = []
        for field in fields:
            if field[4] == str(player):
                my_builders.append(field[0] + field[1])
            elif field[4] != str(player):
                enemy_builders.append(field[0] + field[1])

        if m == 4:  # Win
            if maximizer:
                return 9999
            else:
                return -9999

        my_dist = 0
        enemy_dist = 0
        for builder in my_builders:
            my_dist += abs(ord(builder[0]) - ord(exam_build_field[0])) + abs(ord(builder[1]) - ord(exam_build_field[1]))
        for builder in enemy_builders:
            enemy_dist += abs(ord(builder[0]) - ord(exam_build_field[0])) + abs(
                ord(builder[1]) - ord(exam_build_field[1]))

        l *= (my_dist - enemy_dist)

        return (multiplier if maximizer else -multiplier) * m + (l if maximizer else -l)

    @classmethod
    def find_field(cls, fields, key):
        for field in fields:
            if field[0] + field[1] == key:
                return field


class AILvl2:
    @classmethod
    def get_minimax_result(cls, player, fields, level, alpha, beta, maximizer=True):
        combinations = []

        builders = []

        for field in fields:
            if field[4] == str(player):
                builders.append(field[0] + field[1])

        for builder in builders:
            neighbors = []
            for i in [chr(ord(builder[0]) - 1) if builder[0] != 'A' else 'A', builder[0],
                      chr(ord(builder[0]) + 1) if builder[0] != 'E' else 'E']:
                for j in range(int(builder[1]) - 1 if builder[1] != '1' else 1,
                               int(builder[1]) + 2 if int(builder[1]) <= 4 else 6):
                    if not cls.find_field(fields, i + str(j))[4] != '0':
                        if cls.find_field(fields, i + str(j))[3] < '4':
                            if ord(cls.find_field(fields, i + str(j))[3]) <= ord(
                                    cls.find_field(fields, builder)[3]) + 1:
                                neighbors.append(i + str(j))

            neighbors_pairs = []
            for n in neighbors:
                for i in [chr(ord(n[0]) - 1) if n[0] != 'A' else 'A', n[0],
                          chr(ord(n[0]) + 1) if n[0] != 'E' else 'E']:
                    for j in range(int(n[1]) - 1 if n[1] != '1' else 1,
                                   int(n[1]) + 2 if int(n[1]) <= 4 else 6):
                        if not cls.find_field(fields, i + str(j))[4] != '0':
                            if cls.find_field(fields, i + str(j))[3] < '4':
                                if n + ' ' + i + str(j) not in neighbors_pairs:
                                    neighbors_pairs.append(n + ' ' + i + str(j))

            for np in neighbors_pairs:
                if np.split(' ')[0] != np.split(' ')[1]:
                    combinations.append(builder + ' ' + np)

        if level == 1:
            if maximizer:
                max = -10000
                max_combo = ''

                for combo in combinations:
                    res = cls.static_eval_func(player, fields, combo.split(' ')[1].strip(), combo.split(' ')[2].strip(), maximizer)
                    if res > max:
                        max = res
                        max_combo = combo
                        # ALPHA
                        if max > alpha:
                            alpha = max
                        if beta <= alpha:
                            break
                        # END ALPHA
                return max_combo, max
            else:
                min = 10000
                min_combo = ''

                for combo in combinations:
                    res = cls.static_eval_func(player, fields, combo.split(' ')[1].strip(), combo.split(' ')[2].strip(), maximizer)
                    if res < min:
                        min = res
                        min_combo = combo
                        # BETA
                        if min < beta:
                            beta = min
                        if beta <= alpha:
                            break
                        # END BETA
                return min_combo, min
        else:
            if maximizer:
                max = -10000
                max_combo = ''

                for combo in combinations:
                    old = combo.split(' ')[0].strip()
                    new = combo.split(' ')[1].strip()
                    build = combo.split(' ')[2].strip()

                    new_fields = []

                    for field in fields:
                        new_f = field

                        if field[0] + field[1] == old:
                            new_f = new_f[:-1] + '0'
                        if field[0] + new_f[1] == new:
                            new_f = new_f[:-1] + str(player)
                        if field[0] + field[1] == build:
                            new_f = new_f[:-2] + str(int(new_f[-2]) + 1) + new_f[-1]

                        new_fields.append(new_f)

                    best, res = cls.get_minimax_result(1 if player == 2 else 2, new_fields, level - 1, alpha, beta, False)
                    if res > max:
                        max = res
                        max_combo = combo
                        # ALPHA
                        if max > alpha:
                            alpha = max
                        if beta <= alpha:
                            break
                        # END ALPHA

                return max_combo, max
            else:
                min = 10000
                min_combo = ''

                for combo in combinations:
                    old = combo.split(' ')[0].strip()
                    new = combo.split(' ')[1].strip()
                    build = combo.split(' ')[2].strip()

                    new_fields = []

                    for field in fields:
                        new_f = field

                        if field[0] + field[1] == old:
                            new_f = new_f[:-1] + '0'
                        if field[0] + new_f[1] == new:
                            new_f = new_f[:-1] + str(player)
                        if field[0] + field[1] == build:
                            new_f = new_f[:-2] + str(int(new_f[-2]) + 1) + new_f[-1]

                        new_fields.append(new_f)

                    best, res = cls.get_minimax_result(1 if player == 2 else 2, new_fields, level - 1, alpha, beta)
                    if res < min:
                        min = res
                        min_combo = combo
                        # BETA
                        if min < beta:
                            beta = min
                        if beta <= alpha:
                            break
                        # END BETA

                return min_combo, min

    @classmethod
    def static_eval_func(cls, player, fields, exam_move_field, exam_build_field, maximizer=True):

        m = int(cls.find_field(fields, exam_move_field)[3]) + 1
        l = int(cls.find_field(fields, exam_build_field)[3]) + 1
        # pomnožen razlikom rastojanja sopstvenih i protivničkih igrača od tog polja

        my_builders = []
        enemy_builders = []
        for field in fields:
            if field[4] == str(player):
                my_builders.append(field[0] + field[1])
            elif field[4] != str(player):
                enemy_builders.append(field[0] + field[1])

        if m == 4:  # Win
            if maximizer:
                return 9999
            else:
                return -9999

        my_dist = 0
        enemy_dist = 0
        for builder in my_builders:
            my_dist += abs(ord(builder[0]) - ord(exam_build_field[0])) + abs(ord(builder[1]) - ord(exam_build_field[1]))
        for builder in enemy_builders:
            enemy_dist += abs(ord(builder[0]) - ord(exam_build_field[0])) + abs(
                ord(builder[1]) - ord(exam_build_field[1]))

        l *= (my_dist - enemy_dist)

        return m + l

    @classmethod
    def find_field(cls, fields, key):
        for field in fields:
            if field[0] + field[1] == key:
                return field


class AILvl1:
    @classmethod
    def get_minimax_result(cls, player, fields, level, maximizer=True):
        combinations = []

        builders = []

        for field in fields:
            if field[4] == str(player):
                builders.append(field[0] + field[1])

        for builder in builders:
            neighbors = []
            for i in [chr(ord(builder[0]) - 1) if builder[0] != 'A' else 'A', builder[0],
                      chr(ord(builder[0]) + 1) if builder[0] != 'E' else 'E']:
                for j in range(int(builder[1]) - 1 if builder[1] != '1' else 1,
                               int(builder[1]) + 2 if int(builder[1]) <= 4 else 6):
                    if not cls.find_field(fields, i + str(j))[4] != '0':
                        if cls.find_field(fields, i + str(j))[3] < '4':
                            if ord(cls.find_field(fields, i + str(j))[3]) <= ord(cls.find_field(fields, builder)[3]) + 1:
                                neighbors.append(i + str(j))

            neighbors_pairs = []
            for n in neighbors:
                for i in [chr(ord(n[0]) - 1) if n[0] != 'A' else 'A', n[0],
                         chr(ord(n[0]) + 1) if n[0] != 'E' else 'E']:
                    for j in range(int(n[1]) - 1 if n[1] != '1' else 1,
                                   int(n[1]) + 2 if int(n[1]) <= 4 else 6):
                        if not cls.find_field(fields, i + str(j))[4] != '0':
                            if cls.find_field(fields, i + str(j))[3] < '4':
                                if n + ' ' + i + str(j) not in neighbors_pairs:
                                    neighbors_pairs.append(n + ' ' + i + str(j))

            for np in neighbors_pairs:
                if np.split(' ')[0] != np.split(' ')[1]:
                    combinations.append(builder + ' ' + np)

        if level == 1:
            if maximizer:
                max = -10000
                max_combo = ''

                for combo in combinations:
                    res = cls.static_eval_func(player, fields, combo.split(' ')[1].strip(), combo.split(' ')[2].strip(), maximizer)
                    if res > max:
                        max = res
                        max_combo = combo
                return max_combo, max
            else:
                min = 10000
                min_combo = ''

                for combo in combinations:
                    res = cls.static_eval_func(player, fields, combo.split(' ')[1].strip(), combo.split(' ')[2].strip(), maximizer)
                    if res < min:
                        min = res
                        min_combo = combo
                return min_combo, min
        else:
            if maximizer:
                max = -10000
                max_combo = ''

                for combo in combinations:
                    old = combo.split(' ')[0].strip()
                    new = combo.split(' ')[1].strip()
                    build = combo.split(' ')[2].strip()

                    new_fields = []

                    for field in fields:
                        new_f = field

                        if field[0] + field[1] == old:
                            new_f = new_f[:-1] + '0'
                        if field[0] + new_f[1] == new:
                            new_f = new_f[:-1] + str(player)
                        if field[0] + field[1] == build:
                            new_f = new_f[:-2] + str(int(new_f[-2]) + 1) + new_f[-1]

                        new_fields.append(new_f)

                    best, res = cls.get_minimax_result(1 if player == 2 else 2, new_fields, level - 1, False)
                    if res > max:
                        max = res
                        max_combo = combo

                return max_combo, max
            else:
                min = 10000
                min_combo = ''

                for combo in combinations:
                    old = combo.split(' ')[0].strip()
                    new = combo.split(' ')[1].strip()
                    build = combo.split(' ')[2].strip()

                    new_fields = []

                    for field in fields:
                        new_f = field

                        if field[0] + field[1] == old:
                            new_f = new_f[:-1] + '0'
                        if field[0] + new_f[1] == new:
                            new_f = new_f[:-1] + str(player)
                        if field[0] + field[1] == build:
                            new_f = new_f[:-2] + str(int(new_f[-2]) + 1) + new_f[-1]

                        new_fields.append(new_f)

                    best, res = cls.get_minimax_result(1 if player == 2 else 2, new_fields, level - 1)
                    if res < min:
                        min = res
                        min_combo = combo

                return min_combo, min

    @classmethod
    def static_eval_func(cls, player, fields, exam_move_field, exam_build_field, maximizer=True):

        m = int(cls.find_field(fields, exam_move_field)[3]) + 1
        l = int(cls.find_field(fields, exam_build_field)[3]) + 1
        # pomnožen razlikom rastojanja sopstvenih i protivničkih igrača od tog polja

        my_builders = []
        enemy_builders = []
        for field in fields:
            if field[4] == str(player):
                my_builders.append(field[0] + field[1])
            elif field[4] != str(player):
                enemy_builders.append(field[0] + field[1])

        if m == 4:  # Win
            if maximizer:
                return 9999
            else:
                return -9999

        my_dist = 0
        enemy_dist = 0
        for builder in my_builders:
            my_dist += abs(ord(builder[0]) - ord(exam_build_field[0])) + abs(ord(builder[1]) - ord(exam_build_field[1]))
        for builder in enemy_builders:
            enemy_dist += abs(ord(builder[0]) - ord(exam_build_field[0])) + abs(ord(builder[1]) - ord(exam_build_field[1]))

        l *= (my_dist - enemy_dist)

        return m + l

    @classmethod
    def find_field(cls, fields, key):
        for field in fields:
            if field[0] + field[1] == key:
                return field
