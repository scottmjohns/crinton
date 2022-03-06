from math import sqrt
import collections

def perfect(left, right, card_count, chips, pot, deck, max_loss):
	def perfect_bet_size(pw, pl):
		a, b, c = 2, pl - (3.0*pw), (3.0*pw) + pl - 2.0
		return (1.0/a) * ((-1.0*b) - sqrt((b*b)-(4.0*a*c)))
	max_bet = int(0.5*(chips + max_loss))
	deck_size = len(deck)
	win_count = 0
	for i in range(left+1, right):
		win_count += card_count[i]
	pw = win_count / deck_size
	match_count = card_count[left] + card_count[right]
	pm = match_count / deck_size
	pl = 1 - pw - pm
	if (3.0*pw) + pl - 2.0 <= 0:
		return min(max_bet, 1)
	else:
		bet_size = perfect_bet_size(pw, pl)
		return min(max_bet,round(bet_size * pot))

def strategy_full_half(full_gap, half_gap, left, right, card_count, chips, pot, deck, max_loss):
	max_bet = int(0.5*(chips + max_loss))
	gap = right - left
	if gap >= full_gap:
		return min(max_bet,pot)
	if gap >= half_gap:
		return min(max_bet,round(0.5*pot))
	return 1

def fh_11_7(left, right, card_count, chips, pot, deck, max_loss):
	return strategy_full_half(11, 7, left, right, card_count, chips, pot, deck, max_loss)
def fh_11_8(left, right, card_count, chips, pot, deck, max_loss):
	return strategy_full_half(11, 8, left, right, card_count, chips, pot, deck, max_loss)
def fh_12_7(left, right, card_count, chips, pot, deck, max_loss):
	return strategy_full_half(12, 7, left, right, card_count, chips, pot, deck, max_loss)
def fh_12_8(left, right, card_count, chips, pot, deck, max_loss):
	return strategy_full_half(12, 8, left, right, card_count, chips, pot, deck, max_loss)
def fh_13_7(left, right, card_count, chips, pot, deck, max_loss):
	return strategy_full_half(13, 7, left, right, card_count, chips, pot, deck, max_loss)
def fh_13_8(left, right, card_count, chips, pot, deck, max_loss):
	return strategy_full_half(13, 8, left, right, card_count, chips, pot, deck, max_loss)

def strategy_home(left, right, card_count, chips, pot, deck, max_loss):
	gap = right - left
	if gap <= 9:
		return 1
	elif pot > 20 and gap < 12:
		max_bet = int(0.5*(chips + max_loss))
		return min(max_bet, round(0.5*pot))
	max_bet = int(0.5*(chips + max_loss))
	return min(max_bet, pot)

def strategy_home2(left, right, card_count, chips, pot, deck, max_loss):
	gap = right - left
	if gap <= 8:
		return 1
	elif (9 <= gap <= 10) or (pot > 20 and 11 <= gap <= 12):
		max_bet = int(0.5*(chips + max_loss))
		return min(max_bet, round(0.5*pot))
	max_bet = int(0.5*(chips + max_loss))
	return min(max_bet, pot)
