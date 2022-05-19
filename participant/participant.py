import random

# ================================================================================= do change anything in this code
class Participant:
    def __init__(self, name, team_num):
        self.name = name                        # [str]   your team name
        self.team_num = team_num                # [int]   your team number
        self.__round = 0                        # [int]   for all games
        self.__turn = False                     # [bool]  for all games     ->  True: starter / False: follower
        self.__statement = True                 # [bool]  for marble game   ->  True: odd / False: even
        self.__previous_records = {}            # [dict]  for glass_stepping_stones game
        self.__previous_player = ''             # [str]   for glass_stepping_stones game
        self.__previous_step_result = []        # [list]  for glass_stepping_stones game
        self.__position = 0                     # [int]   for glass_stepping_stones game
        self.__side = False                     # [bool]  for tug_of_war game ->  True: left / False: right
        self.__condition = True                 # [bool]  for tug_of_war game ->  True: standing / False: falling down
        self.__tug_weight = 0.0                 # [float] for tug_of_war game
        self.__tug_strength = 0.0               # [float] for tug_of_war game
        self.__tug_avg_height = 0.0             # [float] for tug_of_war game
        self.__tug_avg_tugging_length = 0.0     # [float] for tug_of_war game

    # ================================================================================= for all games
    def initialize_player(self, string):
        # you can override this method in this sub-class
        # this method must contain 'self.initialize_params()' which is for initializing some essential variables
        # you can initialize what you define
        self.initialize_params()
    # ================================================================================= for all games

    # ================================================================================= for marble game
    def bet_marbles_strategy(self, playground_marbles):
        # you can override this method in your sub-class
        # you can refer to an object of 'marbles', named as 'playground_marbles'
        # the return should be the number of marbles bet (> 0)!
        my_current_marbles = playground_marbles.get_num_of_my_marbles(self)
        return random.randint(playground_marbles.MIN_HOLDING, my_current_marbles)

    def declare_statement_strategy(self, playground_marbles):
        # you can override this method in your sub-class
        # you can refer to an object of 'marbles', named as 'playground_marbles'
        # the return should be True or False!
        answer = bool(random.randint(0, 1))
        return self.set_statement(answer)
    # ================================================================================= for marble game


    # ================================================================================= for glass_stepping_stones game
    def step_toward_goal_strategy(self, playground_glasses):
        # you can override this method in your sub-class
        # you can refer to an object of 'glass_stepping_stones', named as 'playground_glasses'
        # the return should be 0 or 1 (int)!
        return random.randint(0, 1)
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
        return (2, 3, 4, 1)

    def act_tugging_strategy(self, playground_tug_of_war):
        # you can override this method in this sub-class
        # you can refer to an object of 'tug_of_war', named as 'playground_tug_of_war'
        # the return should be a float value in [0, 100]!
        # note that the float represents a stamina-consuming rate for tugging
        return random.randint(0, 100)
    # ================================================================================= for tug_of_war game


    # ================================================================================= do not override anything
    def initialize_params(self):
        self.set_turn(False)
        self.set_statement(True)
        self.replace_previous_records({})
        self.set_previous_player('')
        self.replace_previous_step_result([])
        self.set_position(0)
        self.set_side(False)                   
        self.set_condition(True)

    def configurate_members(self, members):
        if self.team_num != 0: # note that '0' represents 'Computer':
            NUM_MEMBERS = 10
        else:
            NUM_MEMBERS = 12
        temp_list = []
        # stat1: weight,
        # stat2: height,
        # stat3: degree of strength (aka 3대 무게)
        statistics = {'ordinary_person': (75, 172, 200),
                      'tall_person': (70, 185, 250),
                      'heavy_person': (110, 162, 300),
                      'strong_person': (78, 165, 450)}
        if sum(members) == NUM_MEMBERS:
            temp_list = members
        else:
            temp_list = []
            while sum(temp_list) < NUM_MEMBERS:
                if len(temp_list) < 3:
                    temp_list.append(random.randint(0, NUM_MEMBERS - sum(temp_list)))
                else:
                    temp_list.append(NUM_MEMBERS - sum(temp_list))
            while len(temp_list) < 4:
                temp_list.append(0)

        self.__tug_weight = 0
        self.__tug_avg_height = 0
        self.__tug_strength = 0
        self.__tug_avg_tugging_length = 0
        for num, key in zip(temp_list, statistics):
            self.__tug_weight += num * statistics[key][0]
            self.__tug_avg_height += num * statistics[key][1] / NUM_MEMBERS
            self.__tug_strength += num * 5 * statistics[key][2]
        self.__tug_avg_tugging_length = 0.35 * self.__tug_avg_height

    @property
    def stats(self):
        return (self.__tug_weight, self.__tug_avg_height, self.__tug_strength, self.__tug_avg_tugging_length, self.name)

    @property
    def turn(self):
        return self.__turn

    def set_turn(self, turn):
        self.__turn = turn

    @property
    def side(self):
        return self.__side

    def set_side(self, side):
        self.__side = side

    @property
    def round(self):
        return self.__round

    def set_round(self, round):
        self.__round = round

    @property
    def statement(self):
        return self.__statement

    def set_statement(self, statement):
        self.__statement = statement

    @property
    def position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    @property
    def previous_player(self):
        return self.__previous_player

    def set_previous_player(self, name):
        self.__previous_player = name

    @property
    def previous_records(self):
        return self.__previous_records

    def replace_previous_records(self, dict):
        self.__previous_records = dict

    @property
    def previous_step_result(self):
        return self.__previous_step_result

    def replace_previous_step_result(self, list):
        self.__previous_step_result = list

    @property
    def tug_weight(self):
        return self.__tug_weight

    @property
    def tug_avg_height(self):
        return self.__tug_avg_height

    @property
    def tug_avg_strength(self):
        return self.__tug_strength

    @property
    def tug_avg_tugging_length(self):
        return self.__tug_avg_tugging_length

    def set_condition(self, condition):
        self.__condition = condition
    # ================================================================================= do not override anything


# ================================================================================= do change anything in this code