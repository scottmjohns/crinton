import sys
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
	strategy_space = [perfect, strategy_home, strategy_home2, fh_11_8, fh_12_8, fh_13_8]
	for e in strategies:
		if e == 'r':
			strategy.append(np.random.choice(strategy_space))
		if e == 'p':
			strategy.append(perfect)
		if e == 'h':
			strategy.append(strategy_home)
		if e == 'h2':
			strategy.append(strategy_home2)
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

def main(ante: int, number_of_players: int, number_of_games: int, max_loss: int, strategies: list):
	"""
	Runs the game Crinton a fixed number of times with given strategies, and
	displays the aggregated results.

	Inputs:
	ante: the number of chips anted by each player at the beginning of the game


	"""
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
Ante:   6	Total hand counts: {0: 2405375733, 1: 2382318575}	 Runs: 50000000
Player: 0	Strategy: perfect 	Chips won per game: -1.766	Chips won per hand: -0.0367	Min, Max: (-160,160)	Min bet %: 0.864
Player: 1	Strategy: perfect 	Chips won per game: 1.766	Chips won per hand: 0.0371	Min, Max: (-160,160)	Min bet %: 0.859

Ante:   6	Total hand counts: {0: 1647069886, 1: 1629689380, 2: 1613506871}	 Runs: 50000000
Player: 0	Strategy: perfect 	Chips won per game: 0.178	Chips won per hand: 0.0054	Min, Max: (-160,320)	Min bet %: 0.860
Player: 1	Strategy: perfect 	Chips won per game: -0.097	Chips won per hand: -0.0030	Min, Max: (-160,320)	Min bet %: 0.860
Player: 2	Strategy: perfect 	Chips won per game: -0.081	Chips won per hand: -0.0025	Min, Max: (-160,320)	Min bet %: 0.860

Ante:   6	Total hand counts: {0: 1253631877, 1: 1247948263, 2: 1239936032, 3: 1225678550}	 Runs: 50000000
Player: 0	Strategy: perfect 	Chips won per game: -2.428	Chips won per hand: -0.0968	Min, Max: (-160,480)	Min bet %: 0.865
Player: 1	Strategy: perfect 	Chips won per game: -1.364	Chips won per hand: -0.0547	Min, Max: (-160,480)	Min bet %: 0.860
Player: 2	Strategy: perfect 	Chips won per game: 0.334	Chips won per hand: 0.0135	Min, Max: (-160,480)	Min bet %: 0.858
Player: 3	Strategy: perfect 	Chips won per game: 3.458	Chips won per hand: 0.1411	Min, Max: (-160,480)	Min bet %: 0.853

Ante:   6	Total hand counts: {0: 1026510623, 1: 1014923558, 2: 1004691373, 3: 995399014, 4: 986343295}	 Runs: 50000000
Player: 0	Strategy: perfect 	Chips won per game: 0.641	Chips won per hand: 0.0312	Min, Max: (-160,640)	Min bet %: 0.858
Player: 1	Strategy: perfect 	Chips won per game: 0.061	Chips won per hand: 0.0030	Min, Max: (-160,640)	Min bet %: 0.858
Player: 2	Strategy: perfect 	Chips won per game: -0.256	Chips won per hand: -0.0128	Min, Max: (-160,640)	Min bet %: 0.859
Player: 3	Strategy: perfect 	Chips won per game: -0.334	Chips won per hand: -0.0168	Min, Max: (-160,640)	Min bet %: 0.859
Player: 4	Strategy: perfect 	Chips won per game: -0.112	Chips won per hand: -0.0057	Min, Max: (-160,640)	Min bet %: 0.858


Ante:   6	Total hand counts: {0: 832580408, 1: 807485518}	 Runs: 50000000
Player: 0	Strategy: strategy_home 	Chips won per game: -0.068	Chips won per hand: -0.0041	Min, Max: (-160,160)	Min bet %: 0.921
Player: 1	Strategy: strategy_home 	Chips won per game: 0.068	Chips won per hand: 0.0042	Min, Max: (-160,160)	Min bet %: 0.921

Ante:   6	Total hand counts: {0: 707482536, 1: 690209140, 2: 673498526}	 Runs: 50000000
Player: 0	Strategy: strategy_home 	Chips won per game: -0.027	Chips won per hand: -0.0019	Min, Max: (-160,320)	Min bet %: 0.921
Player: 1	Strategy: strategy_home 	Chips won per game: 0.024	Chips won per hand: 0.0018	Min, Max: (-160,320)	Min bet %: 0.921
Player: 2	Strategy: strategy_home 	Chips won per game: 0.002	Chips won per hand: 0.0002	Min, Max: (-160,320)	Min bet %: 0.921

Ante:   6	Total hand counts: {0: 650090049, 1: 637413819, 2: 624984044, 3: 612561080}	 Runs: 50000000
Player: 0	Strategy: strategy_home 	Chips won per game: -0.058	Chips won per hand: -0.0045	Min, Max: (-160,480)	Min bet %: 0.922
Player: 1	Strategy: strategy_home 	Chips won per game: -0.017	Chips won per hand: -0.0013	Min, Max: (-160,480)	Min bet %: 0.921
Player: 2	Strategy: strategy_home 	Chips won per game: 0.023	Chips won per hand: 0.0019	Min, Max: (-160,480)	Min bet %: 0.921
Player: 3	Strategy: strategy_home 	Chips won per game: 0.052	Chips won per hand: 0.0042	Min, Max: (-160,480)	Min bet %: 0.921

