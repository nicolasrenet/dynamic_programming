#!/usr/bin/python3
import sys
import unittest

graph_node=0
cluster=0
color = True

def graph( s, active ):
	if active:
		print( s )

def max(x, y):
	if x >= y:
		return x
	return y


def cut_rod( p, n, node_id=0, graph_active=True):

	global graph_node

	graph_node = 0
	
	if n==0:
		return 0

	q = -(2**14)

	ranked_children = []
	for i in range(1,n+1):
		graph_node+=1
		current_child=graph_node
		graph('subgraph cluster{} {{'.format(current_child), graph_active)
		graph('label="pr[{}] + "'.format(i), graph_active)
		graph('{}[label="cr({})"]'.format(current_child,n-i), graph_active)
		graph('}', graph_active)
		#print('{} -- {};'.format(node_id, current_child))	
		this_solution = p[i] + cut_rod(p, n-i, current_child)
		if this_solution > q:
			q = this_solution
			ranked_children.insert(0, current_child)
		else:
			ranked_children.append(current_child)

	graph('{} -- {}[color="red",penwidth=2.0];'.format(node_id, ranked_children[0]), graph_active)	
	for child in ranked_children[1:]:
		graph('{} -- {};'.format(node_id, child), graph_active)	
	return q




def memoized_cut_rod( p, n, graph_active=True):
	graph('graph {', graph_active)
	graph('{}[label="cr({})"]'.format(graph_node,n), graph_active)

	r = [None]*(n+1)
	# initializing the array of subresults
	for i in range(n+1):
		r[i]=-(2**14)
	result = memoized_cut_rod_aux(p, n, r)
	graph('}', graph_active)
	return result
	



def memoized_cut_rod_aux(p, n, r, node_id=0, graph_active=True):
	
	global graph_node, color

	this_solution=0
	
	if r[n] >= 0:
		graph_node+=1
		graph('{}[label="r[{}]"]'.format(graph_node, n), graph_active)
		graph('{} -- {}'.format(node_id, graph_node), graph_active)	
		return r[n]
	if n==0:
		q = 0
	else:
		q = -(2**14)
		# adding at head for winners, at tail for others
		ranked_children=[]
		childrens_revenues=[]
		for i in range(1, n+1):
			graph_node+=1
			current_child=graph_node
			graph('subgraph cluster{} {{'.format(current_child), graph_active)
			graph('label="pr[{}] + "'.format(i), graph_active)
			graph('{}[label="cr({})"]'.format(current_child,n-i), graph_active)
			graph('}', graph_active)
			this_solution = p[i] + memoized_cut_rod_aux(p, n-i, r, current_child)
			if this_solution > q:
				q = this_solution	
				ranked_children.insert(0,current_child)	
				childrens_revenues.insert(0,q)
				#print('{} -- {}[color="red"];'.format(node_id, current_child))	
			else:
				ranked_children.append(current_child)
				childrens_revenues.append( this_solution )

		if color: 
			graph('{} -- {}[color="red",penwidth=2.0, label={}];'.format(node_id, ranked_children[0], q), graph_active)
		else:
			graph('{} -- {}[label={}];'.format(node_id, ranked_children[0],  q), graph_active)

		for child in range(1, len(ranked_children)):
			graph('{} -- {}[label={}];'.format(node_id, ranked_children[child], childrens_revenues[child]), graph_active)
	r[n] = q
	return q

def memoized_cut_rod_extended( p, n):
	""" Cutting rod problem: the memoized, recursive solution that returns the maximum price, as well at the solution array.

	The function returns a pair, i.e. a 2-tuple (price, s) where price is the optimal price for the given length n, and s is a list where an element at position i is the length of the optimal first cut for total rod length i.
	
	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:type p: list
	:type n: int
	:rtype: tuple
	"""
	
	# initializing the array of subresults with infinite negative values
	r = [ -2**14 for i in range(0,n+1) ]


	# The solution array will store the optimal first cut for all 
	# lengths: by default, it associates to each length (indices 1 to 10)
	# the length itself, i.e. no cut at all
	s = list(range(0,(n+1)))

	price = memoized_cut_rod_extended_aux(p, n, r,s)

	return (price, s)



def memoized_cut_rod_extended_aux(p, n, r, s):
	""" Cutting rod problem: the recursive part of the memoized, recursive solution that returns the maximum price,
	and the solution array.

	This recursive subprocedure just returns the price, and maintains the solution array that is passed in as a parameter.

	:param p: the array of prices, with $0 in position 0, and p_i in position i.
	:param n: length of rod for which a solution is to be computed (n < p.length)
	:param r: the memo, that stores the optimal price for length i at position i
	:param s: the solution array, where an element at position i is the length of the optimal first cut for total rod length i
	:type p: list
	:type n: int
	:type r: list
	:type s: list
	:rtype: tuple
	"""
	
	if r[n] >= 0:
		return r[n]
	if n==0:
		q = 0
	else:
		q = -(2**14)
		for i in range(1, n+1):
			has_cut = p[i] + memoized_cut_rod_extended_aux(p, n-i, r,s)
			if has_cut > q:
				q = has_cut
				s[n]=i
	r[n] = q
	return q


