'''
    GIVEN AN UNDIRECTED AND WEIGHTED GRAPH G( V , E ), FIND THE TREE THAT SPANS ALL NODES
    AND HAVE SMALLEST TOTAL WEIGHT

    -THE BOOK ON ALGORITHMS HAVE A CHAPTER ONLY ABOUT GRAPH ALGOS ( CH 23 ), BUT SINCE THIS ONE CAN 
    BE SOLVED WITH GREEDY APROACH IT CAN BE SEEN A CROSSOVER

    -THE GRAPH WILL BE REPRESENTED BY A SIMPLE dict() THERE ARE MORE SOPHISTICATED FRAMEWORKS FOR
    GRAPH MANEGEMENT, BUT THE FOCUS HERE IS PROBLEM SOLVING.
'''

# solution 1 ------------------------------------------
def prim_algo( V , E ):

    edges_prime = E.keys()
    edges_prime.sort( key = lambda x: E[ x ] , reversed = True )

    #----------------------------------------------------------------
    # building an adjency list, where each node has its neighbors
    # sorted in descending order
    neigh_tab = {}
    for a , b in edges_prime:
        neigh_tab[ a ] = neigh_tab.get( a , [] ) + [ b ]
        neigh_tab[ b ] = neigh_tab.get( b , [] ) + [ a ]
    #----------------------------------------------------------------

    #----------------------------------------------------------------
    # Ugly part of the code, look away!
    Visited = set()
    Ea = dict()
    x = V.pop()
    Visited.add( x )
    V.add( x )
    #----------------------------------------------------------------

    #----------------------------------------------------------------
    # Depth search. Choosing the neighbor with the smallest cost per
    # edge
    stack = [ x ]
    while stack:

        node = stack.pop()
        lst = neigh_tab[ node ]
        if not lst: continue 
        stack.append( node )

        neigh = lst.pop()
        if neigh in Visited: continue
        stack.append( neigh )

        tup = ( node , neigh )
        if not ( tup in E ):
            tup = ( neigh , node )
        Ea[ tup ] = E[ tup ]
    #--------------------------------------------------------------

    return V.copy() , Ea 

# solution 2 -----------------------------------------
def kruskal_algo( V , E ):

    Va = set()
    Ea = dict()
    
    edges_prime = E.keys()
    edges_prime.sort( key = lambda x: E[ x ] )

    for a , b in edges_prime:

        r1 = a in Va
        r2 = b in Va
        if r1*r2: continue
        if r2: Va.add( a )
        if r1: Va.add( b )
        Ea[ ( a , b ) ] = E[ ( a , b ) ]

        if Va == V: break
    
    return Va , Ea
    