import random

import gym
from gym import spaces

from hearts_core import *

class HeartsEnv(gym.Env):
    def __init__(self):
        # TODO
        self.observation_space = spaces.Tuple([
            # player states
            spaces.Tuple([
                spaces.Discrete(200), # score
                spaces.Tuple([ # hand
                    spaces.MultiDiscrete([13, 4])
                ] * 13),
                spaces.Tuple([ # income
                    spaces.MultiDiscrete([13, 4])
                ] * 52),
            ] * 4),
            # table states
            spaces.Tuple([
                spaces.Discrete(13), # n_round
                spaces.Discrete(4), # start_pos
                spaces.Discrete(4), # cur_pos
                spaces.Discrete(1), # exchanged
                spaces.Discrete(1), # heart_occured
                spaces.Discrete(100), # n_games
                spaces.Tuple([ # board
                    spaces.MultiDiscrete([13, 4])
                ] * 4),
                spaces.Tuple([ # first_draw
                    spaces.MultiDiscrete([13, 4])
                ]),
                spaces.Tuple([ # bank
                    spaces.Tuple([
                        spaces.MultiDiscrete([13, 4])
                    ] * 3),
                ] * 4)
            ]),
        ])

        self.action_space = spaces.Tuple([
            spaces.Discrete(4), # cur_pos
            spaces.Tuple([ # bank(3) draw(1)
                spaces.MultiDiscrete([13, 4])
            ] * 3),
        ])

    def _pad(self, l, n, v):
        if (not l) or (l is None):
            l = []
        return l + [v] * (n - len(l))


    # TODO
    def step(obs):
        return cur_obs, reward, isfinish, info

    # XXX ...strange I fell confused about the return type
    # What type is for MultiDiscrete XXX
    def _get_current_state(self):
        player_states = []
        for idx, player in enumerate(self._table.players):
            player_features = [
                int(player.score),
            ]
            
            player_hand = player.hand
            self._pad(player_hand, 13, (-1, -1))

            player_income = player.income
            self._pad(player_income, 52, (-1, -1))

            # Tuple: [int], ([r, s], [r, s], ...), ([r, s], [r, s], ...)
            player_states.append((player_features, player_hand, player_income))

        table_states = [
            int(self._table.n_round),
            int(self._table.start_pos)
            int(self._table.cur_pos),
            int(self._table.exchange),
            int(self._table.heart_occur),
            int(self._table.n_games),
        ]

        boards = []
        for card in self._table.board:
            if card:
                boards.append(card)
            else:
                boards.append((-1, -1))

        first_draw = self._table.first_draw if self._table.first_draw else (-1, -1)

        banks = []
        for cards in self._table.bank:
            bank = cards
            self._pad(bank, 3, (-1, -1))
            banks.append(tuple(bank))

        table_states.append(boards, first_draw, banks)

        return (tuple(player_states), tuple(table_states))

    def reset(self):
        self._table = Table()
        return self._get_current_state()

