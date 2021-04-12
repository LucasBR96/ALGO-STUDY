import numpy
from sys import maxsize
from collections import namedtuple

class Young_table:

    def __init__( self , m , n ):

        self.mat = numpy.ones( ( m , n ) , dtype = int )*maxsize
        self.position = ( 0 , 0 )
        self.shape = ( m , n )

    def __getitem__( self , i , j ):

        m , n = self.shape
        pos_i , pos_j = self.position
        if ( i >= m ) or ( j >= n ):
            raise IndexError "Required position beyond table capacity"
        elif( i >= pos_i ) or ( j >= pos_j ) :
            raise IndexError "Required position beyond table size"
        else:
            return self.mat[ i , j ]
    
    def is_full( self ):

        m , n = self.shape
        pos_i , pos_j = self.position

        return ( pos_i == m -1 ) and ( pos_j == n - 1 )
    
    def is_valid( self ):

        m , n = self.shape
        pos_i , pos_j = self.position
        if pos_i == 0 and pos_j <= 1:
            return True

        result = True
        i , j = 0 , 0 
        while result and ( i != pos_i or j != pos_j ):

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
        return prnt//n , rght_child%n


class smart_table( Young_table ):

    def __init__( self , m , n ):
        super().__init__( m , n )
    
    def upwards( self, i , j ):

        