Ante:   6	Total hand counts: {0: 562373371, 1: 552076601, 2: 542097354, 3: 532116427, 4: 522341198}	 Runs: 50000000
Player: 0	Strategy: strategy_home 	Chips won per game: 0.038	Chips won per hand: 0.0034	Min, Max: (-160,640)	Min bet %: 0.921
Player: 1	Strategy: strategy_home 	Chips won per game: 0.012	Chips won per hand: 0.0011	Min, Max: (-160,640)	Min bet %: 0.921
Player: 2	Strategy: strategy_home 	Chips won per game: -0.004	Chips won per hand: -0.0003	Min, Max: (-160,640)	Min bet %: 0.921
Player: 3	Strategy: strategy_home 	Chips won per game: -0.014	Chips won per hand: -0.0013	Min, Max: (-160,640)	Min bet %: 0.921
Player: 4	Strategy: strategy_home 	Chips won per game: -0.032	Chips won per hand: -0.0031	Min, Max: (-160,640)	Min bet %: 0.921


Ante:   6	Total hand counts: {0: 1266134140, 1: 1241549237}	 Runs: 50000000
Player: 0	Strategy: strategy_home2 	Chips won per game: -0.072	Chips won per hand: -0.0028	Min, Max: (-160,160)	Min bet %: 0.873
Player: 1	Strategy: strategy_home2 	Chips won per game: 0.072	Chips won per hand: 0.0029	Min, Max: (-160,160)	Min bet %: 0.873

Ante:   6	Total hand counts: {0: 1007519215, 1: 990612290, 2: 974192585}	 Runs: 50000000
Player: 0	Strategy: strategy_home2 	Chips won per game: -0.022	Chips won per hand: -0.0011	Min, Max: (-160,320)	Min bet %: 0.873
Player: 1	Strategy: strategy_home2 	Chips won per game: 0.012	Chips won per hand: 0.0006	Min, Max: (-160,320)	Min bet %: 0.873
Player: 2	Strategy: strategy_home2 	Chips won per game: 0.011	Chips won per hand: 0.0005	Min, Max: (-160,320)	Min bet %: 0.873

Ante:   6	Total hand counts: {0: 886697065, 1: 874436859, 2: 862024704, 3: 849679946}	 Runs: 50000000
Player: 0	Strategy: strategy_home2 	Chips won per game: -0.051	Chips won per hand: -0.0028	Min, Max: (-160,480)	Min bet %: 0.874
Player: 1	Strategy: strategy_home2 	Chips won per game: -0.013	Chips won per hand: -0.0008	Min, Max: (-160,480)	Min bet %: 0.874
Player: 2	Strategy: strategy_home2 	Chips won per game: 0.020	Chips won per hand: 0.0012	Min, Max: (-160,480)	Min bet %: 0.873
Player: 3	Strategy: strategy_home2 	Chips won per game: 0.044	Chips won per hand: 0.0026	Min, Max: (-160,480)	Min bet %: 0.873

Ante:   6	Total hand counts: {0: 759949248, 1: 749956125, 2: 739922859, 3: 730005343, 4: 720081154}	 Runs: 50000000
Player: 0	Strategy: strategy_home2 	Chips won per game: 0.038	Chips won per hand: 0.0025	Min, Max: (-160,640)	Min bet %: 0.873
Player: 1	Strategy: strategy_home2 	Chips won per game: 0.029	Chips won per hand: 0.0019	Min, Max: (-160,640)	Min bet %: 0.874
Player: 2	Strategy: strategy_home2 	Chips won per game: -0.004	Chips won per hand: -0.0003	Min, Max: (-160,640)	Min bet %: 0.874
Player: 3	Strategy: strategy_home2 	Chips won per game: -0.019	Chips won per hand: -0.0013	Min, Max: (-160,640)	Min bet %: 0.874
Player: 4	Strategy: strategy_home2 	Chips won per game: -0.043	Chips won per hand: -0.0030	Min, Max: (-160,640)	Min bet %: 0.873

Ante:   6	Total hand counts: {0: 72816657, 1: 69540830, 2: 72303486, 3: 69303478, 4: 70887212}	 Runs: 5000000
Player: 0	Strategy: fh_13_8 			Chips won per game: -1.323	Chips won per hand: -0.0908	Min, Max: (-160,640)	Min bet %: 0.814
Player: 1	Strategy: fh_11_8 			Chips won per game: 1.463	Chips won per hand: 0.1052	Min, Max: (-160,640)	Min bet %: 0.814
Player: 2	Strategy: strategy_home2 	Chips won per game: 0.588	Chips won per hand: 0.0406	Min, Max: (-160,640)	Min bet %: 0.874
Player: 3	Strategy: fh_13_8 			Chips won per game: -1.294	Chips won per hand: -0.0933	Min, Max: (-160,640)	Min bet %: 0.814
Player: 4	Strategy: strategy_home2 	Chips won per game: 0.566	Chips won per hand: 0.0399	Min, Max: (-160,640)	Min bet %: 0.874

Ante:   6	Total hand counts: {0: 52915361, 1: 55223386, 2: 54701835, 3: 49311680, 4: 47868259}	 Runs: 5000000
Player: 0	Strategy: fh_13_8 			Chips won per game: -1.990	Chips won per hand: -0.1880	Min, Max: (-160,640)	Min bet %: 0.813
Player: 1	Strategy: perfect 			Chips won per game: 2.059	Chips won per hand: 0.1864	Min, Max: (-160,640)	Min bet %: 0.856
Player: 2	Strategy: strategy_home 	Chips won per game: -0.376	Chips won per hand: -0.0344	Min, Max: (-160,640)	Min bet %: 0.922
Player: 3	Strategy: fh_11_8 			Chips won per game: 0.162	Chips won per hand: 0.0164	Min, Max: (-160,640)	Min bet %: 0.813
Player: 4	Strategy: fh_11_8 			Chips won per game: 0.145	Chips won per hand: 0.0151	Min, Max: (-160,640)	Min bet %: 0.813

"""
