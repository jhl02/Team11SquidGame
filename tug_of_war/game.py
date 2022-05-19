import time
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D

class Map():
    __STATIC_FRICTION = (0, 0)      # coefficient of static friction
    __KINETIC_FRICTION = (0, 0)     # coefficient of kinetic friction
    __GRAVIT_ACCEL = 9.8            # meter per sec. squared

    def __init__(self, goal_length, type='glass'):
        self.__TEAM_NUM = 0
        self.__mat_type = type
        self.__GOAL = goal_length
        self.update_coefficient()
        self.__flag_position = 0.0
        self.__is_end = False
        self.__player_names = []
        self.__player_stamina = [100.0, 100.0] # [full stamina(100) for left player, full stamina(100) for right player]
        self.__player_condition = [True, True] # [standing_condition(True), standing_condition(True)]
        self.__dragged_distance = [0.0, 0.0] # dragged distance after someone falls down
        self.__lying_time = [0.0, 0.0] # time after someone falls down
        self.__player_weight = [0.0, 0.0]
        self.__player_height = [0.0, 0.0]
        self.__player_strength = [0.0, 0.0]
        self.__player_tugging_range = [0.0, 0.0]
        self.__time_interval = 1.0 # sec
        self.__velocity = 0 # meter/sec

        # ===== for plotting
        self.fig = plt.figure()
        self.fig.suptitle('Tug of War')
        self.x = np.array([0.0])
        self.y = np.array([0.0])
        self.ax1 = self.fig.add_subplot(2, 1, 1)
        self.ax1.set_ylabel('Flag')
        self.line1 = Line2D([], [], color='black')
        self.line1a = Line2D([], [], color='green', linewidth=2)
        self.line1e = Line2D([], [], color='green', marker='o', markeredgecolor='green')
        self.line2 = Line2D([], [], color='red', linewidth=3)
        self.line3 = Line2D([], [], color='blue', linewidth=3)
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1a)
        self.ax1.add_line(self.line1e)
        self.ax1.add_line(self.line2)
        self.ax1.add_line(self.line3)
        self.ax1.set_ylim(-self.__GOAL - 0.1, self.__GOAL + 0.1)
        self.ax1.set_xlim(min(self.x) - 0.1, max(self.x) + 2.1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)
        self.ax2.set_xlabel('Stamina and Condition')
        self.colors = {True: "green", False: "yellow"}
        self.fig.canvas.draw()
        #plt.show(block=False)
        # ===== for plotting

    def update_coefficient(self):
        type_list = OrderedDict(
            {'teflon-asphalt': (0.5, 0.5), 'teflon-sand': (0.15, 0.15), 'teflon-glass': (0.03, 0.03),
             'teflon-steel': (0.04, 0.04), 'rubber-asphalt': (1.0, 0.7),
             'rubber-sand': (0.25, 0.25), 'rubber-glass': (2.5, 2.0), 'rubber-steel': (0.6, 0.5)
             })
        if self.__mat_type in ['asphalt', 'sand', 'glass', 'steel']:
            i = 0
            for atuple in zip(*[value for key, value in type_list.items() if self.__mat_type in key]):
                if i == 0:
                    self.__STATIC_FRICTION = atuple
                    i += 1
                else:
                    self.__KINETIC_FRICTION = atuple
            return True
        else:
            return False

    def change_mat(self, type):
        if self.__mat_type in ['asphalt', 'sand', 'glass', 'steel']:
            self.__mat_type = type
            return self.update_coefficient()
        else:
            return False

    def calculate_distance(self, condition, weight, abs_force, direction):
        acceleration = 0
        condition_id = int(condition)
        kinetic_f_force = 0.2 * weight * self.__GRAVIT_ACCEL * self.__KINETIC_FRICTION[condition_id]
        static_f_force = 0.2 * weight * self.__GRAVIT_ACCEL * self.__STATIC_FRICTION[condition_id]
        t = 0.2
        if self.__velocity != 0:
            self.__velocity = round(1.1 * self.__velocity, 4)
            if self.__velocity/abs(self.__velocity) == direction:
                if kinetic_f_force < abs_force:
                    temp = abs_force - kinetic_f_force  # calculate force - kinetic friction
                    acceleration = temp / sum(self.__player_weight)  # calculate the acceleration
                    self.__velocity += direction * acceleration * t
                distance = self.__velocity * 1 + (1 / 2) * direction * acceleration * t * t
            else: # the directions of the net force and the velocity are different
                self.__velocity = 0
                if static_f_force < abs_force:
                    temp = abs_force - static_f_force  # calculate force - kinetic friction
                    acceleration = temp / sum(self.__player_weight)  # calculate the acceleration
                    self.__velocity += direction * acceleration * t
                distance = self.__velocity * 1 + (1 / 2) * direction * acceleration * t * t
        else: # if the velocity is equal to 0
            if static_f_force < abs_force:
                temp = abs_force - static_f_force  # calculate force - kinetic friction
                acceleration = temp / sum(self.__player_weight)  # calculate the acceleration
                self.__velocity += direction * acceleration * t
            distance = self.__velocity * 1 + (1 / 2) * direction * acceleration * t * t
        return distance

    def simulate_players_action(self, left_player_rate, right_player_rate, *args):
        consume_rate = [left_player_rate, right_player_rate] # % unit
        forces = [(left_player_rate / 100) * self.__player_strength[0],
                  (right_player_rate/ 100) * self.__player_strength[1]]
        leading_player = ''         # the leading player represents a player with strong pulling power this turn
        following_player = ''       # the following player represents a player with weak pulling power this turn
        message = ['왼쪽', '오른쪽']
        direction = 0
        directions = [-1, 1]

        # ===== consume player's stamina
        for i in range(2):
            if forces[i] >= 0:
                if self.__player_stamina[i] >= 0:
                    if consume_rate[i] > self.__player_stamina[i]:  # if a player has little stamina
                        forces[i] = (self.__player_stamina[i] / 100) * self.__player_strength[i]
                        self.__player_stamina[i] = 0  # then the consumption rate should be the remnant
                        # correspondingly, the player's force is reduced
                    else:
                        self.__player_stamina[i] -= consume_rate[i]
                else:
                    forces[i] = 0.0
                    self.__player_stamina[i] = 0
            else:
                print(" □ : 참가자 전략에 문제가 생겼습니다.\n")
                with open('result_term_project.csv', 'a') as f:  # the file name may change
                    # team_num, game, win, defeat, violation, error
                    f.writelines(str(self.__TEAM_NUM) + 'tug, 0, 0, 1, 0, 참가자 전략에 문제가 생겼습니다.\n')
                    f.close()
                forces[i] = 0.0

        for i in range(2):
            if self.__player_condition[i] == True:  # if a player is standing
                pass  # do nothing
            else:  # if a player is down
                if forces[i] > 0:
                    forces[i] /= 8.0
                # then the player's force to the opponent is reduced
            self.__player_stamina[i] += 5
            if self.__player_stamina[i] > 100:
                self.__player_stamina[i] = 100

        # ===== calculate the net force
        net_force = - forces[0] + forces[1]     # note that the negative represents left direction
        if net_force != 0:
            direction = net_force / abs(net_force)
        else:
            direction = 1
        scalar = abs(net_force)
        if net_force < 0:
            leading_player, following_player = 0, 1
        elif net_force > 0:
            leading_player, following_player = 1, 0
        else:
            # ===== update players' standing conditions
            for i in range(2):
                if self.__player_condition[i] == False:
                    if self.__lying_time[i] > 3:
                        self.__player_condition[i] = True
                        self.__dragged_distance[i] = 0.0
                        self.__lying_time[i] = 0.0
                        print(" □ : {} 참가자가 일어났습니다.".format(message[i]))
                        # if the player has been down for 4 sec.
                        # then the following player will stand up
                    else:
                        self.__lying_time[i] += 1.0

            # ===== update the position of the flag
            print(" □ : 깃발이 멈췄습니다.")

            # ===== for plotting
            self.x = np.append(self.x, max(self.x) + self.__time_interval)
            self.y = np.append(self.y, self.__flag_position)
            self.draw_frame()
            # ===== for plotting
            return True

        distance = self.calculate_distance(self.__player_condition[following_player],
                                         self.__player_weight[following_player],
                                         abs(net_force), direction)


        # ===== update players' standing conditions
        if distance != 0:
            if directions[leading_player] < 0:
                if distance < directions[leading_player] * self.__player_tugging_range[leading_player] / 100 and \
                        self.__player_condition[leading_player] == True:  # cm -> m
                    self.__player_condition[leading_player] = False # let the leading player fall down
                    self.__velocity = 0
                    # if the distance longer than the leading player's tugging range (height * 0.35),
                    # then the leading player will fall down
                    print(" □ : {} 참가자가 넘어졌습니다.".format(message[leading_player]))
                    distance /= 10
                    distance += directions[leading_player] * self.__player_tugging_range[leading_player] / 100
                    # correspondingly, the distance is regulated
            else:
                if distance > directions[leading_player] * self.__player_tugging_range[leading_player] / 100 and \
                        self.__player_condition[leading_player] == True:  # cm -> m
                    self.__player_condition[leading_player] = False
                    self.__velocity = 0
                    # if the distance longer than the leading player's tugging range (height * 0.35),
                    # then the leading player will fall down
                    print(" □ : {} 참가자가 넘어졌습니다.".format(message[leading_player]))
                    distance /= 10
                    distance += directions[leading_player] * self.__player_tugging_range[leading_player] / 100
                    # correspondingly, the distance is regulated

            if self.__player_condition[following_player] == False:
                if directions[leading_player] == abs(distance) / distance:
                    self.__dragged_distance[following_player] /= 1.05  # the dragged distance is shrunken over time
                    self.__dragged_distance[following_player] += abs(distance)
                    # this calculation makes the leading player's dragging longer if the player forces appropriately
                    self.__lying_time[following_player] += 0.125
                    if self.__dragged_distance[following_player] > 1.5 * self.__player_height[leading_player] / 100:  # cm -> m
                        self.__player_condition[following_player] = True
                        self.__dragged_distance[following_player] = 0.0
                        self.__lying_time[following_player] = 0.0
                        print(" □ : {} 참가자가 일어났습니다.".format(message[following_player]))
                    # if the distance dragged after the player falls down longer than a certain range (1.5 * height),
                    # then the following player will stand up
        for i in range(2):
            if self.__player_condition[i] == False:
                if self.__lying_time[i] > 3:
                    self.__player_condition[i] = True
                    self.__dragged_distance[i] = 0.0
                    self.__lying_time[i] = 0.0
                    print(" □ : {} 참가자가 일어났습니다.".format(message[i]))
                    # if the player has been down for 4 sec.
                    # then the following player will stand up
                else:
                    self.__lying_time[i] += 1.0


        # ===== update the position of the flag
        if distance < 0:
            print(" □ : 깃발이 왼쪽으로 {0:.2f}m 움직였습니다.".format(abs(distance)))
        elif distance == 0:
            print(" □ : 깃발이 멈췄습니다.")
        else:
            print(" □ : 깃발이 오른쪽으로 {0:.2f}m 움직였습니다.".format(abs(distance)))
        self.__flag_position += distance

        # ===== for plotting
        self.x = np.append(self.x, max(self.x) + self.__time_interval)
        self.y = np.append(self.y, self.__flag_position)
        self.draw_frame()
        # ===== for plotting

        pass

    def is_reached(self):
        if self.__flag_position < -1 * self.__GOAL:
            return -1       # left-side player won
        elif self.__GOAL < self.__flag_position:
            return 1        # right-side player won
        return False            # no one won

    def initialize_player_stats(self, left_player_stats, right_player_stats):
        self.__flag_position = 0.0
        self.__dragged_distance = [0.0, 0.0]
        self.__player_stamina = [100.0, 100.0]
        self.__player_weight[0] = left_player_stats[0]
        self.__player_weight[1] = right_player_stats[0]
        self.__player_height[0] = left_player_stats[1]
        self.__player_height[1] = right_player_stats[1]
        self.__player_strength[0] = left_player_stats[2]
        self.__player_strength[1] = right_player_stats[2]
        self.__player_tugging_range[0] = left_player_stats[3]
        self.__player_tugging_range[1] = right_player_stats[3]
        self.__player_names = []
        self.__player_names.append(left_player_stats[4])
        self.__player_names.append(right_player_stats[4])

        # ===== for plotting
        if self.__player_names[0] == 'Computer':
            self.line2.set_data([0, 1000], [-self.goal, -self.goal])
            self.line3.set_data([0, 1000], [self.goal, self.goal])
        else:
            self.line2.set_data([0, 1000], [self.goal, self.goal])
            self.line3.set_data([0, 1000], [-self.goal, -self.goal])
        plt.show(block=False)
        plt.pause(2)
        # ===== for plotting


    def draw_frame(self):
        # ===== for plotting
        i = len(self.x)
        head = i - 1
        self.line1.set_data(self.x[:i], self.y[:i])
        self.line1a.set_data(self.x[head - min(i, 3) + 1:head + 1], self.y[head - min(i, 3) + 1:head + 1])
        self.line1e.set_data(self.x[head], self.y[head])
        self.ax1.set_xlim(min(self.x) - 0.1, max(self.x) + 2.1)
        self.ax2.clear()
        self.ax2.set_ylim(0, 105)
        self.ax2.bar(self.__player_names, self.__player_stamina,
                                  color=[self.colors[x] for x in self.__player_condition])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # ===== for plotting

    @property
    def goal(self):
        return self.__GOAL

    @property
    def mat_type(self):
        return self.__mat_type

    @property
    def flag_position(self):
        return self.__flag_position

    @property
    def player_stamina(self):
        return self.__player_stamina

    @property
    def player_condition(self):
        return self.__player_condition

    def set_TEAM_NUM(self, num):
        self.__TEAM_NUM = num


