def TimeChecker(input_time):
	n = input_time
	n = n.replace(':', ' ')
	n = n.split()
	print(n)
	a,b = n 
	
	if int(a) >= 0 and int(a) <= 24 and int(b) >=0 and int(b) <= 60:
		return True
	return False