def bottom_up_cut_rod(p, n):

	r=[None]*(n+1)
	r[0]=0
	
	for j in range(1, n+1):
		print('j={}:'.format(j))
		q = -(2**14)
		for i in range(1, j+1):
			print('\tp[{}] + r[{}]'.format(i,j-i))
			q = max(q, p[i] + r[j-i])
		r[j] = q
		print('\nr[{}]=${}'.format(j, r[j], ))
		print('')
	print('r[n]=${}'.format(r[n]))
	return r[n]

def extended_bottom_up_cut_rod(p, n):

	r=[None]*(n+1)
	r[0]=0
	s=[None]*(n+1)
	
	for j in range(1, n+1):
		print('j={}:'.format(j))
		q = -(2**14)
		for i in range(1, j+1):
			print('\tp[{}] + r[{}]'.format(i,j-i))
			if q < ( p[i] + r[j-i]):
				q = ( p[i] + r[j-i])
				s[j]=i
		r[j] = q
		print('\nr[{}]=${} s[{}]={} in'.format(j, r[j], j,s[j]))
		print('')
	print('r[n]=${}'.format(r[n]))
	print('s={}'.format(s))
	index_table=list(range(0,n+1))
	index_table[0]=None
	print('l={}'.format(index_table))
	return (r[n],s)


def read_solution_array(s, n):
	""" Read a solution array, i.e. return the lengths of rod the pieces that make an optimal cut for length n, as a list.

	:param s: the solution array, a list where an element at position i is the length of the optimal first cut for total rod length i. 
	:param n: the length of rod for which a solution is to be read
	:rtype: list
	"""
	i = n
	bits = []
	while( i>0):
		bits.append( s[i] )
		i -= s[i]
	return bits


def run_naive(n):
	global prices, graph_node
	print('graph {')
	print('{}[label="cr({})"]'.format(graph_node,n))
#
	cut_rod(prices,n,0)
	print('}')



class Cut_Rod_Test( unittest.TestCase ):

	# a class attribute
	prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
	prices2 =  [0, 1, 5, 5, 9, 10, 15, 17, 20, 24, 30]
	prices3 =  [0, 2, 8, 7, 10, 12, 15, 17, 20, 24, 30]
	
	def test_cut_rod_naive_1(self):

		self.assertEqual( cut_rod(self.prices, 5), 13 )


	def test_cut_rod_naive_2(self):
			
		self.assertEqual( cut_rod(self.prices, 9), 25 )


	def test_memoized_cut_rod_1(self):
		
		self.assertEqual( memoized_cut_rod(self.prices, 5), 13 )
		
	def test_memoized_cut_rod_2(self):
		
		self.assertEqual( memoized_cut_rod(self.prices, 9), 25 )
		
	
	def test_bottom_up_cut_rod_1(self):
		
		self.assertEqual( bottom_up_cut_rod(self.prices, 5), 13 )
		
	def test_bottom_up_cut_rod_2(self):
		
		print("test_bottom_up_cut_rod( prices, 10 )")
		max_price,solution_array = extended_bottom_up_cut_rod(self.prices, 9)
		self.assertEqual( read_solution_array( solution_array, 9), [3,6] )
		
	def test_memoized_cut_rod_extended_1(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 1)	
		self.assertEqual( max_price, 1 )
		self.assertEqual( solution_array, [0, 1])

	def test_memoized_cut_rod_extended_2(self):
		
		print("test_memoized_cut_rod_extended(prices, 6)")
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 5)	
		self.assertEqual( max_price, 13 )
		self.assertEqual( solution_array, [0, 1, 2, 3, 2, 2 ])
		
	def test_memoized_cut_rod_extended_3(self):
		
		print("test_memoized_cut_rod_extended(prices2, 6)")
		max_price, solution_array = memoized_cut_rod_extended(self.prices2, 5)	
		self.assertEqual( max_price, 11 )
		self.assertEqual( solution_array, [0, 1, 2, 1, 2, 1 ])
		
	def test_memoized_cut_rod_extended_4(self):
		
		print("test_memoized_cut_rod_extended(prices3, 5)")
		max_price, solution_array = memoized_cut_rod_extended(self.prices3, 5)	
		self.assertEqual( max_price, 18 )
		self.assertEqual( solution_array, [0, 1, 2, 1, 2, 1 ])
		
	def test_memoized_cut_rod_extended_5(self):
		
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 9)	
		self.assertEqual( max_price, 25 )
		self.assertEqual( solution_array, [0, 1, 2, 3, 2, 2, 6, 1, 2, 3] )
	
	def test_read_solution_array_1(self):
		
		print("test_read_solution_array( prices) ")	
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 9)	
		self.assertEqual( read_solution_array( solution_array, 1), [1])

	def test_read_solution_array_9(self):
		print("test_read_solution_array( prices) ")	
		max_price, solution_array = memoized_cut_rod_extended(self.prices, 9)	
		self.assertEqual( read_solution_array( solution_array, 9), [3,6])

	
	def test_bottom_up_cut_rod_3( self ):
		print("test_bottom_up_cut_rod( prices2, 10 )")
		max_price, solution_array = extended_bottom_up_cut_rod(self.prices2, 9)
		self.assertEqual( read_solution_array( solution_array, 9), [9])




def main():
        unittest.main()

if __name__ == '__main__':
        main()

#eval(sys.argv[1])
