import math
def dist(a, b):
	return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def getwidth(t):
	#print(max(1, min(10, t)))
	return max(1, min(5, t))