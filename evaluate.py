rules=[]
constants = ['a','b','c','0']
variables = ['u','v','x','y','z']
functions = ['S','+','*','f']

def parserule(rule):
    hs = rule.split(" -> ")  # lhs and rhs
    rules.append(Rule(hs[0], hs[1]))
    return

def term(stream):
	fname = stream[0]
	if fname in constants or fname in variables:
		return fname
	termdict={}
	termdict[fname]=[]
	##########################
	temp = stream[2:-1]
	cntr=0
	lefti=0
	for i in range(len(temp)):
		if temp[i] == ',' and cntr==0:
			termdict[fname].append(term(temp[lefti:i]))
			lefti=i+1
		else:
			if temp[i] == '(':
				cntr+=1
			elif temp[i] == ')':
				cntr-=1
	termdict[fname].append(term(temp[lefti:]))
	return termdict
	###################################

class Rule(object):
	#################### rule contains two main terms
	left_term = None
	right_term = None

	def __init__(self,string1,string2):
		self.left_term = term(string1)
		self.right_term = term(string2)
		return
	def __str__(self):
		return str(left_term)+","+str(right_term)

def read_rule_file():
	input_file = open("rules.txt",'r')
	input_txt = input_file.readlines()
	for rule in input_txt:
		#print("\n",rule)
		parserule(rule)
	for i in rules:
		print (str(i.left_term)+","+str(i.right_term))
	return

read_rule_file()
