import time

def measure_time( fun , *args , repeats = 10):

    t = time.time()
    for i in range( repeats ):
        fun( *args )
    t = time.time() - t
    return t/repeats

def compare_sol( fun1 , fun2 , *args , comp_fun = None ):
    
    s1 = fun1( *args )
    s2 = fun2( *args )

    if comp_fun is None:
        return ( s1 == s2 )
    else:
        return comp_fun( s1 , s2 )