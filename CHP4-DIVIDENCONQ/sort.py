from benchig_tools import *
from sys import maxsize
import random

def rec_selection( seq , n ):

    if n <= 1:
        return

    m = -maxsize
    j = -1
    for i in range( n ):
        m = max( m , seq[ i ] )
        if m == seq[ i ]: j = i
    aux = seq[ n - 1 ]
    seq[ n - 1 ] = seq[ j ] 
    seq[ j ] = aux

    rec_selection( seq , n - 1 )

def select_sort( seq ):
    n = len( seq )
    seq_prime = seq.copy()

    for j in range( n , 1 , -1 ):
        max_val = -maxsize
        pos = -1
        for i in range( j ):
            if seq_prime[ i ] > max_val:
                max_val = seq_prime[ i ]
                pos = i
        seq_prime[ j - 1 ] , seq_prime[ pos ] = seq_prime[ pos ] , seq_prime[ j - 1 ]
    return seq_prime

def partition( seq , i , j ):

    if j - i == 2 and seq[ i ] > seq[ i + 1 ]:
        seq[ i ] , seq[ i + 1 ] = seq[ i + 1 ] , seq[ i ]
        return i

    k = i
    m = k + 1
    while m < j:
        if seq[ m ] <= seq[ k ]:
            
            aux = seq[ m ]
            seq[ m ] = seq[ k + 1 ]
            seq[ k + 1 ] = aux 

            aux = seq[ k + 1 ]
            seq[ k + 1 ] = seq[ k ]
            seq[ k ] = aux

            k += 1
        m += 1
    return k

def quick_sort_rec( seq , i , j ):

    if j - i <= 1:
        return
    else:
        k = partition( seq , i , j )
        quick_sort_rec( seq , i , k )
        quick_sort_rec( seq , k + 1 , j )

def quick_sort( seq ):

    n = len( seq )
    seq_prime = seq.copy()
    quick_sort_rec( seq_prime , 0 , n )
    return seq_prime

def test_1():

    test_cases = [
        [ 2, 12, 2, 3, 11, 7, 1 ],
        [ 7, 5, 2, 3, 8, 7, 1, 9, 12, 1, 7 ],
        [ 2, 21, 2, 8, 9, 0, 3, 4, 2, 6, 3, 7 ],
        [ 2, 5, 2, 3, 11, 7, 1, 4, 2, 6, 3, 88, 91, 3 ]
    ]

    for t in test_cases:

        A = t.copy()
        A = select_sort( A )

        B = t.copy()
        B = quick_sort( B )

        eq = all( a == b for a , b in zip( A , B ) )

        s1 = "-"*50
        s2 = "select = {}".format( A )
        s3 = "quick  = {}".format( B )
        s4 = "eq = {}".format( eq )
        print("\n".join( [ s1 , s2 , s3 , s4 ] ) )

def test_2():

    N_MIN, N_MAX = 50 , 10**5
    DN = 500
    ARR = random.choices( range( 1 , 101 ) , k = N_MAX )

    ns , t1s , t2s = [] , [] , []
    start = N_MIN
    while start < N_MAX:

        ns.append( start )
        i = random.randint( 0 , N_MAX - start )
        j = i + start
        seq = ARR[ i : j ]

        t1 = measure_time( select_sort , seq )
        t1s.append( t1 )

        t2 = measure_time( quick_sort , seq )
        t2s.append( t2 )

        #-----------------------------------

        s1 = "-"*50
        s2 = "n = {}".format( start )

        m = min( start , 10 )
        s3 = "arr = " 
        s3 += " ".join( str( x ) for x in seq[ :m ] )
        if start > 10:
            s3 += " ... {}".format( seq[ -1 ] )
        
        s4 = "t1 = {}".format( t1 )
        s5 = "t2 = {}".format( t2 )

        print( "\n".join( [s1 , s2 , s3 , s4 , s5] ) )

        #---------------------------------------------
        start += DN
    return ns, t1s, t2s

if __name__ == "__main__":
    # test_1()
    test_2()
    