class tug_of_war():
    __running_time = 0.0
    __recent_flag_position = 0.0

    def __init__(self, a_map, players):
        self.ground = a_map
        self.mat_type = a_map.mat_type
        self.names = [x.name for x in players]
        self.__TEAM_NUM = players[1].team_num # *** This line is for examining your team score
        self.__GOAL = a_map.goal
        self.__player_expression = {}
        self.__player_stamina = {players[0].name: 100.0, players[1].name: 100.0}
        self.__player_condition = {}
        self.__time_interval = 1.0 # sec.

    def let_player_do(self, players, a_map):
        # ===== initialize variables
        left_player = ''
        right_player = ''

        # ===== check player's position
        if players[0].side == players[1].side:
            print(" □ : 참가자 부정행위가 적발되었습니다.\n")
            with open('result_term_project.csv', 'a') as f: # the file name may change
                # team_num, game, win, defeat, violation, error
                f.writelines(str(players[1].team_num) + 'tug, 0, 0, 1, 0\n')
                f.close()
            print(" □ : 임의로 자리를 다시 배정하겠습니다.\n")
            temp = random.randint(0, 1)
            print(" □ : '{}'가 왼쪽, '{}'가 오른쪽에서 줄다기리 게임을 다시 시작합니다.".format(self.names[temp], self.names[1 - temp]))
            players[temp].set_side(False)
            players[1 - temp].set_side(True)
            a_map.initialize_player_stats(players[temp].stats, players[1 - temp].stats)
        if players[0].side == False:
            left_player, right_player = players[0], players[1]
        else:
            left_player, right_player = players[1], players[0]

        # ===== simulate players' actions
        time.sleep(0.05)
        self.__running_time += self.__time_interval
        stamina1 = left_player.act_tugging_strategy(self)
        stamina2 = right_player.act_tugging_strategy(self)
        a_map.simulate_players_action(stamina1, stamina2, self.change_mat(a_map))

        # update player's info
        temp = {0: left_player.name, 1: right_player.name}
        index = 0
        for value in a_map.player_stamina:
            self.__player_expression[temp[index]] = self.figure_out_face_expression(value)
            index += 1
        index = 0
        for value in a_map.player_condition:
            self.__player_condition[temp[index]] = value
            for i in range(2):
                if players[i].name == temp[index]:
                    players[i].set_condition(value)
            index += 1

        # update the position of the flag
        self.__recent_flag_position = a_map.flag_position

        # update info
        if a_map.is_reached():
            return False
        else:
            return True

    def run_game(self, players, a_map):
        for player in players:
            player.initialize_player('tugging')
        winner = ''
        loser = ''
        print(" □ : '{}'와 '{}'가 게임에 참가하였습니다.".format(*self.names))
        for player in players:
            player.configurate_members(player.gathering_members())
        input(" □ : 위치를 정하겠습니다.")
        temp = random.randint(0, 1)
        print(" □ : '{}'가 왼쪽, '{}'가 오른쪽에서 줄다기리 게임을 시작합니다.".format(self.names[temp], self.names[1 - temp]))
        players[temp].set_side(False)
        players[1 - temp].set_side(True)
        a_map.initialize_player_stats(players[temp].stats, players[1 - temp].stats)
        a_map.set_TEAM_NUM(self.__TEAM_NUM)

        for name in self.names:
            self.__player_condition[name] = True
            self.__player_expression[name] = 'best'
        self.__recent_flag_position = 0
        start_time = time.time()

        # ===== main procedure
        while self.let_player_do(players, a_map):
            if time.time() - start_time > 180:
                print(" □ : 제한시간이 초과하여 게임을 종료합니다.")
                break
        # ===== main procedure

        if a_map.flag_position < 0:
            if players[0].side == False:
                winner, loser = players[0].name, players[1].name
            else:
                winner, loser = players[1].name, players[0].name
        elif a_map.flag_position > 0:
            if players[0].side == True:
                winner, loser = players[0].name, players[1].name
            else:
                winner, loser = players[1].name, players[0].name
        else:
            winner = players[1].name

        print(" □ : 줄다리기 게임을 통해 {} 참가자가 승리했습니다. (경기시간: {})\n\n".format(winner, self.__running_time))
        time.sleep(5)
        return winner

    @property
    def player_expression(self):
        return self.__player_expression

    @property
    def player_condition(self):
        return self.__player_condition

    @property
    def flag_position(self):
        return self.__recent_flag_position

    def change_mat(self, a_map):
        return a_map.change_mat(self.mat_type)

    def get_player_own_stamina(self, player):
        return self.__player_stamina[player.name]

    def initialize_player_stamina(self):
        for player in self.__player_stamina:
            self.__player_stamina[player] = 100

    def figure_out_face_expression(self, stamina_value):
        if stamina_value > 90:
            return 'best'
        elif stamina_value > 70:
            return 'well'
        elif stamina_value > 40:
            return 'good'
        elif stamina_value > 10:
            return 'bad'
        else:
            return 'worst'