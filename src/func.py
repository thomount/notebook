import math
def dist(a, b):
	return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def getwidth(t):
	#print(max(1, min(10, t)))
	return max(1, min(5, t))


def getdeg(a, b):
	print(math.atan2(a[1]-b[1], b[0]-a[0])/math.pi * 180)
	return (math.atan2(a[1]-b[1], b[0]-a[0])/math.pi * 180)