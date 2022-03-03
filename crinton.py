import sys
from random import shuffle
import collections
from math import sqrt
import numpy as np
from crinton_strategy import *

def build_new_deck() -> list:
	new_deck = [i+1 for i in range(13)]*4
	np.random.shuffle(new_deck)
	return collections.deque(new_deck)

def ev(pw: float, pl: float) -> float:
	return 3.0*pw + pl - 2.0

def payoff(left: int, right: int, middle: int, chips: int, pot: int, bet: int) -> tuple:
	if middle < left or middle > right:
		return chips - bet, pot + bet
	elif middle > left and middle < right:
		return chips + bet, pot - bet
	else:
		return chips - (2 * bet), pot + (2 * bet)

def play_game(ante: int, number_of_players: int, strategy: list, max_loss: int, verbose=False) -> tuple:
	deck = build_new_deck()
	card_count = collections.Counter(deck)
	pot = ante * number_of_players
	chips = [-ante]*number_of_players
	current_player = 0
	hand_count = [0]*number_of_players
	min_bet_count = [0]*number_of_players

	if verbose: print("***** New Hand *****")
	while pot > 0:
		all_players_out = True
		player = 0
		while all_players_out and player < number_of_players:
			if chips[player] > -max_loss + 1:
				all_players_out = False
			player += 1
		if all_players_out: return [0.0]*number_of_players, hand_count, min_bet_count
		if chips[current_player] > -max_loss + 1:
			if len(deck) == 4:
				if verbose: print("*shuffle*")
				deck = build_new_deck()
				card_count = collections.Counter(deck)
			left, right = deck.pop(), deck.pop()
			card_count[left] -= 1
			card_count[right] -= 1
			hand_count[current_player] += 1
			if left == 1 and left == right:
				right = 14
			if left > right:
				left, right = right, left
			bet = strategy[current_player](left, right, card_count, chips[current_player], pot, deck, max_loss)
			if bet == 1: min_bet_count[current_player] += 1
			middle = deck.pop()
			card_count[middle] -= 1
			chips[current_player], pot = payoff(left, right, middle, chips[current_player], pot, bet)
			if verbose: print("Player: {}, Left: {} Middle: {} Right: {}, Bet: {}, Chip count: {}, Pot: {}".format(current_player, left, middle, right, bet, chips, pot))
			if pot == 0:
				return chips, hand_count, min_bet_count
		current_player = (current_player + 1) % number_of_players

def display_results(total_hand_count: dict, number_of_games: int, number_of_players: int, strategy: list, win_per_game: list, win_per_hand: list, min_result: list, max_result: list, ante: int, min_bet_count: list) -> None:
	print("Ante:   {}\tTotal hand counts: {}\t Runs: {}".format(ante, total_hand_count, number_of_games))
	for player in range(number_of_players):
		print("Player: {}\tStrategy: {} \tChips won per game: {:.3f}\tChips won per hand: {:.4f}\tMin, Max: ({},{})\tMin bet %: {:.3f}".format(player, strategy[player].__name__ , win_per_game[player], win_per_hand[player], min_result[player], max_result[player], 1.0*min_bet_count[player]/total_hand_count[player]))

def get_strategies(strategies: list) -> list:
	strategy = []
	for e in strategies:
		if e == 'p':
			strategy.append(perfect)
		if e == 'h':
			strategy.append(strategy_home)
		if e == "117":
			strategy.append(fh_11_7)
		if e == "118":
			strategy.append(fh_11_8)
		if e == "127":
			strategy.append(fh_12_7)
		if e == "128":
			strategy.append(fh_12_8)
		if e == "137":
			strategy.append(fh_13_7)
		if e == "138":
			strategy.append(fh_13_8)
	return strategy

def main(ante, number_of_players, number_of_games, max_loss, strategies):
	strategy_list = get_strategies(strategies)
	game_count = 0
	results = {}
	min_result = {player:  999999999 for player in range(number_of_players)}
	max_result = {player: -999999999 for player in range(number_of_players)}
	total_hand_count = {}
	min_bets = [0]*number_of_players

	while game_count < number_of_games:
		game_result, hand_count, min_bet_count = play_game(ante=ante, number_of_players=number_of_players, strategy=strategy_list, max_loss=max_loss, verbose=False)
		for i, e in enumerate(min_bet_count): min_bets[i] += e
		for i, e in enumerate(game_result):
			if e < min_result[i]:
				min_result[i] = e
			if e > max_result[i]:
				max_result[i] = e
			try:
				results[i].append(e)
			except KeyError:
				results[i] = [e]
		game_count += 1
		for i, e in enumerate(hand_count):
			try:
				total_hand_count[i] += e
			except KeyError:
				total_hand_count[i] = e

	win_per_game = [np.mean(v) for v in results.values()]
	win_per_hand = [1.0*sum(results[i])/total_hand_count[i] for i in range(number_of_players)]
	display_results(total_hand_count, number_of_games, number_of_players, strategy_list, win_per_game, win_per_hand, min_result, max_result, ante, min_bets)


if __name__ == "__main__":
	ante, max_loss, number_of_games, *strategies = sys.argv[1:]
	main(int(ante), len(strategies), int(number_of_games), int(max_loss), strategies)


