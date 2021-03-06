'''
-------------------------INCOMPLETE------------------------------------
Problem 6.1

A YOUNG TABLE IS A MATRIX OF SIZE MxN OF SOME ORDERABLE TYPE WHERE EACH
ROW IS SORTED IN ASCENDING ORDER, AND THE COLUMNS AS WELL. SO THE ITTEM
AT M[ 0 , 0 ] IS THE SMALLEST OF THE MATRIX.

WRITE THE FUNCTIONS FOR:
    1 - POPING THE FIRST ELEMENT OF THE TABLE, BUT KEEPING THE PROPERTY 
    CONSISTENT. ( T( N , M ) = O( M + N ) )

    2 - INSERTING A NEW ELEMENT ON THE TABLE. ( T( N , M ) = O( M + N ) )

    3 - SEARCHING A ELEMENT IN A YOUNG TABLE. T( N , M ) = O( M + N )

------------------------------------------------------------------------
'''

import numpy
from sys import maxsize
from collections import namedtuple
from math import floor
import random

# the datastructure ------------------------------------------------------------------------------
class Young_table:

    def __init__( self , m , n ):

        self.mat = numpy.ones( ( m , n ) , dtype = int )*maxsize
        self.position = ( 0 , 0 )
        self.shape = ( m , n )

    def __getitem__( self , pos ):

        i , j = pos
        m , n = self.shape
        pos_i , pos_j = self.position
        if ( i >= m ) or ( j >= n ):
            raise IndexError ( "Required position beyond table capacity" )
        elif ( n*i + j ) >= ( pos_i*n + pos_j ):
            raise IndexError ( "Required position beyond table size" )
        else:
            return self.mat[ i , j ]

    def __setitem__( self , pos , val ):

        i , j = pos
        m , n = self.shape
        pos_i , pos_j = self.position
        if ( i >= m ) or ( j >= n ):
            raise IndexError ( "Required position beyond table capacity" )
        elif ( n*i + j ) >= ( pos_i*n + pos_j ):
            raise IndexError ( "Required position beyond table size" )
        self.mat[ i , j ] = val

    def is_full( self ):

        m , n = self.shape
        pos_i , pos_j = self.position

        return ( pos_i == m -1 ) and ( pos_j == n - 1 )
    
    def clear( self ):
        self.position = ( 0 , 0 )
        self.mat = numpy.ones( self.shape , dtype = int )*maxsize
    
    def is_valid( self ):

        m , n = self.shape
        pos_i , pos_j = self.position
        if pos_i == 0 and pos_j <= 1:
            return True

        result = True
        i , j = 0 , 0 
        while result and ( n*i + j < pos_i*n + pos_j ):

            v1 = self.mat[ i , j ]

            v2 = maxsize
            if j < n - 1:
                v2 = self.mat[ i , j + 1 ]

            v3 = maxsize
            if i < m - 1:
                v3 = self.mat[ i + 1 , j ]
            
            result = ( ( v1 <= v2 ) and ( v1 <= v3 ) )

            j += 1
            if j == n:
                j = 0
                i += 1

        return result

    def left( self , i , j ):

        m , n = self.shape
        pos = n*i + j 
        lft_child = 2*pos + 1 
        return lft_child//n , lft_child%n 

    def right( self , i , j ):
        
        m , n = self.shape
        pos = n*i + j 
        rght_child = 2*pos + 2 
        return rght_child//n , rght_child%n 

    def parent( self , i , j ):

        m , n = self.shape
        pos = n*i + j 
        prnt = floor( ( pos - 1 )/2 ) 
        return prnt//n , prnt%n

    def increment_pos( self ):
        _ , n = self.shape
        i , j = self.position
        pos = n*i + j + 1
        self.position = ( pos//n , pos%n )

    def push_up( self , i , j ):

        value = self[ i , j ]
        while True:

            a = -maxsize
            if i > 0:
                a = self[ i - 1, j ] 
            
            b = -maxsize
            if j > 0:
                b = self[ i, j - 1 ] 

            m = max( a , b , value )
            if m == value: break

            pos = [ i - 1, j ]
            if m == b:
                pos = [ i, j - 1 ] 
            self[ pos ] , self[ i , j ] = self[ i , j ] , self[ pos ]

            i , j = pos

    def add( self , value ):

        if self.is_full():
            raise Exception( "self IS FULL" )
        i , j = self.position
        self.increment_pos()
        self[ i , j ] = value
        self.push_up( i , j )

    def pull_dowm( self , i , j ):

        value = self[ i , j ]
        m , n = self.shape 
        while True:

            try:
                a = self[ i + 1, j ]
            except IndexError: 
                a = maxsize
            
            try:
                b = self[ i , j + 1]
            except IndexError:
                b = maxsize

            m_val = min( a , b , value )
            if m_val == value: break

            pos = [ i + 1, j ]
            if m_val == b:
                pos = [ i, j + 1 ] 
            self[ pos ] , self[ i , j ] = self[ i , j ] , self[ pos ]
            i , j = pos

    def decrement_pos( self ):
        _ , n = self.shape
        i , j = self.position
        pos = n*i + j - 1
        self.position = ( pos//n , pos%n )

    def pop( self ):

        if self.position == ( 0 , 0 ):
            raise Exception( "self is empty")
        
        self.decrement_pos()
        i , j = self.position
        self.increment_pos()

        head = self[ 0 , 0 ]
        last = self[ i , j ]
        self[ 0 , 0 ] = last
        self.mat[ i , j ] = maxsize

        self.pull_dowm( 0 , 0 )
        self.decrement_pos()
        return head

def test1():
    T = Young_table( 8 , 7 )
    for i in range( 1000 ):

        if T.is_full():
            print( T.is_valid() )
            T.clear()

        a = random.randint( 0 , 100 )
        T.add( a )

def test2():
    T = Young_table( 20 , 20 )
    for i in range( 399 ):
        a = random.randint( 0 , 500 )
        T.add( a )
    
    for x in range( 400 ):
        try: T.pop()
        except Exception: print("Yaaaaay, it works!")
        if ( x + 1 )%10:
            print( T.is_valid() )

if __name__ == "__main__":
    # test1()
    test2()


