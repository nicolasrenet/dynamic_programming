#!/usr/bin/python3
import unittest
import random

X1=['A','B','C','B','D','A','B']
Y1=['B','D','C','A','B','A']

X2= ['C','G','G','A','A','T','G','C','C','G']
Y2= ['C','G','G','T','C','G','A','G']

X3= ['A','A','G','A','A','T','G','C','G','A']
Y3= ['C','G','G','A','C','G','A','G']


def recursive_length( x, y ):
    """
    A naive, recursive solution to the LCS problem. 
    """
    if len(x) == 0 or len(y) == 0:
        return 0
    if x[-1] == y[-1]:
        return recursive_length( x[0:-1], y[0:-1]) + 1
    return max( recursive_length( x[0:-1],y), recursive_length( x,y[0:-1]))

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
    return max( recursive_lcs( x[0:-1],y, tab), recursive_lcs( x,y[0:-1], tab))
        

    
def recursive_length_memoized(x, y):

    def recursive_length_memoized_aux(x, y, r):
        
        if r[len(x)][len(y)] > 0:
            return r[len(x)][len(y)]

        if len(x) == 0 or len(y) == 0:
            length = 0
        elif x[-1] == y[-1]:
            length = recursive_length_memoized_aux( x[0:-1], y[0:-1],r) + 1
        else:
            length = recursive_length_memoized_aux( x[0:-1],y, r)
            l2 = recursive_length_memoized_aux( x,y[0:-1], r)
            if l2 > length:
                length = l2
        r[len(x)][len(y)] = length
        return length

    r = [ [0 for i in range(len(y)+1) ] for j in range( len(x)+1) ]
    return recursive_length_memoized_aux(x, y, r)


def non_deterministic_memoized(x, y):


    def recursive_memoized_aux(x, y, r, t):
        
        #print(t+'lcs({},{})'.format(len(x), len(y)))
        #print('memo[0][3]: {}'.format( r[0][3] ))
        if r[len(x)][len(y)]:
            #print(t+'retrieving result memo[{}][{}]={}'.format(len(x), len(y), r[len(x)][len(y)]))
            return r[len(x)][len(y)]

        if len(x) == 0 or len(y) == 0:
            length,solutions = (0,[[]])
        elif x[-1] == y[-1]:
            #print(t+ "X[m]:{}==Y[n]:{}".format(x[-1],x[-1]))
            length, solutions = recursive_memoized_aux( x[0:-1], y[0:-1],r,t+'  ') 
            length += 1
            solutions = [ s + [x[-1]] for s in solutions ] 
            #print(t+ "Solutions: {}".format(solutions))
        else:
            length_1, north_solutions = recursive_memoized_aux( x[0:-1],y, r,t+'  ')
            length_2, west_solutions = recursive_memoized_aux( x,y[0:-1], r,t+'  ')
            if length_2 > length_1:
                length,solutions = length_2,west_solutions
            elif length_1 > length_2:
                length,solutions = length_1, north_solutions
            else:
                length, solutions = length_1, west_solutions + north_solutions 
                #print(t+ 'Merge N:{} and W:{} into {}'.format( north_solutions,west_solutions,solutions))
        #print(t+'memo[{}][{}]={}'.format( len(x), len(y), (length, solutions)))
        #r[len(x)][len(y)] = (length,solutions)
        return (length,solutions)

    r = [ [None for i in range(len(y)+1) ] for j in range( len(x)+1) ]
    length, solutions = recursive_memoized_aux(x, y, r,'')

    words = []
    for seq in solutions:
        words.append( ''.join(  seq ))
    words.sort()
    return (length, words)
    

def lcs_length(x, y):

    m = [  [0 for j in range(len(y)+1) ] for i in range(len(x)+1) ]

    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]:
                m[i][j] = m[i-1][j-1] + 1
            elif m[i-1][j] >= m[i][j-1]:
                m[i][j] =  m[i-1][j]
            else:    
                m[i][j] =  m[i][j-1]
    return (m[-1][-1], m)


def reconstruct_lcs(c, X, Y):
    """
    Reconstruct a LCS from the length matrix.
    
    :param c: the matrix of lengths
    :param X: string X
    :param Y: string Y
    :return: a list of token
    :rtype: list
    """

    def reconstruct_lcs_recursive(i, j):
        if i==0 or j==0:
            return
        if X[i-1] == Y[j-1]:
            reconstruct_lcs_recursive(i-1, j-1)
            seq.append(X[i-1])
        elif c[i-1][j] >= c[i][j-1]:
            reconstruct_lcs_recursive(i-1, j)
        elif c[i-1][j] < c[i][j-1]:
            reconstruct_lcs_recursive(i, j-1)

    seq = []
    reconstruct_lcs_recursive(len(X), len(Y))
    return seq

