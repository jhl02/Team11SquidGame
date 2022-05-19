import random
import time
import matplotlib.pyplot as plt

class marbles():
    _NO_MARBLES = 100
    _MAX_HOLDING = 100
    _MIN_HOLDING = 1
    _marbles_in_hand = 0
    _round = 0

    def __init__(self, players):
        self.__TEAM_NUM = players[1].team_num # *** This line is for examining your team score
        self.__player_marble = {players[0].name: 50, players[1].name: 50}

        # ===== for plotting
        self.fig = plt.figure()
        self.fig.suptitle('Odds and Evens')
        self.ax = self.fig.add_subplot()
        self.ax.set_xlabel('Marbles')
        self.ax.bar([players[0].name, players[1].name],
                     [self.__player_marble[players[0].name], self.__player_marble[players[1].name]],
                     color=['red', 'blue'])
        self.fig.canvas.draw()
        #plt.show(block=False)
        # ===== for plotting

    def check_num_of_marbles(self):
        if sum(self.__player_marble.values()) + self._marbles_in_hand == self._NO_MARBLES:
            return True
        else:
            print(" □ : 구슬 수에 문제가 발생했습니다.")
            with open('result_term_project.csv', 'a') as f: # the file name may change
                # team_num, game, win, defeat, violation, error
                f.writelines(str(self.__TEAM_NUM) + ', marble, 0, 0, 1, 0, 구슬 수에 문제가 발생했습니다.\n')
                f.close()
            return False

        #print(" □ : The player failed to prepare the next step")

    def gamble_marbles(self, players):
        for player in sorted(players, key=lambda x: x.turn, reverse=True):
            if player.turn: # for the questioner
                # ============================== place a bet
                bet = player.bet_marbles_strategy(self) # the return should be the number of marbles bet
                error_count = 0
                while bet < 1 or bet > self.get_num_of_my_marbles(player):
                    if error_count > 2:
                        bet = random.randint(1, self.get_num_of_my_marbles(player))
                        print(" □ : 구슬 배팅에 문제가 발생했습니다.")
                        if player.name != "Computer":
                            with open('result_term_project.csv', 'a') as f:  # the file name may change
                                # team_num, game, win, defeat, violation, error
                                f.writelines(str(self.__TEAM_NUM) + ', marble, 0, 0, 1, 0, 배팅에 문제가 발생했습니다. \n')
                                f.close()
                        break
                    bet = player.bet_marbles_strategy(self)
                    error_count += 1

                self._marbles_in_hand = bet
                self.__player_marble[player.name] -= bet
                # ==============================

                if self.check_num_of_marbles():
                    print(" □ : '{}'가 구슬을 배팅했습니다. ({}개, {})".format(player.name, bet, self.odd_and_even(bet)))

                    pass
                    # return True
                else:
                    print(" □ : '{}'의 구슬 계산에 문제가 생겼습니다.".format(player.name))
                    return False

            else: # for the answer
                # ============================== place statement for the bet
                player.declare_statement_strategy(self) # the return should be 'True(홀)' or 'False(짝)'
                # ==============================
                if isinstance(player.statement, bool):
                    print(" □ : '{}'가 '{}'을 외쳤습니다.".format(player.name, self.odd_and_even(player.statement)))
                    time.sleep(0.5)
                    pass
                    # return True
                else:
                    print(" □ : '{}'의 홀짝 선언에 문제가 생겼습니다.".format(player.name))
                    if player.name != "Computer":
                        with open('result_term_project.csv', 'a') as f:  # the file name may change
                            # team_num, game, win, defeat, violation, error
                            f.writelines(str(self.__TEAM_NUM) + ', marble, 0, 0, 1, 0, 홀짝 선언에 문제가 생겼습니다.\n')
                            f.close()
                    return False

    def check_result(self, players):
        for player in players:
            if not player.turn:
                if player.statement == self._marbles_in_hand % 2:
                    return True # if the opposite player get the answer right
                else:
                    return False # if the opposite player failed to the right answer

    def pay_out(self, players):
        result = self.check_result(players)
        bet = self._marbles_in_hand
        round_winner = ''
        round_loser = ''
        winner = ''
        loser = ''

        test1 = sorted(players, key=lambda x: x.turn, reverse=True)
        for player in sorted(players, key=lambda x: x.turn, reverse=True):
            if player.turn: # for the questioner
                if result: # if the player lost the round
                    round_loser = player.name
                else:
                    self.__player_marble[player.name] += 2 * bet
                    round_winner = player.name
                player.set_turn(False)  # set the next role
            else: # for the answer
                if result: # if the player win the round
                    self.__player_marble[player.name] += bet
                    round_winner = player.name
                else:
                    self.__player_marble[player.name] -= bet
                    round_loser = player.name
                player.set_turn(True)  # set the next role
        self._marbles_in_hand = 0

        if self.check_num_of_marbles():
            print(" □ : '{}'가 '{}'의 구슬 {}개를 획득합니다.".format(round_winner, round_loser, bet))
            print("\n □ : '{}'의 구슬은 {}개, ".format(round_winner, self.__player_marble[round_winner]), end='')
            print("'{}'의 구슬은 {}개입니다.\n".format(round_loser, self.__player_marble[round_loser]))
            time.sleep(0.5)
            time.sleep(0.3)

            names = [x.name for x in players]
            if self.__player_marble[names[0]] < 1:
                loser, winner = names[0], names[1]
            if self.__player_marble[names[1]] < 1:
                loser, winner = names[1], names[0]

            if winner != '':
                print(" □ : 따라서 '{}' 탈락, ".format(loser), end='')
                print("'{}' 통과".format(winner))

                return winner, loser
            else:
                return True
        else:
            print(" □ : 홀짝게임 결과 산출에 문제가 생겼습니다")
            with open('result_term_project.csv', 'a') as f: # the file name may change
                # team_num, game, win, defeat, violation, error
                f.writelines(str(self.__TEAM_NUM) + ', marble, 0, 0, 1, 0, 홀짝게임 결과 산출에 문제가 생겼습니다.\n')
                f.close()
            return False

    def odd_and_even(self, num):
        if num % 2 == 1:
            return '홀'
        else:
            return '짝'

    @property
    def MAX_HOLDING(self):
        return self._MAX_HOLDING

    @property
    def MIN_HOLDING(self):
        return self._MIN_HOLDING

    def get_num_of_my_marbles(self, participant):
        if participant.name in self.__player_marble.keys():
            return self.__player_marble[participant.name]
        else:
            print(" □ : {}(은)는 참가자 목록에 없습니다.".format(participant.name))
            with open('result_term_project.csv', 'a') as f: # the file name may change
                # team_num, game, win, defeat, violation, error
                f.writelines(str(self.__TEAM_NUM) + ', marble, 0, 0, 1, 0, 참가자 목록에 없습니다.\n')
                f.close()
            return False

    def round_goes_by(self, players):
        time.sleep(0.5)
        self._round += 1
        self.gamble_marbles(players)
        time.sleep(0.5)
        return self.pay_out(players)

    def run_game(self, players):
        for player in players:
            player.initialize_player('marbles')
        names = [x.name for x in players]
        self.__player_marble = {players[0].name: 50, players[1].name: 50}
        print(" □ : '{}'와 '{}'가 게임에 참가하였습니다.".format(*names))
        input(" □ : 선공을 정하겠습니다.")
        temp = random.randint(0, 1)
        print(" □ : '{}'가 먼저 홀짝 배팅을 시작합니다.".format(names[temp]))
        players[temp].set_turn(True)
        players[1 - temp].set_turn(False)
        self.draw_frame(players), plt.show(block=False), plt.pause(2)
        start_time = time.time()

        # ===== main procedure
        while True:
            winner_and_loser = self.round_goes_by(players)
            self.draw_frame(players)
            if isinstance(winner_and_loser, tuple):
                break
            if time.time() - start_time > 180:
                print(" □ : 제한시간이 초과하여 게임을 종료합니다.")
                return 'no one'
        winner, loser = winner_and_loser
        # ===== main procedure

        print(" □ : {} 번의 홀짝게임을 통해 {} 참가자가 승리했습니다.\n\n".format(self._round, winner))

        return winner

    def draw_frame(self, players):
        # ===== for plotting
        self.ax.clear()
        self.ax.set_ylim(0, 105)
        self.ax.bar([players[0].name, players[1].name],
                     [self.__player_marble[players[0].name], self.__player_marble[players[1].name]],
                     color=['red', 'blue'])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # ===== for plotting

if __name__ == '__main__':
    pass
