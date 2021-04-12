import numpy
import matplotlib.pyplot as pplt
from math import ceil , floor
import random
import time
from benchig_tools import measure_time , compare_sol

'''

    Having two polynoms A and B, as
    A( x ) = a0 + a1*x + a2x² + .... + an*( x^n )
    B( x ) = b0 + b1*x + b2x² + .... + bn*( x^n )

    Compute the product between a and b.

    obs: A and B will be treated as vector, like:
    A[ i ] = ai

'''

def naive_solution( A , B ):

    '''
    O( n²), obviously
    '''
    result = [0]*( len( A ) + len( B ) - 1 )
    for i , a in enumerate( A ):
        for j , b in enumerate( B ):
            result[ i + j ] += a*b 
    return result

def particiona_vetor( P ):

    n = floor( len( P )/ 2 )
    lft , rght = [] , []
    for i , x in enumerate( P ):
        if i < n: lft.append( x )
        else: rght.append( x )
    return lft , rght , n

def soma_pol( A , B ):

    n = max( len( A ) , len( B ) )
    result = [ 0 ]*n

    for i in range( n ):

        a = 0
        if i < len( A ):
            a = A[ i ]

        b = 0
        if i < len( B ):
            b = B[ i ]
        
        result[ i ] = a + b
    return result

def opm_solution( A , B ):

    '''
    The Tricky one. 
    '''

    if len( A )*len( B ) <= 9:
        return naive_solution( A , B )
    
    part_pt = min( len( A ) , len( B ) )
    part_pt = floor( part_pt/2 )

    A0, A1 = [] , [] 
    for i , a in enumerate( A ):
        if i < part_pt:
            A0.append( a )
        else:
            A1.append( a )

    B0, B1 = [] , [] 
    for i , b in enumerate( B ):
        if i < part_pt:
            B0.append( b )
        else:
            B1.append( b )

    C1 = opm_solution( A0 , B0 )
    C2 = opm_solution( A1 , B1 )
    C_sum = soma_pol( C1 , C2 )

    A_prime = soma_pol( A0 , A1 )
    B_prime = soma_pol( B0 , B1 )
    Aux = opm_solution( A_prime , B_prime )

    C_prime = [ -x for x in C_sum ]
    C = soma_pol( C_prime , Aux )

    resultado = [0]*( len( A ) + len( B ) - 1 )
    for i , a in enumerate( C1 ):
        resultado[ i ] += a 
    
    for i , b in enumerate( C ):
        resultado[ i + part_pt ] += b

    for i , c  in enumerate( C2 ):
        resultado[ i + 2*part_pt ] += c  


    return resultado

# For benching ----------------------------------------------

def generate_pol( n , c_max , c_min ):

    return [ random.randint( c_min , c_max ) for i in range( n ) ]

def pplotar_resultados( Ns , Ingenuas, Opm ):
    
    Ns_arr = numpy.array( Ns )
    Ingenuas_arr = numpy.array( Ingenuas )
    Opm_arr = numpy.array( Opm )

    pplt.plot( Ns_arr , Ingenuas_arr , color = "blue" , label = "solução ingênua"  )
    pplt.plot( Ns_arr ,      Opm_arr , color = "red" , label = "solução ingênua"  )

    pplt.xlabel( "Tamanho do input")
    pplt.ylabel( "Tempo Ms")

    pplt.show()

def compara_polinomios( A , B ):

    if len( A ) != len( B ): return False

    result = True
    for a , b in zip( A , B ):
        if a != b:
            result = False
            break
    return result

# benching on itself ---------------------------------

def bench( ):

    c_max = 15
    c_min = 1

    N = 5000
    # N = 25
    Ns = []
    Tempos_ingenuos = []
    Tempos_opm = []

    for i in range( 50 , N + 1, 50 ):

        print( "-"*50 )
        print( "resultado para i = {}".format( i ) )
        Ns.append( i )

        A = generate_pol( i , c_max , c_min )
        B = generate_pol( i , c_max , c_min )

        dt = measure_time( naive_solution , A , B )*( 10**3 )
        dt_s = str( dt ).rstrip()
        print( "tempo para ingenua: {}".format( dt_s[ :8 ] ) )
        Tempos_ingenuos.append( dt )

        dt = measure_time( opm_solution , A , B )*( 10**3 )
        dt_s = str( dt ).rstrip()
        print( "tempo para otimizada: {}".format( dt_s[ : 8] ) )
        Tempos_opm.append( dt )

        res = compare_sol( naive_solution , opm_solution , A , B, comp_fun = compara_polinomios )
        print( res )

    pplotar_resultados( Ns , Tempos_ingenuos, Tempos_opm )


if __name__ == "__main__":
    bench()

    # A = [ 1 , 2 , -1 , 3 ]
    # B = [ 2 , -1 , 1 , -2 ]

    # res = compare_sol( naive_solution , opm_solution , A , B, comp_fun = compara_polinomios )
    # print( res )

    # A.append( 8 )
    # res = compare_sol( naive_solution , opm_solution , A , B, comp_fun = compara_polinomios )
    # print( res )