"""
Which position has an advantage?
Ante:   6	Total hand counts: {0: 481199844, 1: 476404771}	 Runs: 10000000
Player: 0	Strategy: perfect	Chips won per game: -1.762	Chips won per hand: -0.0366	Min, Max: (-161,161)
Player: 1	Strategy: perfect	Chips won per game: 1.762	Chips won per hand: 0.0370	Min, Max: (-161,161)

Ante:   6	Total hand counts: {0: 329547567, 1: 326074960, 2: 322894495}	 Runs: 10000000
Player: 0	Strategy: perfect	Chips won per game: 0.170	Chips won per hand: 0.0052	Min, Max: (-161,322)
Player: 1	Strategy: perfect	Chips won per game: -0.095	Chips won per hand: -0.0029	Min, Max: (-161,322)
Player: 2	Strategy: perfect	Chips won per game: -0.076	Chips won per hand: -0.0023	Min, Max: (-161,322)

Ante:   6	Total hand counts: {0: 250819858, 1: 249702508, 2: 248116082, 3: 245257201}	 Runs: 10000000
Player: 0	Strategy: perfect	Chips won per game: -2.456	Chips won per hand: -0.0979	Min, Max: (-161,483)
Player: 1	Strategy: perfect	Chips won per game: -1.368	Chips won per hand: -0.0548	Min, Max: (-161,483)
Player: 2	Strategy: perfect	Chips won per game: 0.339	Chips won per hand: 0.0137	Min, Max: (-161,483)
Player: 3	Strategy: perfect	Chips won per game: 3.485	Chips won per hand: 0.1421	Min, Max: (-161,483)

Ante:   6	Total hand counts: {0: 205411394, 1: 203102824, 2: 201079720, 3: 199172275, 4: 197409095}	 Runs: 10000000
Player: 0	Strategy: perfect	Chips won per game: 0.639	Chips won per hand: 0.0311	Min, Max: (-161,643)
Player: 1	Strategy: perfect	Chips won per game: 0.065	Chips won per hand: 0.0032	Min, Max: (-161,643)
Player: 2	Strategy: perfect	Chips won per game: -0.237	Chips won per hand: -0.0118	Min, Max: (-161,643)
Player: 3	Strategy: perfect	Chips won per game: -0.342	Chips won per hand: -0.0172	Min, Max: (-161,643)
Player: 4	Strategy: perfect	Chips won per game: -0.124	Chips won per hand: -0.0063	Min, Max: (-161,643)

Ante:   6	Total hand counts: {0: 174061098, 1: 172734212, 2: 170679354, 3: 169271457, 4: 167073696, 5: 165894616}	 Runs: 10000000
Player: 0	Strategy: perfect	Chips won per game: -0.679	Chips won per hand: -0.0390	Min, Max: (-161,803)
Player: 1	Strategy: perfect	Chips won per game: 0.897	Chips won per hand: 0.0519	Min, Max: (-161,803)
Player: 2	Strategy: perfect	Chips won per game: -0.569	Chips won per hand: -0.0333	Min, Max: (-161,804)
Player: 3	Strategy: perfect	Chips won per game: 1.164	Chips won per hand: 0.0688	Min, Max: (-161,803)
Player: 4	Strategy: perfect	Chips won per game: -1.085	Chips won per hand: -0.0650	Min, Max: (-161,803)
Player: 5	Strategy: perfect	Chips won per game: 0.272	Chips won per hand: 0.0164	Min, Max: (-161,803)

Ante:   6	Total hand counts: {0: 832580408, 1: 807485518}	 Runs: 50000000
Player: 0	Strategy: strategy_home 	Chips won per game: -0.068	Chips won per hand: -0.0041	Min, Max: (-160,160)	Min bet %: 0.921
Player: 1	Strategy: strategy_home 	Chips won per game: 0.068	Chips won per hand: 0.0042	Min, Max: (-160,160)	Min bet %: 0.921

Ante:   6	Total hand counts: {0: 707482536, 1: 690209140, 2: 673498526}	 Runs: 50000000
Player: 0	Strategy: strategy_home 	Chips won per game: -0.027	Chips won per hand: -0.0019	Min, Max: (-160,320)	Min bet %: 0.921
Player: 1	Strategy: strategy_home 	Chips won per game: 0.024	Chips won per hand: 0.0018	Min, Max: (-160,320)	Min bet %: 0.921
Player: 2	Strategy: strategy_home 	Chips won per game: 0.002	Chips won per hand: 0.0002	Min, Max: (-160,320)	Min bet %: 0.921



Ante:   6	Total hand counts: {0: 112514156, 1: 110439963, 2: 108433652, 3: 106426182, 4: 104487334}	 Runs: 10000000
Player: 0	Strategy: strategy_home 	Chips won per game: 0.055	Chips won per hand: 0.0049	Min, Max: (-160,640)	Min bet %: 0.921
Player: 1	Strategy: strategy_home 	Chips won per game: 0.026	Chips won per hand: 0.0024	Min, Max: (-160,640)	Min bet %: 0.921
Player: 2	Strategy: strategy_home 	Chips won per game: -0.008	Chips won per hand: -0.0008	Min, Max: (-160,640)	Min bet %: 0.922
Player: 3	Strategy: strategy_home 	Chips won per game: -0.043	Chips won per hand: -0.0040	Min, Max: (-160,640)	Min bet %: 0.921
Player: 4	Strategy: strategy_home 	Chips won per game: -0.030	Chips won per hand: -0.0029	Min, Max: (-160,640)	Min bet %: 0.921

"""
