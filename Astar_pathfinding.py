"""
Algorithm explained:

Its an informative algorithm that uses heuristic func to find shortest path,
so it doesn't bruteforce to find shortest path.

=Equation

F(n) = G(n) + H(n)

H(n) *Hscore-> shows the estimation of distance between node n to end node
G(n) *Gscore-> current shortest distance to get from node n to start node
F(n) *Fscore-> nodes with lower Fscore are the ones considered, assuming its closer to the end

Consider (A ----> D)
                           Node | F | G | H | Last
A-------B----              -----------------------
 \     /    |                A  | 0 | 0 | 0 |     
  \   /     |                B  | ∞ | ∞ | ∞ |
   \ C------D                C  | ∞ | ∞ | ∞ |
                             D  | ∞ | ∞ | ∞ |
Open set = {(0,A)
-> keeps track of the node that we want to look at next, starting with the start node)
-> contains (Fscore, node)
-> start graph with infinity for all points
-> points updated according to fscore considering nodes in open set
-> when a node is checked, all neighboring nodes fscores are calculated and if these values
are less than the ones in the table then the table is updated, if not then the node is ignored
-> if the end node reaches the open set with the lowest fscore, then the algorithm is done
-> check last column in table to find the shortest path


"""


