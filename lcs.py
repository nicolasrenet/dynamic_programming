#!/usr/bin/python3
import unittest

X1=['A','B','C','B','D','A','B']
Y1=['B','D','C','A','B','A']

X2= ['C','G','G','A','A','T','G','C','C','G']
Y2= ['C','G','G','T','C','G','A','G']

X3= ['A','A','G','A','A','T','G','C','G','A']
Y3= ['C','G','G','A','C','G','A','G']

class Matrix():

	def __init__(self, m,n, default=0, labels=None):
		self.m=m
		self.n=n
		self.m_labels=None
		self.n_labels=None
		if labels is not None:
			self.m_labels=labels[0]
			self.n_labels=labels[1]
		self.array = [ [0 for i in range(0,n+1) ] for i in range(0,m+1) ]

	def initialize(self, val ):
		for i in range(0, self.m):
			for j in range(0, self.n):
				self.array[i][j]=val
	

	def get(self, x,y):
		return self.array[x][y]

	
	def set(self, x,y,val):
		self.array[x][y]=val

	def __str__(self):
		result = ''
		if self.n_labels is not None:
			result += '     y_i'
			for l in self.n_labels:
				result += '   {}'.format(l)
			result += '\n'	
		for i in range(0,self.m):
			if self.m_labels is not None:
				if i==0:
					result += ' x_i'
				else:
					result += '   {}'.format(self.m_labels[i-1])
			for j in range(0,self.n):
				if len(str(self.array[i][j]))==2:
					result += '  '
				else:
					result += '   '	
				result+='{}'.format(self.array[i][j])
			result += '\n'
		return result
			

def recursive_length( x, y ):
	"""
	A naive, recursive solution to the LCS problem. 
	"""
	if len(x) == 0 or len(y) == 0:
		return 0
	if x[-1] == y[-1]:
		return recursive_length( x[0:-1], y[0:-1]) + 1
	if x[-1] != y[-1]:
		max_length = recursive_length( x[0:-1],y)
		length2 = recursive_length( x,y[0:-1])
		if length2 > max_length:
			max_length = length2
		return max_length

def recursive_lcs( x, y, tab ):
	"""
	A naive, recursive solution to the LCS problem. 
	"""
	tab = tab+"  "
	print("{}recursive_lcs({}, {})".format(tab, x, y ))
	if len(x) == 0 or len(y) == 0:
		return ('')
	if x[-1] == y[-1]:
		lcs = recursive_lcs( x[0:-1], y[0:-1], tab) + x[-1]
		print("{}LCS: {}".format(tab,lcs))
		return lcs
	if x[-1] != y[-1]:
		lcs1 = recursive_lcs( x[0:-1],y, tab)
		lcs2 = recursive_lcs( x,y[0:-1], tab)
		if len(lcs2) > len(lcs1):
			lcs1 = lcs2
		print("{}LCS: {}".format(tab,lcs1))
		return lcs1
		

	
def recursive_length_memoized(x, y):


	def recursive_length_memoized_aux(x, y, r):
		
		if r[len(x)][len(y)] > 0:
			return r[len(x)][len(y)]

		if len(x) == 0 or len(y) == 0:
			length = 0
		elif x[-1] == y[-1]:
			length = recursive_length_memoized_aux( x[0:-1], y[0:-1],r) + 1
		elif x[-1] != y[-1]:
			length = recursive_length_memoized_aux( x[0:-1],y, r)
			l2 = recursive_length_memoized_aux( x,y[0:-1], r)
			if l2 > length:
				length = l2
		r[len(x)][len(y)] = length
		return length

	r = [ [0 for i in range(len(y)+1) ] for j in range( len(x)+1) ]
	return recursive_length_memoized_aux(x, y, r)


	

def lcs_length(x, y):
	m = len(x)
	n = len(y)

	b = Matrix(m+1, n+1, 0, (x,y))
	c = Matrix(m+1, n+1, 0, (x,y))

	for i in range(1, m+1):
		
		for j in range(1, n+1):
			
			if x[i-1] == y[j-1]:
				c.set(i,j, c.get(i-1,j-1) + 1)
				b.set(i,j,'NW')
			elif c.get(i-1,j) >= c.get(i,j-1):
				c.set(i,j,  c.get(i-1,j))
				b.set(i,j, 'N')
			else:	
				c.set(i,j, c.get(i, j-1))
				b.set(i,j, 'W')
	return (c,b)


def print_lcs(b, X, Y):
	"""
	Reconstruct a LCS from matrix B (the "arrows" matrix).
	
	:param c: the matrix of lengths
	:param X: string X
	:param Y: string Y
	:return: a list of tokens
	:rtype: list
	"""
	def print_lcs_recursive(b,i,j, lst):
		if i==0 or j==0:
			return
		if b.get(i,j)=='NW':
			print_lcs_recursive(b,i-1,j-1, lst)
			lst.append('{}'.format(X[i-1]))
		elif b.get(i,j)=='N':
			print_lcs_recursive(b,i-1,j, lst)
		else:
			print_lcs_recursive(b,i,j-1, lst)

	string = []
	print_lcs_recursive( b, len(X), len(Y) , string)
	return string