def get_active_nodes(c, X, Y):
    """
    A matrix of active nodes
    
    :param c: the matrix of lengths
    :param X: string X
    :param Y: string Y
    :return: a matrix of lengths
    :rtype: list
    """
    active_nodes = [ [ 0 for col in range(len(Y)+1) ] for row in range(len(X)+1) ]

    def lcs_recursive(i, j):
        active_nodes[i][j]=1
        if i==0 or j==0:
            return
        if X[i-1] == Y[j-1]:
            active_nodes[i][j] += 1
            lcs_recursive(i-1, j-1)
        elif c[i-1][j] > c[i][j-1]:
            lcs_recursive(i-1, j)
        elif c[i-1][j] < c[i][j-1]:
            lcs_recursive(i, j-1)
        else:
            lcs_recursive(i, j-1)
            lcs_recursive(i-1, j)

    lcs_recursive(len(X), len(Y))
    return active_nodes
          

def lcs_to_tikz(x, y, template=False):

    length,c = lcs_length(x, y)

    active_nodes = get_active_nodes(c, x, y)

    active_edges=[]
    output = []

    output.append( '\\begin{tikzpicture}[-,>=stealth\',auto,node distance=2.8cm, semithick    ]')
    output.append( '\\tikzset{')
    output.append( 'optimal/.style = {preaction={draw,red,-,double=red,double distance=3\pgflinewidth}, draw=black},')
    output.append( 'letter/.style= {font=\\ttfamily\\normalsize},')
    output.append( 'highlight/.style = {fill=blue!20,draw},')
    output.append( 'select/.style = {fill=red!30,draw}')
    output.append('}')

    top_row = len(x)+2
    last_col = len(y)+2

    output.append('\\node\t(0-{}) at (0,{}*.75)\t{{$T$}};'.format(top_row, top_row))
    output.append('\\node\t(1-{}) at (1,{}*.75)\t{{$j$}};'.format(top_row, top_row))
    for col in range(2,last_col+1):
        output.append( '\\node\t({}-{}) at ({},{}*.75)\t{{${}$}};'.format(col, top_row, col, top_row, col-2))

    output.append('\\node\t(0-{}) at (0,{}*.75)\t{{$i$}};'.format(top_row-1, top_row-1))
    output.append('\\node\t(2-{}) at (2,{}*.75)\t{{$y[j]$}};'.format(top_row-1, top_row-1))

    for col in range(3,last_col+1):
        output.append( '\\node\t({}-{}) at ({},{}*.75)\t{{\\tt {}}};'.format(col, top_row-1, col, top_row-1, y[col-3]))

    output.append('\\node\t(0-{}) at (0,{}*.75)\t{{$0$}};'.format(top_row-2, top_row-2))
    output.append('\\node\t(1-{}) at (1,{}*.75)\t{{$x[i]$}};'.format(top_row-2, top_row-2))
    output.append('\\node\t(2-{}) at (2,{}*.75)\t{{$0$}};'.format(top_row-2, top_row-2))
    
    for col in range(2,last_col+1):
        rw = 0
        if active_nodes[0][col-2] and not template:
            output.append( '\\node\t({}-{})[highlight] at ({},{}*.75)\t{{${}$}};'.format(col, top_row-2, col, top_row-2, c[0][col-2]))
        else:
            output.append( '\\node\t({}-{}) at ({},{}*.75)\t{{${}$}};'.format(col, top_row-2, col, top_row-2, c[0][col-2]))

    for row in range(top_row-3,-1,-1):
        rw = top_row-(2+row)
        output.append('')    
        output.append('\\node\t(0-{}) at (0,{}*.75)\t{{${}$}};'.format(row, row,  rw))
        output.append('\\node\t(1-{}) at (1,{}*.75)\t{{\\tt {}}};'.format(row, row, x[rw-1]))
        for col in range(2,last_col+1):
            cl = col-2
            if active_nodes[rw][cl] and not template:
                #print('tikz (x,y)={},{} --> [{},{}]'.format(row, col, rw,cl))
                if active_nodes[rw][cl]==1:
                    output.append( '\\node[highlight]\t({}-{}) at ({},{}*.75)\t{{${}$}};'.format(col, row, col, row, c[rw][cl]))
                elif active_nodes[rw][cl]==2:
                    output.append( '\\node[select]\t({}-{}) at ({},{}*.75)\t{{$\\mathbf{{{}}}$}};'.format(col, row, col, row, c[rw][cl]))
                # explore W, NW, and N adjacent nodes: stores active edges
                if active_nodes[rw][cl]==2 and cl>0 and rw>0 and active_nodes[rw-1][cl-1]:
                    active_edges.append( '({}-{}) edge ({}-{})'.format( col-1, row+1, col, row ))
                else:
                    if cl>0 and active_nodes[rw][cl-1]:
                        active_edges.append( '({}-{}) edge ({}-{})'.format( col-1, row, col, row ))
                    if rw>0 and active_nodes[rw-1][cl]:
                        active_edges.append( '({}-{}) edge ({}-{})'.format( col, row+1, col, row ))
            else:
                output.append('\\node\t({}-{}) at ({},{}*.75)\t{{\\tt {}}};'.format(col, row, col, row, c[rw][ cl]))    
    
    output.append('\\path')
    output.append( '\n'.join(active_edges))
    output.append(';')

    # vertical
    output.append('\\draw[-,thin] (1.5,{}*.77)--(1.5,-.2);'.format(top_row))
    # horizontal
    output.append('\\draw[-,thin] (-.2,{}*.75)--({},{}*.75);'.format(top_row-1.5, last_col+.2, top_row-1.5))

    output.append('\\end{tikzpicture}')

    return '\n'.join(output)


