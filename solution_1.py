# CS 621: Artificial Intelligence
# Assignment 1, Part 1
# By Abhijeet Dubey and Nithin S
# Note: Part 0 taken from file upload by Venkata Naga Hanumath Sai Prasad Kousika

import sys
variables=['x','y','z','u',]
constants=['0','a','b','c','d',]
binary_functions=['+','*',]
unary_functions=['s','fact',]
changes={}

# Method defined in Part 0
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




def match_terms(lhs,term):
	#print ("Compare ",left_rule.string,input_rule.string)
	global changes
	if lhs.object_type=='ufun' and term.object_type=='ufun':
		if lhs.function_type==term.function_type:
			return match_terms(lhs.parameter_1,term.parameter_1)
	elif lhs.object_type=='bfun' and term.object_type=='bfun':
		if lhs.function_type==term.function_type:
			if match_terms(lhs.parameter_1,term.parameter_1) and match_terms(lhs.parameter_2,term.parameter_2):
				return 1
	elif lhs.object_type=='con' and term.object_type=='con':
		if lhs.string==term.string:
			return 1
	elif lhs.object_type=='var' and term.object_type!='var':
		if lhs.string in changes.keys():
			if changes[lhs.string]!=term.string:
				return 0
		else:
			changes[lhs.string]=term.string
		return 1
	return 0

def replace(rule):
	global changes
	if rule.object_type=='var':
		if rule.string in changes.keys():
			return Rule(changes[rule.string])
	elif rule.object_type=='ufun':
		rule.parameter_1=replace(rule.parameter_1)
		rule.parameter_2=""
		rule.string=rule.function_type+"("+rule.parameter_1.string+")"
		return rule
	elif rule.object_type=='bfun':
		rule.parameter_1=replace(rule.parameter_1)
		rule.parameter_2=replace(rule.parameter_2)
		rule.string=rule.function_type+"("+rule.parameter_1.string+","+rule.parameter_2.string+")"
		return rule
	return rule


def substitute(lhs,rhs,term):
	global changes
	#print ("Compare and replace",left_rule.string,right_rule.string,input_rule.string)
	changes.clear()
	if match_terms(lhs,term):
		term = Rule(rhs.string)
		term = replace(term)
		return True,term
	if term.object_type=='bfun':
		status1,result1 = substitute(lhs,rhs,term.parameter_1)
		if (status1):
			term.parameter_1 = result1
		status2,result2 = substitute(lhs,rhs,term.parameter_2)
		if (status2):
			term.parameter_2 = result2
		if (status1 or status2):
			term.string=term.function_type + "(" + term.parameter_1.string + "," + term.parameter_2.string +")"
			return True,term
	if term.object_type=='ufun':
		status,result=substitute(lhs,rhs,term.parameter_1)
		if (status == True):
			term.parameter_1=result
			term.string=term.function_type+"("+result.string+")"
			return True,term

	return False,term


# def parse_tree(rules_objects,input_rule):
# 	flag=True
# 	while flag:
# 		flag=False
# 		for rule in rules_objects:
# 			if rule.function_type=='->':
# 				left_rule=rule.parameter_1
# 				right_rule=rule.parameter_2
# 				result=compare_replace(left_rule,right_rule,input_rule)
# 				if (result[0]):
# 					input_rule=result[1]
# 					#print(input_rule.string)
# 					flag=True
# 	return input_rule




def evaluate(rules,term):
	for rule in rules:
		if rule.function_type=='->':
			left_rule=rule.parameter_1
			right_rule=rule.parameter_2
			status,result=substitute(left_rule,right_rule,term)
			if (status):
				return evaluate(rules,result)
	return term






# Class defined in  Part 0
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
			try:
				self.parameter_1=Rule(rule[first_par+1:split_index[0]])
				self.parameter_2=Rule(rule[split_index[0]+1:split_index[1]])
			except Exception as error:
				print ("Error: ",error)
				sys.exit()
		elif name in unary_functions:
			self.object_type='ufun'
			self.function_type=name
			if rule[first_par]!='(' or rule[-1]!=')':
				print ("Error: Misbalance of parameters/parentheses")
				sys.exit(0)
			try:
				self.parameter_1=Rule(rule[first_par+1:-1])
				self.parameter_2=""
			except Exception  as error:
				print ("Error: ",error)
				sys.exit()
		else:
			print ("Error: '"+name+"' not found")
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


# Method defined in Part 0

def read_rules():
	file=open("rules.txt","r")
	rules=file.readlines()
	file.close()
	rules_objects=[]
	for each in rules:
		each=each.replace("\n","")
		each=each.replace(" ","")
		print(each)
		if (each):
			rule_object=Rule(each)
			rules_objects.append(rule_object)

	input_rule=input("Enter Term: ")
	input_rule_object=Rule(input_rule)
	result_rule=evaluate(rules_objects,input_rule_object)
	print ("Result: ",result_rule.string)

if __name__ == "__main__":
    read_rules()

### Done
