#!/usr/bin/python3

import unittest
import time

class Counter:
	def __init__(self):
		self.count=0
	def inc(self):
		self.count+=1
	def read(self):
		return self.count

def max_vorp_brute_force( players, budget ):

	pools = ( 	players[0:11],
		 	players[11:22],
		 	players[22:33],
			players[33:44])

	max_vorp=0
		
	count = Counter()

	def max_vorp_rec( position, cumulated_vorp, salaries, signed ):
		nonlocal max_vorp
		count.inc()
		#print('max_vorp_rec({},{},{},{})'.format(position, cumulated_vorp, salaries, signed))
		if position==4:
			if cumulated_vorp > max_vorp and salaries <= budget:
				max_vorp = cumulated_vorp
				#print("Signed: {} VORP={}".format(signed, cumulated_vorp))
			return
		for player in range(0,11):
			sal = salaries + pools[ position ][player][0]
			if sal > budget:
				if cumulated_vorp> max_vorp:
					max_vorp = cumulated_vorp
				#print("Signed: {} VORP={}".format(signed, cumulated_vorp))
				return
			else:
				max_vorp_rec( position+1, cumulated_vorp + pools[ position ][player][1], sal, signed+[player])			


	max_vorp_rec(0, 0, 0, [])
	print('BRUTE-FORCE - Budget: {} Calls: {}'.format(budget, count.read()))
	return max_vorp

def next_best(players, i, free, indent):
	# Note: if solutions are not unique, the first position will be selected,
	# possibly resulting in non-optimal solutions for a larger budget

	#print("{}Scanning for next best player at {}K".format(indent, i))
	max_vorp = -1 
	max_pos = 0
	for p in players:
		if not free.is_set(p[2]) and p[0]==i:
			#print("{}Found player {}".format(indent, p))
			if p[1]> max_vorp:
				max_pos = p[2]
				max_vorp = p[1] 
	if max_pos > 0: free.set_bit( max_pos )
	return max_vorp, free
			

class BitSet:
	def __init__(self, size, value=0):
		self.bits = value
		self.size = size
	
	def set_bit(self, i):
		#print("Setting bit {} in {:b}".format(i, self.bits))
		self.bits |= (1<<(i-1))
		return self.bits
	def unset_bit(self, i):
		self.bits ^= (1<<(i-1))
		return self.bits
	def complement(self):
		comp = ~self.bits & ((1<<(self.size))-1)
		return BitSet( self.size, comp)
	def is_set(self, i):
		return bool(self.bits & (1<<(i-1)))
	def copy(self):
		return BitSet(self.size, self.bits)

	def free_positions(self):
		free = []
		for i in range(self.size):
			if not self.is_set(i):
				free.append(i)
		return free

def max_vorp_naive( players, total_budget ):

	count = Counter()

	def max_vorp_rec( budget, free, indent):
		#print("{}==== max_vorp_rec({})".format(indent, budget))
	
		count.inc()
		if budget == 0:
			return 0
		max_vorp = 0
		max_free = None
		for i in range(1,budget+1):
			free_copy = free.copy()
			next_best_vorp = next_best(players, i, free_copy, indent)
			#print("{}Choosing {}K: next best is {}".format(indent, i, next_best_vorp[0]))
			if next_best_vorp[0]>0:
				vorp = next_best_vorp[0] + max_vorp_rec(budget-i, free_copy, indent+'  ')
				if vorp>max_vorp:
					max_vorp = vorp
					max_free = free_copy

		#print(counter.read())
		return max_vorp

	max_vorp = max_vorp_rec(total_budget, BitSet(4), '')
	print('NAIVE - Budget: {} Calls: {}'.format(total_budget, count.read()))
	return max_vorp
			

def max_vorp_memoized( players, total_budget ):
		
	memo = [ [ -1 for i in range(0, total_budget+1) ] for f in range(0,16)]
	
	counter = Counter()	

	def max_vorp_rec( budget, free, indent):
		#print("{}==== max_vorp_rec({})".format(indent, budget))
		nonlocal counter

		counter.inc()	

		if memo[free.bits][budget]>=0:
			#print("{}Read from memo[{:b}][{}] --> {}".format(indent,free.bits, budget, memo[free.bits][budget]))
			return memo[free.bits][budget]
			
		if budget == 0:
			return 0
		max_vorp = 0
		max_free = None
		for i in range(1,budget+1):
			free_copy = free.copy()
			next_best_vorp = next_best(players, i, free_copy, indent)
			#print("{}Choosing {}K: next best is {}".format(indent, i, next_best_vorp[0]))
			if next_best_vorp[0]>0:
				vorp = next_best_vorp[0] + max_vorp_rec(budget-i, free_copy, indent+'  ')
				if vorp>max_vorp:
					max_vorp = vorp
					max_free = free_copy

		memo[free.bits][budget] = max_vorp
		return max_vorp

	max_vorp = max_vorp_rec(total_budget, BitSet(4), '')
	print('MEMOIZED - Budget: {} Calls: {}'.format(total_budget, counter.read()))
	return max_vorp
			
		

		