def print_lcs_alt(c, X, Y):
	"""
	Reconstruct a LCS without using matrix B (the "arrows" matrix).
	
	:param c: the matrix of lengths
	:param X: string X
	:param Y: string Y
	:return: a list of token
	:rtype: list
	"""

	active_nodes = [ [ 0 for row in range(0, len(Y)+1) ] for col in range(0, len(X)+1) ]

	def print_lcs_recursive(c, i, j, lst):
		active_nodes[i][j]=True
		if i==0 or j==0:
			return
		if X[i-1] == Y[j-1]:
			print_lcs_recursive(c, i-1, j-1, lst)
			lst.append('{}'.format(X[i-1]))
		elif c.get(i-1,j) > c.get(i,j-1):
			print_lcs_recursive(c, i-1, j, lst)
		elif c.get(i-1,j) == c.get(i,j-1):
			print_lcs_recursive(c, i, j-1, lst)
			print_lcs_recursive(c, i-1, j, lst)
		else:
			print_lcs_recursive(c, i, j-1, lst)
	string = []
	print_lcs_recursive(c, len(X), len(Y), string)
	return (string, active_nodes)
		  

def lcs_to_tikz(x, y):

	c,b = lcs_length(x, y)

	s,active_nodes = print_lcs_alt(c, x, y)

	#for i in active_nodes:
	#	print(i)

	active_edges=[]
	output = []

	output.append( '\\begin{tikzpicture}[-,>=stealth\',auto,node distance=2.8cm, semithick	]')
	output.append( '\\tikzset{')
	output.append( 'optimal/.style = {preaction={draw,red,-,double=red,double distance=3\pgflinewidth}, draw=black},')
	output.append( 'letter/.style= {font=\ttfamily\normalsize},')
	output.append( 'highlight/.style = {fill=blue!20,draw}')
	output.append('}')

	top_row = len(x)+2
	last_col = len(y)+2

	output.append('\\node\t(0-{}) at (0,{})\t{{$T$}};'.format(top_row, top_row))
	output.append('\\node\t(1-{}) at (1,{})\t{{$j$}};'.format(top_row, top_row))
	for col in range(2,last_col+1):
		output.append( '\\node\t({}-{}) at ({},{})\t{{${}$}};'.format(col, top_row, col, top_row, col-3))

	output.append('\\node\t(0-{}) at (0,{})\t{{$i$}};'.format(top_row-1, top_row-1))
	output.append('\\node\t(2-{}) at (2,{})\t{{$y[j]$}};'.format(top_row-1, top_row-1))

	for col in range(3,last_col+1):
		output.append( '\\node\t({}-{}) at ({},{})\t{{\\tt {}}};'.format(col, top_row-1, col, top_row-1, y[col-3]))

	output.append('\\node\t(0-{}) at (0,{})\t{{$-1$}};'.format(top_row-2, top_row-2))
	output.append('\\node\t(1-{}) at (1,{})\t{{$x[i]$}};'.format(top_row-2, top_row-2))
	output.append('\\node\t(2-{}) at (2,{})\t{{$0$}};'.format(top_row-2, top_row-2))
	
	for col in range(2,last_col+1):
		rw = 0
		if active_nodes[0][col-2]:
			output.append( '\\node\t({}-{})[highlight] at ({},{})\t{{${}$}};'.format(col, top_row-2, col, top_row-2, c.get(0,col-2)))
		else:
			output.append( '\\node\t({}-{}) at ({},{})\t{{${}$}};'.format(col, top_row-2, col, top_row-2, c.get(0,col-2)))

	for row in range(top_row-3,-1,-1):
		rw = top_row-(2+row)
		output.append('')	
		output.append('\\node\t(0-{}) at (0,{})\t{{${}$}};'.format(row, row,  rw))
		output.append('\\node\t(1-{}) at (1,{})\t{{\\tt {}}};'.format(row, row, x[rw-1]))
		for col in range(2,last_col+1):
			cl = col-2
			if active_nodes[rw][cl]:
				#print('tikz (x,y)={},{} --> [{},{}]'.format(row, col, rw,cl))
				output.append( '\\node[highlight]\t({}-{}) at ({},{})\t{{${}$}};'.format(col, row, col, row, c.get(rw,cl)))
				# explore W, NW, and N adjacent nodes: stores active edges
				if cl>0 and active_nodes[rw][cl-1]:
					active_edges.append( '({}-{}) edge ({}-{})'.format( col-1, row, col, row ))
				if x[rw-1]==y[cl-1] and cl>0 and rw>0 and active_nodes[rw-1][cl-1]:
					active_edges.append( '({}-{}) edge ({}-{})'.format( col-1, row+1, col, row ))
				if rw>0 and active_nodes[rw-1][cl]:
					active_edges.append( '({}-{}) edge ({}-{})'.format( col, row+1, col, row ))
			else:
				output.append('\\node\t({}-{}) at ({},{})\t{{\\tt {}}};'.format(col, row, col, row, c.get(rw, cl)))	
	
	output.append('\\path')
	output.append( '\n'.join(active_edges))
	output.append(';')

	output.append('\\end{tikzpicture}')



	return '\n'.join(output)


