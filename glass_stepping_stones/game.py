import copy
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class Map():
    def __init__(self, num):
        self.__TEAM_NUM = 0
        self.length = num
        self.steps = self.generate_map(num)
        self.__current_position = 0   # 0: the first stone, 2: the second stone, ..., 'length' - 1 : the last stone
        self.__previous_player = ''
        self.__previous_records = {}

        # ===== for plotting
        self.fig = plt.figure()
        self.fig.suptitle('Glass Stepping Stones')
        self.y = np.linspace(1, self.length, self.length)
        self.hard_glasses = np.array([])
        self.weak_glasses = np.array([])
        self.player_point_x = np.array([])
        self.player_point_y = np.array([])
        self.ax1 = self.fig.add_subplot(1, 5, 1)
        self.ax1.set_xlabel('Computer')
        self.line1 = Line2D([], [], color='red')
        self.line1e = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.set_xlim(- 0.1, 1.1)
        self.ax1.set_ylim(- 0.6, self.length + 0.6)
        self.ax2 = self.fig.add_subplot(1, 5, 3)
        self.ax2.set_xlabel('Team')
        self.line2 = Line2D([], [], color='blue')
        self.line2e = Line2D([], [], color='blue', marker='o', markeredgecolor='blue')
        self.ax2.set_xlim(- 0.1, 1.1)
        self.ax2.set_ylim(- 0.6, self.length + 0.6)
        self.fig.canvas.draw()
        #plt.show(block=False)
        # ===== for plotting

    def draw_glasses(self):
        # ===== for plotting
        self.ax1.clear(), self.ax2.clear()
        self.ax1.set_xlim(- 0.1, 1.1)
        self.ax1.set_ylim(- 0.6, self.length + 0.6)
        self.ax1.set_xlabel('Computer')
        self.ax1.scatter(x=self.hard_glasses, y=self.y, c='limegreen', marker='s', s=20)
        self.ax1.scatter(x=self.weak_glasses, y=self.y, c='aquamarine', marker='s', s=20)
        self.ax2.set_xlim(- 0.1, 1.1)
        self.ax2.set_ylim(- 0.6, self.length + 0.6)
        self.ax2.set_xlabel('Team')
        self.ax2.scatter(x=self.hard_glasses, y=self.y, c='limegreen', marker='s', s=20)
        self.ax2.scatter(x=self.weak_glasses, y=self.y, c='aquamarine', marker='s', s=20)
        self.line1.set_data([], []), self.line1e.set_data([], [])
        self.line2.set_data([], []), self.line2e.set_data([], [])
        self.ax1.add_line(self.line1), self.ax1.add_line(self.line1e)
        self.ax2.add_line(self.line2), self.ax2.add_line(self.line2e)
        self.player_point_x = np.array([])
        self.player_point_y = np.array([])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # ===== for plotting

    def draw_traces(self, step, player_name):
        # ===== for plotting
        if self.__current_position == 1:
            self.player_point_x = np.array([0.5, step])
        else:
            self.player_point_x = np.append(self.player_point_x, step)
        self.player_point_y = np.linspace(0, len(self.player_point_x) - 1, len(self.player_point_x))
        i = len(self.player_point_x)
        head = i - 1
        if player_name == 'Computer':
            self.line1.set_data(self.player_point_x[:i], self.player_point_y[:i])
            self.line1e.set_data(self.player_point_x[head], self.player_point_y[head])
        else:
            self.line2.set_data(self.player_point_x[:i], self.player_point_y[:i])
            self.line2e.set_data(self.player_point_x[head], self.player_point_y[head])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # ===== for plotting

    def generate_map(self, num_steps):
        temp = []
        for _ in range(num_steps):
            temp.append(random.randint(0, 1))
        return tuple(temp)

    def initialize_map(self):
        self.steps = self.generate_map(len(self.steps))
        self.__current_position = 0
        self.__previous_player = ''
        self.__previous_records = {}

        # ===== for plotting
        self.y = np.linspace(1, self.length, self.length)
        self.hard_glasses = np.array([])
        self.weak_glasses = np.array([])
        for i in range(self.length):
            if self.steps[i] == 0:
                self.hard_glasses = np.append(self.hard_glasses, 0)
                self.weak_glasses = np.append(self.weak_glasses, 1)
            else:
                self.hard_glasses = np.append(self.hard_glasses, 1)
                self.weak_glasses = np.append(self.weak_glasses, 0)
        self.player_point_x = np.array([])
        self.player_point_y = np.array([])
        self.ax1.clear(), self.ax2.clear()
        self.ax1.set_xlabel('Computer'), self.ax2.set_xlabel('Team')
        self.line1 = Line2D([], [], color='red')
        self.line1e = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.line2 = Line2D([], [], color='blue')
        self.line2e = Line2D([], [], color='blue', marker='o', markeredgecolor='blue')
        self.ax1.set_xlim(- 0.1, 1.1)
        self.ax1.set_ylim(- 0.6, self.length + 0.6)
        self.ax2.set_xlim(- 0.1, 1.1)
        self.ax2.set_ylim(- 0.6, self.length + 0.6)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.show(block=False)
        # ===== for plotting

    def add_position(self):
        self.__current_position += 1
        return True

    def check_goal(self):
        if self.__current_position == self.length:
            return True # the goal reached
        else:
            return False

    @property
    def current_position(self):
        return self.__current_position

    def reset_position(self):
        self.__current_position = 0

    @property
    def previous_player(self):
        return self.__previous_player

    def set_previous_player(self, name):
        self.__previous_player = name

    @property
    def previous_records(self):
        return self.__previous_records

    def set_TEAM_NUM(self, num):
        self.__TEAM_NUM = num

