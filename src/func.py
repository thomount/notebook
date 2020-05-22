import math
def dist(a, b):
	return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
def signal(x):
	return 1 if x > 0 else -1
def one_circle(x):
	while x > 180:
		x -= 360
	while x < -180:
		x += 360
	return x
def getDir(a, b):
	return (b[0]-a[0], b[1]-a[1])
def getwidth(t):
	#print(max(1, min(10, t)))
	return max(1, min(5, t))


def getdeg(a, b):
	#print(math.atan2(a[1]-b[1], b[0]-a[0])/math.pi * 180)
	return (math.atan2(a[1]-b[1], b[0]-a[0])/math.pi * 180)

keys = list(range(ord('0'), ord('9')+1))+list(range(ord('a'), ord('z')+1))+[ord(x) for x in list('[],./;\\\'`-= ')]
def getKey(s, x):
	if s == False:
		if x in keys:
			return chr(x)
		else:
			return ''
	else:
		if x >= ord('a') and x <= ord('z'):
			return chr(x).upper()
		if x >= ord('0') and x <= ord('9'):
			return [')','!','@','#','$','%','^','&','*','('][x-48]
		if x == ord('['):
			return '{'
		if x == ord(']'):
			return '}'
		if x == ord('\\'):
			return '|'
		if x == ord('/'):
			return '?'
		if x == ord(','):
			return '<'
		if x == ord('.'):
			return '>'
		if x == ord('`'):
			return '~'
		if x == ord('\''):
			return '\"'
		if x == ord('-'):
			return '_'
		if x == ord('='):
			return '+'
		if x == ord(';'):
			return ':'
		return ''

