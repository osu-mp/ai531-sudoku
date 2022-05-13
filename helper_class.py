digits =  cols = "123456789"
rows = "ABCDEFGHI"

def cross(A, B):
	return [a + b for a in A for b in B]

squares = cross(rows, cols)