class glass_stepping_stones():
    _players_steps = []
    _round = 0
    record = {}

    def __init__(self, a_map, players):
        self.__TEAM_NUM = players[1].team_num # *** This line is for examining your team score
        self.__NUM_STEPS = a_map.length
        self.players = players
        self.names = [x.name for x in self.players]

    def check_a_stone(self, step, player_name, a_map):

        if step == None :
            print('error')

        if a_map.current_position == 0:
            self._players_steps = []
        self._players_steps.append(step)
        if step == 0:
            print(" □ : 왼쪽을 향합니다.")
        else:
            print(" □ : 오른쪽을 향합니다.")
        if a_map.steps[a_map.current_position] == step:
            a_map.add_position()
            a_map.draw_traces(step, player_name)
            return True
        else:
            a_map.add_position()
            a_map.draw_traces(step, player_name)
            return False

    def let_runner_go(self, a_map):
        a_step = -1
        self._round += 1
        a_map.previous_records[self._round] = {}
        a_map.draw_glasses(), time.sleep(0.05)
        for player in sorted(self.players, key=lambda x: x.turn, reverse=True):
            time.sleep(0.05)
            player.set_previous_player(copy.deepcopy(a_map.previous_player))
            player.set_round = self._round
            print(" □ : '{}'가 출발선에서 징검다리 건너기를 시작합니다.".format(player.name))
            while True:
                time.sleep(0.1)
                a_step = player.step_toward_goal_strategy(self)
                if a_step == None:
                    print('error')
                if self.check_a_stone(a_step, player.name, a_map):
                    if a_map.check_goal():
                        print(" □ : '{}'가 결승점에 도달했습니다.".format(player.name))
                        winner = player.name
                        temp = self.names.copy()
                        temp.remove(player.name)
                        loser = temp[0]
                        return winner, loser
                    else:
                        print(" □ : '{}'가 {}번째 징검다리에 무사히 서있습니다.".format(player.name, a_map.current_position))
                        player.set_position(a_map.current_position)
                        a_map.previous_records[self._round][player.name] = self._players_steps.copy()
                        player.replace_previous_step_result([a_map.current_position - 1, a_step, True])
                else:
                    print(" □ : '{}'가 {}번째 징검다리에서 떨어졌습니다.".format(player.name, a_map.current_position))
                    print(" □ : 따라서 '{}' 탈락.\n".format(player.name))
                    a_map.reset_position()
                    player.set_position(a_map.current_position)
                    a_map.previous_records[self._round][player.name] = self._players_steps.copy()
                    player.replace_previous_step_result([a_map.current_position - 1, a_step, False])
                    break
            a_map.set_previous_player(player.name)
        print(" □ : 참가자 모두 떨어졌으므로 게임을 다시 시작합니다.\n")
        time.sleep(0.2)
        return True


    def run_game(self, a_map):
        for player in self.players:
            player.initialize_player("glass")
            player.replace_previous_records(a_map.previous_records) # this reference should not be replaced once again
        names = [x.name for x in self.players]
        print(" □ : '{}'와 '{}'가 게임에 참가하였습니다.".format(*names))
        if a_map.previous_player == '':
            a_map.set_previous_player('None')
        input(" □ : 선주를 정하겠습니다.")
        temp = random.randint(0, 1)
        print(" □ : '{}'가 먼저 징검다리 건너기를 시작합니다.".format(names[temp]))
        self.players[temp].set_turn(True)
        self.players[1 - temp].set_turn(False)
        a_map.set_TEAM_NUM(self.__TEAM_NUM)
        a_map.initialize_map(), plt.pause(2)
        self._players_steps = []
        start_time = time.time()

        # ===== main procedure
        while True:
            winner_and_loser = self.let_runner_go(a_map)
            if isinstance(winner_and_loser, tuple):
                break
            if time.time() - start_time > 180:
                print(" □ : 제한시간이 초과하여 게임을 종료합니다.")
                return 'no one'
        winner, loser = winner_and_loser
        # ===== main procedure
        print(" □ : {} 번의 징검다리 건너기 게임을 통해 '{}'가 승리했습니다.".format(self._round, winner))

        return winner

    def players_record_update(self, record_dict):
        for player in self.players:
            player.replace_previous_records(record_dict)

if __name__ == '__main__':
    pass
