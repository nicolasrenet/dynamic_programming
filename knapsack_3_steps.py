#!usr/bin/python3

import unittest

WEIGHT=0
VALUE=1


def subsets( items ):
	""" List all subsets of a set: upward recursion """

	set_list=[]

	def subrec( i, sub ):
		if i == len(items):
			set_list.append( sub )
			return
		subrec(i+1, sub + [items[i]] )
		subrec(i+1, sub )
	

	subrec( 0, [] )
	return set_list

def subsets_down( items ):
	""" List all subsets of a set: downward recursion """

	set_list=[]

	def subrec( i, sub ):
		if i < 0:
			set_list.append( sub )
			return
		subrec(i-1, sub + [items[i]] )
		subrec(i-1, sub )
	

	subrec( len(items)-1, [] )
	return set_list


def knapsack_01_bf( boxes, weight ):

	def ks(i, w):

		if w == 0 or i < 0:
			return 0

		if boxes[i][WEIGHT]> w:
			return  ks(i-1, w)

		return max( ks(i-1, w), boxes[i][VALUE] + ks(i-1,w-boxes[i][WEIGHT]) )

	return ks( len(boxes)-1, weight)

def knapsack_01_bf_ext( boxes, weight ):

	solutions = []
	count=0
	def ks(i, w):

		if w == 0 or i == len(boxes):
			return (0, [])

		if boxes[i][WEIGHT]> w:
			return  ks(i+1, w)

		within_value, within_items = ks(i+1, w-boxes[i][WEIGHT])
		within_value += boxes[i][VALUE]
		without_value, without_items =  ks(i+1, w)

		if within_value > without_value:
			return (within_value, [ boxes[i]] + within_items)
		return (without_value, without_items)

	pair = ks( 0, weight)
	print(count, " recursive calls")
	return pair



def knapsack_01_mem( boxes, weight ):


	memo = [ [ None for b in range(len(boxes)) ] for w in range(weight+1) ]
	count=0

	def ks(i, w):

		nonlocal count 
		
		#print("ks({},{})".format(i, w))
		if w == 0 or i == len(boxes):
			return (0, [])

		count += 1
		if memo[w][i]:
			return memo[w][i]

		if boxes[i][WEIGHT]> w:
			sol = ks(i+1, w)
			memo[w][i]=sol
			return sol

		without_value, without_items =  ks(i+1, w)
		within_value, within_items = ks(i+1, w-boxes[i][WEIGHT])
		within_value += boxes[i][VALUE]

		if within_value > without_value:
			sol=(within_value, [ boxes[i]] + within_items)
			memo[w][i]=sol
			return sol
		
		sol = (without_value, without_items)
		memo[w][i]=sol
		return sol

	pair = ks( 0, weight)
	print(count, " recursive calls")
	return pair


def knapsack_01_bottom_up( boxes, weight ):

	boxes = ( (0,0), ) + boxes

	memo = [ [ -1 for w in range(weight+1) ] for b in range(len(boxes)) ] 
		
	for i in range(len(boxes)):
		for w in range(weight+1):
			if i==0:
				memo[i][w]=0
			elif boxes[i][WEIGHT] > w:
				memo[i][w]=memo[i-1][w]
			else:
				memo[i][w] = max(
					memo[i-1][w],
					boxes[i][VALUE] + memo[i-1][w - boxes[i][WEIGHT]])
	print(memo)
	return memo[-1][-1]	
			



class Test_Knapsack(unittest.TestCase):

	boxes_1 = (
		(1,1),
		(1,2),
		(2,2),
		(4,10),
		(8,6),
		(12,8)
		) 

	boxes_2 = (
		(5,10),
		(4, 40),
		(6,30),
		(3,50),
		(2,40),
		(3,30),
		(7,10),
		(2,20)
	)

	def test_ks_01( self ):

		self.assertEqual( knapsack_01_bf( self.boxes_1, 15), 20)

	def test_ks_01_down( self ):

		self.assertEqual( knapsack_01_bf_down( self.boxes_1, 15), 20)


	def test_ks_01_bf_ext_1( self ):
		print("Extended returns best value")
		self.assertEqual( knapsack_01_bf_ext( self.boxes_1, 15)[0], 20)

	def test_ks_01_bf_ext_2( self ):
		print("Extended returns list of items")
		self.assertEqual( knapsack_01_bf_ext( self.boxes_1, 15)[1], [(1, 2), (2, 2), (4, 10), (8, 6)])

	def test_ks_01_mem_1( self ):
		print("Memoized returns best value")
		self.assertEqual( knapsack_01_mem( self.boxes_1, 15)[0], 20)

	def test_ks_01_mem_2( self ):
		print("Memoized returns list of items")
		self.assertEqual( knapsack_01_mem( self.boxes_1, 15)[1], [(1, 2), (2, 2), (4, 10), (8, 6)])

	def test_ks_01_bf_ext_3( self ):
		print("Extended returns best value (set 2)")
		self.assertEqual( knapsack_01_bf_ext( self.boxes_2, 20)[0], 210)

	def test_ks_01_bf_ext_4( self ):
		print("Extended returns list of items (set 2)")
		self.assertEqual( knapsack_01_bf_ext( self.boxes_2, 20)[1], [(4,40), (6, 30), (3, 50), (2, 40), (3, 30), (2, 20)])

	def test_ks_01_mem_3( self ):
		print("Memoized returns best value (set 2)")
		self.assertEqual( knapsack_01_mem( self.boxes_2, 20)[0], 210)

	def test_ks_01_mem_4( self ):
		print("Memoized returns list of items (set 2)")
		self.assertEqual( knapsack_01_mem( self.boxes_2, 20)[1], [(4,40), (6, 30), (3, 50), (2, 40), (3, 30), (2, 20)])

	def test_ks_01_bottom_up( self ):
		print("Memoized returns best value (20)")
		self.assertEqual( knapsack_01_bottom_up( self.boxes_2, 20), 210)

def main():
        unittest.main()

if __name__ == '__main__':
        main()


