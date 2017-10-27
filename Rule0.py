import sys

variables=['x','y','z','u',]
constants=['0','a','b','d','nl','1','2','3']
binary_functions=['+','*','app','c']
unary_functions=['s','fact','rev']



def get_middle(string):
	count=0
	pos=-1
	for i in range(0,len(string)):
		each=string[i]
		if (each=='('):
			count+=1
		elif (each==')'):
			count-=1
			if (count<1):
				break
		elif (each==',' and count==1):
			pos=i
	if (count==0 and pos!=-1):
		return (pos+1,i+1)
	else:
		print ("Invalid Rule: Paranthesis mismatch. Exiting")
		sys.exit(0)


class Rule:
	object_type=''
	function_type=''
	parameter_1=''
	parameter_2=''
	def explore(self,rule):
		first_par = rule.find('(')
		if(first_par == -1):
			 first_par = len(rule)
		name=rule[:first_par]
		#print("rule:",rule,"name:",name,"loc:",first_par)
		if '->' in rule:
			self.object_type='bfun'
			self.function_type='->'
			rules=rule.split('->')
			self.parameter_1=Rule(rules[0])
			self.parameter_2=Rule(rules[1])
		elif name in variables:
			self.object_type='var'
		elif name in constants:
			self.object_type='con'
		elif name in binary_functions:
			self.object_type='bfun'
			self.function_type=name
			split_index=get_middle(rule[first_par:])
			#print('bfun:',split_index,rule[first_par:])
			#print(rule[first_par+1:split_index[0]+first_par-1])
			#print(rule[split_index[0]+1+first_par-1:split_index[1]+first_par-1])

			try:
				self.parameter_1=Rule(rule[first_par+1:split_index[0]+first_par-1])
				self.parameter_2=Rule(rule[split_index[0]+1+first_par-1:split_index[1]+first_par-1])
			except Exception as error:
				print ("Error in parsing binary function: ",error)
				sys.exit()
		elif name in unary_functions:
			self.object_type='ufun'
			self.function_type=name
			if rule[first_par]!='(' or rule[-1]!=')':
				print ("Invalid Rule: Paranthesis mismatch. Exiting")
				sys.exit(0)
			try:
				self.parameter_1=Rule(rule[first_par+1:-1])
				self.parameter_2=""
			except Exception  as error:
				print ("Error in parsing unary function: ",error)
				sys.exit()
		else:
			print ("Please add'" + name + "'to list of function symbols/variables.")
			sys.exit(0)
	def __init__(self,string):
		self.string=string
		self.explore(self.string)

	def traverse(self):
		print ("|Type", self.object_type)
		if (self.object_type=='bfun'):
			print ("|\t"+self.string)
			print ("|\tFunction:  ",self.function_type)
			print ("|\tParameter1:",self.parameter_1.string)
			print ("|\tParameter2:",self.parameter_2.string)
			if (self.parameter_1!=""):
				self.parameter_1.traverse()
			if (self.parameter_2!=""):
				self.parameter_2.traverse()
		elif (self.object_type=='ufun'):
			print ("|\t"+self.string)
			print ("|\tFunction: ",self.function_type)
			print ("|\tParameter:",self.parameter_1.string)
			if (self.parameter_1!=""):
				self.parameter_1.traverse()
		else:
			print ("|\tValue: ", self.string)