class LCS_Test( unittest.TestCase ):


	X1=['A','B','C','B','D','A','B']
	Y1=['B','D','C','A','B','A']

	X2= ['C','G','G','A','A','T','G','C','C','G']
	Y2= ['C','G','G','T','C','G','A','G']

	X3= ['A','A','G','A','A','T','G','C','G','A']
	Y3= ['C','G','G','A','C','G','A','G']

	def test_lcs_to_tikz(self):
		print( lcs_to_tikz( ['A','C','G','A'], ['A','T','G','C','T','A']))

	def atest_lcs_length_1( self ):
		matrices = lcs_length( self.X1, self.Y1 )
		print(matrices[0])
		print(matrices[1])
		self.assertEqual(print_lcs( matrices[1], self.X1, self.Y1), ['B','C','B','A'])


	def atest_lcs_length_2( self ):
		matrices = lcs_length( self.X2, self.Y2 )
		print(matrices[0])
		print(matrices[1])
		self.assertEqual(print_lcs( matrices[1], self.X2, self.Y2), ['C','G','G','T','G','G'])


	def atest_lcs_length_3( self ):
		matrices = lcs_length( self.X3, self.Y3 )
		print(matrices[0])
		print(matrices[1])
		self.assertEqual(print_lcs( matrices[1], self.X3, self.Y3), ['G','A','C','G','A'])

	def atest_recursive_length_1( self ):
		self.assertEqual( recursive_length(self.X1, self.Y1), 4 )
		
	def atest_recursive_length_2( self ):
		self.assertEqual( recursive_length(self.X2, self.Y2), 6 )

	def atest_recursive_length_3( self ):
		self.assertEqual( recursive_length(self.X3, self.Y3), 5 )


	def atest_recursive_length_memoized_1( self ):
		self.assertEqual( recursive_length_memoized(self.X1, self.Y1), 4 )
		
	def atest_recursive_length_memoized_2( self ):
		self.assertEqual( recursive_length_memoized(self.X2, self.Y2), 6 )

	def atest_recursive_length_memoized_3( self ):
		self.assertEqual( recursive_length_memoized(self.X3, self.Y3), 5 )


	def atest_15_4_1_1( self ):
		X = [ '0', '1', '0', '1', '1', '0', '1', '1', '0' ]
		Y = [ '1', '0', '0', '1', '0','1','0','1']
		matrices = lcs_length( X, Y )
		print(matrices[0])
		print(matrices[1])
		self.assertEqual(print_lcs( matrices[1], X, Y),['0','1','0','1','0','1'])

	def atest_15_4_1_2( self ):
		X = [ '0', '1', '0', '1', '1', '0', '1', '1', '0' ]
		Y = [ '1', '0', '0', '1', '0','1','0','1']
		matrices = lcs_length( Y, X )
		print(matrices[0])
		print(matrices[1])
		self.assertEqual(print_lcs( matrices[1], Y, X),['1','0','0','1','1','0'])

	def atest_15_4_2_1( self):
		matrices = lcs_length( self.X3, self.Y3 )
		print(matrices[0])
		print(matrices[1])
		self.assertEqual(print_lcs_alt( matrices[0], self.X3, self.Y3), ['G','A','C','G','A'])

#	def atest_recursive_lcs_1( self ):
#		self.assertEqual( recursive_lcs(self.X1, self.Y1, ''), 'BCBA' )
#		
#	def atest_recursive_lcs_2( self ):
#		self.assertEqual( recursive_lcs(self.X2, self.Y2, ''), 'CGGTGG' )
#
#	def atest_recursive_lcs_3( self ):
#		self.assertEqual( recursive_lcs(self.X3, self.Y3, ''), 'GACGA' )




#for pair in [(X1,Y1), (X2,Y2), (X3,Y3)]:
#	print("--------------------")
#	print('\nX={}\nY={}\n'.format(pair[0], pair[1]))
#	matrices = lcs_length(pair[0],pair[1])
#	print(matrices[0])
#	print(matrices[1])
#
#	result = []
#	print_lcs(matrices[1], pair[0], len(pair[0]), len(pair[1]), result)
#
#	print(result)



def main():
        unittest.main()

if __name__ == '__main__':
        main()