class PlayersUnitTest(unittest.TestCase):

	players = (

		# (salary, VORP, position)
		(0,0,1),
		(1,4,1),
		(1,2,1),
		(2,9,1),
		(3,7,1),
		(5,8,1),
		(6,16,1),
		(6,13,1),
		(7,13,1),
		(8,10,1),
		(9,14,1),

		(0,0,2),
		(1,6,2),
		(2,3,2),
		(3,5,2),
		(4,2,2),
		(6,10,2),
		(7,9,2),
		(7,8,2),
		(8,11,2),
		(9,9,2),
		(9,14,2),

		(0,0,3),
		(1,5,3),
		(2,5,3),
		(2,8,3),
		(4,10,3),
		(4,9,3),
		(5,9,3),
		(7,11,3),
		(8,14,3),
		(9,13,3),
		(10,15,3),
		
		(0,0,4),
		(2,3,4),
		(2,2,4),
		(3,6,4),
		(3,4,4),
		(4,7,4),
		(4,5,4),
		(6,10,4),
		(6,6,4),
		(8,11,4),
		(8,9,4))

	
	# 0-BF: 10: (actual, expected)  20: (actual, expected) 32: (actual, expected)
	# 0-REC: 10: (actual, expected)  20: (actual, expected) 32: (actual, expected)
	# 0-MEM: 10: (actual, expected)  20: (actual, expected) 32: (actual, expected)

	times = [ {10: (0,0), 20:(0,0), 32:(0,0) } for i in range(3) ]


	def test_bit_set_1(self):
		bs = BitSet(4)
		bs.set_bit(2)
		bs.set_bit(3)
		bs.set_bit(4)
		bs.unset_bit(3)
		self.assertEqual( bs.bits, 10)
		self.assertEqual( bs.complement().bits, 5)

	def test_bit_set_2(self):
		bs = BitSet(4,5)
		self.assertTrue( bs.is_set(1))
		self.assertTrue( bs.is_set(3))
		self.assertFalse( bs.is_set(2))
		self.assertFalse( bs.is_set(4))


	def test_brute_force(self):
		self.assertEqual( max_vorp_brute_force( self.players, 3), 15)
		self.assertEqual( max_vorp_brute_force( self.players, 4), 20)
		self.assertEqual( max_vorp_brute_force( self.players, 5), 23)
		self.assertEqual( max_vorp_brute_force( self.players, 6), 23)
		self.assertEqual( max_vorp_brute_force( self.players, 7), 26)
		self.assertEqual( max_vorp_brute_force( self.players, 10), 31)
		self.assertEqual( max_vorp_brute_force( self.players, 20), 44)
		self.assertEqual( max_vorp_brute_force( self.players, 32), 55)

		
		
	def test_naive_recursive_03(self):
		self.assertEqual( max_vorp_naive(self.players, 3), 15)
	def test_naive_recursive_04(self):
		self.assertEqual( max_vorp_naive(self.players, 4), 20)
	def test_naive_recursive_5(self):
		self.assertEqual( max_vorp_naive(self.players, 5), 23)
	def test_naive_recursive_06(self):
		self.assertEqual( max_vorp_naive(self.players, 6), 23)
	def test_naive_recursive_07(self):
		self.assertEqual( max_vorp_naive(self.players, 7), 26)

	def test_naive_recursive_10(self):
		start = time.time()
		self.assertEqual( max_vorp_naive(self.players, 10), 31)
		elapsed = time.time() - start
		self.times[1][10]=(elapsed, elapsed)
		
	def test_naive_recursive_20(self):
		start = time.time()
		self.assertEqual( max_vorp_naive(self.players, 20), 44)
		elapsed = time.time() - start
		self.times[1][20]=(elapsed, elapsed)

	def test_naive_recursive_55(self):
		start = time.time()
		self.assertEqual( max_vorp_naive(self.players, 32), 55)
		elapsed = time.time() - start
		self.times[1][32]=(elapsed, elapsed)

	def test_memoized_recursive_03(self):
		self.assertEqual( max_vorp_memoized(self.players, 3), 15)
	def test_memoized_recursive_04(self):
		self.assertEqual( max_vorp_memoized(self.players, 4), 20)
	def test_memoized_recursive_05(self):
		self.assertEqual( max_vorp_memoized(self.players, 5), 23)
	def test_memoized_recursive_06(self):
		self.assertEqual( max_vorp_memoized(self.players, 6), 23)
	def test_memoized_recursive_07(self):
		self.assertEqual( max_vorp_memoized(self.players, 7), 26)
	def test_memoized_recursive_10(self):
		start = time.time()
		self.assertEqual( max_vorp_memoized(self.players, 10), 31)
		elapsed = time.time() - start
		self.times[2][10]=(elapsed, elapsed)
	def test_memoized_recursive_20(self):
		start = time.time()
		self.assertEqual( max_vorp_memoized(self.players, 20), 44)
		elapsed = time.time() - start
		self.times[2][20]=(elapsed, 2*self.times[2][10][0])
	def test_memoized_recursive_32(self):
		start = time.time()
		self.assertEqual( max_vorp_memoized(self.players, 32), 55)
		elapsed = time.time() - start
		self.times[2][32]=(elapsed, 3.2*self.times[2][10][0])

	@classmethod
	def tearDownClass(cls):
		print("BF\tActual\tExpected")
		print("10\t{}\t{}".format(cls.times[0][10][0], cls.times[0][10][1]))
		print("20\t{}\t{}".format(cls.times[0][20][0], cls.times[0][20][1]))
		print("32\t{}\t{}".format(cls.times[0][32][0], cls.times[0][32][1]))

		print("REC\tActual\tExpected")
		print("10\t{}\t{}".format(cls.times[1][10][0], cls.times[1][10][1]))
		print("20\t{}\t{}".format(cls.times[1][20][0], cls.times[1][20][1]))
		print("32\t{}\t{}".format(cls.times[1][32][0], cls.times[1][32][1]))

		print("MEM\tActual\tExpected")
		print("10\t{}\t{}".format(cls.times[2][10][0], cls.times[2][10][1]))
		print("20\t{}\t{}".format(cls.times[2][20][0], cls.times[2][20][1]))
		print("32\t{}\t{}".format(cls.times[2][32][0], cls.times[2][32][1]))
			


def main():
        unittest.main()

if __name__ == '__main__':
        main()


