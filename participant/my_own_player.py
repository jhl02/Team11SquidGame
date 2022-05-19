import random
from . import participant as part
import copy


class my_own_player(part.Participant):
    def __init__(self):
        super().__init__('name of your team', 'team num')
        # you can change everything in this code file!!
        # also, you can define your own variables here or in the overriding method
        # Any modifications are possible if you follows the rules of Squid Game


    # ====================================================================== for initializing your player every round
    def initialize_player(self, string):
        # you can override this method in this sub-class
        # this method must contain 'self.initialize_params()' which is for initializing some essential variables
        # you can initialize what you define
        self.initialize_params()
    # ====================================================================== for initializing your player every round


    # ================================================================================= for marble game
    def bet_marbles_strategy(self, playground_marbles):
        # you can override this method in this sub-class
        # you can refer to an object of 'marbles', named as 'playground_marbles'
        # the return should be the number of marbles bet (> 0)!
        my_current_marbles = playground_marbles.get_num_of_my_marbles(self)
        return random.randint(playground_marbles.MIN_HOLDING, my_current_marbles)

    def declare_statement_strategy(self, playground_marbles):
        # you can override this method in this sub-class
        # you can refer to an object of 'marbles', named as 'playground_marbles'
        # the return should be True or False!
        answer = bool(random.randint(0, 1))
        return self.set_statement(answer)
    # ================================================================================= for marble game


    # ================================================================================= for glass_stepping_stones game
    def step_toward_goal_strategy(self, playground_glasses):
        # you can override this method in this sub-class
        # you can refer to an object of 'glass_stepping_stones', named as 'playground_glasses'
        # the return should be 0 or 1 (int)!
        if self.position == 0:
            self.temp_list = copy.deepcopy(playground_glasses._players_steps)  # 상대방것도 복사
        length = len(self.temp_list)
        if self.previous_player != 'None' and self.temp_list != []:
            if self.position < length - 1:  # 카피 한 것보다 앞에 있으면
                print(self.temp_list)
                # print('chk1')
                return self.temp_list[self.position]  # 내가 갔던 곳으로
            else:
                if self.position == length - 1:
                    # print('chk2')
                    if self.temp_list[self.position] == 0:
                        return 1
                    else:
                        return 0
                else:
                    # print('chk3')
                    return random.randint(0, 1)
        return 'error'
    # ================================================================================= for glass_stepping_stones game


    # ================================================================================= for tug_of_war game
    def gathering_members(self):
        # you can override this method in this sub-class
        # this method gathers your members for the tug of war game
        # you only can change the configuration of the numbers of person types
        # there are 4 types of persons
        # type1 corresponds a ordinary person who has standard stats for the game
        # type2 corresponds a person with great height
        # type3 corresponds a person with a lot of weight
        # type4 corresponds a person with strong power
        # the return should be a tuple with size of 4, and the sum of the elements should be 10
        # only for computer, it is allowed to set 12 members
        return (0, 0, 5, 5)

    def act_tugging_strategy(self, playground_tug_of_war):
        # you can override this method in this sub-class
        # you can refer to an object of 'tug_of_war', named as 'playground_tug_of_war'
        # the return should be a float value in [0, 100]!
        # note that the float represents a stamina-consuming rate for tugging
        if playground_tug_of_war.player_condition['Computer'] == False:
            if playground_tug_of_war.player_expression[self.name] in ['best', 'well']:
                return 15
            else:
                return 10
        else:
            if playground_tug_of_war.player_expression['Computer'] in ['best', 'well']:
                return 0
            else:
                if playground_tug_of_war.player_expression[self.name] in ['best', 'well']:
                    return 30 + random.randint(0, 3)
                else:
                    return random.randint(0, 3)
    # ================================================================================= for tug_of_war game