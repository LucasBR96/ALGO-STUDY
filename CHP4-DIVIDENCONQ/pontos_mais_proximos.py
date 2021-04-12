'''
    Given a set Q of points in the Z² ( Whole numbers ) space, find the two points of that set that are the closest.
'''

from math import sqrt, floor
from sys import maxsize
import time
import random
import matplotlib.pyplot as pplt
import numpy

def distance( p1 , p2 ):

    x1 , y1 = p1
    x2 , y2 = p2

    return sqrt( ( x1 - x2 )**2 + ( y1 - y2 )**2 )

def naive_solution( Q ):

    champions = None
    m = maxsize
    n = len( Q )
    for i in range( n - 1 ):
        p1 = Q[ i ]
        for j in range( i + 1 , n ):
            p2 = Q[ j ]
            d = distance( p1 , p2 )
            if d < m:
                m = d 
                champions = ( p1 , p2 )
    return m , champions

def partition( Xs , Ys ):

    n = floor( len( Xs )/2 )
    Xl = Xs[ :n ]
    Xr = Xs[ n: ]

    last_x = Xl[ -1 ][ 0 ]
    Yl = []
    Yr = []
    for p in Ys:
        x , y = p
        if x <= last_x:
            Yl.append( p )
        else:
            Yr.append( p )
    return ( Xr , Yr ) , ( Xl , Yl )

def get_central_partition( Ys , mid , d ):

    central = []
    for x , y in Ys:
        if abs( x - mid ) <= d:
            central.append( ( x , y ) )
    return central

def recursive_call( Xs , Ys ):

    if len( Xs ) <= 3:
        return naive_solution( Xs )

    ( Xr , Yr ) , ( Xl , Yl ) = partition( Xs , Ys )

    d1 , champ1 = recursive_call( Xl , Yl )
    d2 , champ2 = recursive_call( Xr , Yr )
    d = min( d1 , d2 )
    if d == d1:
        champ = champ1
    else:
        champ = champ2

    first_x = Xr[ 0 ][ 0 ]
    last_x = Xl[ -1 ][ 0 ]
    mid = .5*( first_x + last_x )
    central = get_central_partition( Ys , mid , d )
    i = 0
    while i < len( central ) - 1:
        p = central[ i ]
        j = 1
        while j <= 7 and i + j < len( central ):
            q = central[ i + j ]
            d_prime = distance( p , q )
            if d_prime < d:
                d = d_prime
                champ = ( p , q )
            j += 1
        i += 1
    
    return d , champ

def pre_opm_solution( Q ):

    Xs = sorted( Q , key = lambda p : p[ 0 ] )
    Ys = sorted( Q , key = lambda p : p[ 1 ] )

    return Xs , Ys

def opm_solution( Q ):

    Xs , Ys = pre_opm_solution( Q )
    return recursive_call( Xs , Ys )

# For bench marking ---------------------------------------------------------------------------------

def measure_time( fun , *args , repeats = 10):

    t = time.time()
    for i in range( repeats ):
        fun( *args )
    t = time.time() - t
    return t/repeats

def generate_Q( n , max_x , max_y ):

    Q = []
    for i in range( n ):
        x = random.randint( 0 , max_x )
        y = random.randint( 0 , max_y )

        Q.append( ( x , y ) )
    return Q

def truncate(num, n):
    integer = int(num*( 10**n ))/( 10**n )
    return float(integer)

def pplotar_resultados( Ns , Ingenuas, Opm ):
    
    Ns_arr = numpy.array( Ns )
    Ingenuas_arr = numpy.array( Ingenuas )
    Opm_arr = numpy.array( Opm )

    pplt.plot( Ns_arr , Ingenuas_arr , color = "blue" , label = "solução ingênua"  )
    pplt.plot( Ns_arr ,      Opm_arr , color = "red" , label = "solução ingênua"  )

    pplt.xlabel( "Tamanho do input")
    pplt.ylabel( "Tempo Ms")

    pplt.show()

# benchmarking em si ----------------------------
def bench( ):

    mult = 1000
    max_x = 100
    max_y = 100

    N = 1500
    # N = 25
    Ns = []
    Tempos_ingenuos = []
    Tempos_opm = []

    for i in range( 10 , N + 1, 10):

        print( "-"*25 )
        print( "resultado para i = {}".format( i ) )
        Ns.append( i )

        Q = generate_Q( i , max_x , max_y )

        dt = measure_time( naive_solution , Q )*( 10**3 )
        dt_s = str( dt ).rstrip()
        print( "tempo para ingenua: {}".format( dt_s[ :8 ] ) )
        Tempos_ingenuos.append( dt )

        dt = measure_time( opm_solution , Q )*( 10**3 )
        dt_s = str( dt ).rstrip()
        print( "tempo para otimizada: {}".format( dt_s[ : 8] ) )
        Tempos_opm.append( dt )

    pplotar_resultados( Ns , Tempos_ingenuos, Tempos_opm )


if __name__ == "__main__":
    bench()
