import matrix

m = [[1,2],[3,4],[5,6]]
q = [[1,1],[5,4],[3,7]]
d = [[1, 2, 3], [4, 5, 6]]
dd = [[1,2], [3, 4]]
ddd1 = [[3, 4], [5, 7]]
c = 2
v = [2,3,4]


print( matrix.scalar_multiplication(m,c) )
print("\n")
print( matrix.addition(m,q) )
print("\n")
print( matrix.subtraction(m,q) )
print("\n")
print( matrix.vector_multiplication(v,m) )
print("\n")
print( matrix.matrix_multiplication(m, d) )
print("\n")
print( matrix.transposition(m) )
print("\n")
print( matrix.determinant(dd) )
print("\n")
print( matrix.inversion(ddd1) )