class LCS_Test( unittest.TestCase ):


    X1=['B','D','C','A','B','A']
    Y1=['A','B','C','B','D','A','B']

    X2= ['C','G','G','A','A','T','G','C','C','G']
    Y2= ['C','G','G','T','C','G','A','G']

    X3= ['A','A','G','A','A','T','G','C','G','A']
    Y3= ['C','G','G','A','C','G','A','G']

    def test_lcs_to_tikz(self):
        print( lcs_to_tikz( ['A','C','G','A'], ['A','T','G','C','T','A']))

    def test_lcs_length_1( self ):
        length,matrix = lcs_length( self.X1, self.Y1 )
        print(length, matrix)
        self.assertEqual(reconstruct_lcs( matrix, self.X1, self.Y1), ['B','D','A','B'])


    def test_lcs_length_2( self ):
        length,matrix = lcs_length( self.X2, self.Y2 )
        self.assertEqual(reconstruct_lcs( matrix, self.X2, self.Y2), ['C','G','G','T','G','G'])


    def test_lcs_length_3( self ):
        length,matrix = lcs_length( self.X3, self.Y3 )
        self.assertEqual(reconstruct_lcs( matrix, self.X3, self.Y3), ['G','A','C','G','A'])

    def test_recursive_length_1( self ):
        self.assertEqual( recursive_length(self.X1, self.Y1), 4 )
        
    def test_recursive_length_2( self ):
        self.assertEqual( recursive_length(self.X2, self.Y2), 6 )

    def test_recursive_length_3( self ):
        self.assertEqual( recursive_length(self.X3, self.Y3), 5 )


    def test_recursive_length_memoized_1( self ):
        self.assertEqual( recursive_length_memoized(self.X1, self.Y1), 4 )
        
    def test_recursive_length_memoized_2( self ):
        self.assertEqual( recursive_length_memoized(self.X2, self.Y2), 6 )

    def test_recursive_length_memoized_3( self ):
        self.assertEqual( recursive_length_memoized(self.X3, self.Y3), 5 )


    def test_15_4_1_1( self ):
        X = [ '0', '1', '0', '1', '1', '0', '1', '1', '0' ]
        Y = [ '1', '0', '0', '1', '0','1','0','1']
        length, matrix = lcs_length( X, Y )
        self.assertEqual( reconstruct_lcs(matrix, X, Y),['0','1','0','1','0','1'])

    def test_15_4_1_2( self ):
        X = [ '0', '1', '0', '1', '1', '0', '1', '1', '0' ]
        Y = [ '1', '0', '0', '1', '0','1','0','1']
        length, matrix = lcs_length( Y, X )
        self.assertEqual(reconstruct_lcs( matrix, Y, X),['1','0','0','1','1','0'])

    def test_15_4_2_1( self):
        length, matrix = lcs_length( self.X3, self.Y3 )
        self.assertEqual(reconstruct_lcs( matrix, self.X3, self.Y3), ['G','A','C','G','A'])

#    def atest_recursive_lcs_1( self ):
#        self.assertEqual( recursive_lcs(self.X1, self.Y1, ''), 'BCBA' )
#        
#    def atest_recursive_lcs_2( self ):
#        self.assertEqual( recursive_lcs(self.X2, self.Y2, ''), 'CGGTGG' )
#
#        self.assertEqual( recursive_lcs(self.X3, self.Y3, ''), 'GACGA' )


    def test_lcs_non_deterministic_1(self):
        length,solutions = non_deterministic_memoized( self.X1, self.Y1) 
        self.assertEqual( length, 4)

    def test_lcs_non_deterministic_2(self):
        length,solutions = non_deterministic_memoized( self.X1, self.Y1) 
        self.assertEqual( solutions, ['BCAB', 'BCBA', 'BDAB'])


#for pair in [(X1,Y1), (X2,Y2), (X3,Y3)]:
#    print("--------------------")
#    print('\nX={}\nY={}\n'.format(pair[0], pair[1]))
#    matrices = lcs_length(pair[0],pair[1])
#    print(matrices[0])
#    print(matrices[1])
#
#    result = []
#    print_lcs(matrices[1], pair[0], len(pair[0]), len(pair[1]), result)
#
#    print(result)





def main():
        unittest.main()

if __name__ == '__main__':
        main()


