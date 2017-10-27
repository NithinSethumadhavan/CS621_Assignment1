# Artificial Intelligence 
# Project 1
# Generating Parse tree for given prefix form rules given in Rules.txt
# By K Sai Prasad 173050010 and K Madhu 163059010

import sys
variables=['x','y','z','u',]
constants=['0','a','b','c','d',]
binary_functions=['+','*',]
unary_functions=['s','fact',]
changes={}
idfc_values={}
idfc_start=-1
solution_count=0

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
		print ("Error: Misbalance of parameters/parentheses")
		sys.exit(0)

def compare_tree(left_rule,input_rule):
	#print ("Compare ",left_rule.string,input_rule.string)
	global changes
	if left_rule.object_type=='ufun' and input_rule.object_type=='ufun':
		if left_rule.function_type==input_rule.function_type:
			return compare_tree(left_rule.parameter_1,input_rule.parameter_1)
	elif left_rule.object_type=='bfun' and input_rule.object_type=='bfun':
		if left_rule.function_type==input_rule.function_type:
			if compare_tree(left_rule.parameter_1,input_rule.parameter_1) and compare_tree(left_rule.parameter_2,input_rule.parameter_2):
				return 1
	elif left_rule.object_type=='con' and input_rule.object_type=='con':
		if left_rule.string==input_rule.string:
			return 1
	elif left_rule.object_type=='var' and input_rule.object_type!='var':
		if left_rule.string in changes.keys():
			if changes[left_rule.string]!=input_rule.string:
				return 0
		else:
			changes[left_rule.string]=input_rule.string
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

def idfc_compare_tree(left_rule,input_rule):
	if left_rule.object_type=='ufun' and input_rule.object_type=='ufun':
		if left_rule.function_type==input_rule.function_type:
			return compare_tree(left_rule.parameter_1,input_rule.parameter_1)
	elif left_rule.object_type=='bfun' and input_rule.object_type=='bfun':
		if left_rule.function_type==input_rule.function_type:
			return compare_tree(left_rule.parameter_1,input_rule.parameter_1) and compare_tree(left_rule.parameter_2,input_rule.parameter_2)
	elif left_rule.object_type=='con' and input_rule.object_type=='con':
		return left_rule.string==input_rule.string
	return 0

def idfc_replace(rule):
	global idfc_values
	#print ("Changes", idfc_values,rule.string)
	if rule.object_type=='var':
		if rule.string in idfc_values.keys():
			return Rule(idfc_values[rule.string])
	elif rule.object_type=='ufun':
		rule.parameter_1=idfc_replace(rule.parameter_1)
		rule.parameter_2=""
		rule.string=rule.function_type+"("+rule.parameter_1.string+")"
		return rule
	elif rule.object_type=='bfun':
		rule.parameter_1=idfc_replace(rule.parameter_1)
		rule.parameter_2=idfc_replace(rule.parameter_2)
		rule.string=rule.function_type+"("+rule.parameter_1.string+","+rule.parameter_2.string+")"
		return rule
	return rule

def compare_replace(left_rule,right_rule,input_rule):
	global changes
	#print ("Compare and replace",left_rule.string,right_rule.string,input_rule.string)
	changes.clear()
	if compare_tree(left_rule,input_rule):
		input_rule=Rule(right_rule.string)
		input_rule=replace(input_rule)
		return (1,input_rule)
	if input_rule.object_type=='ufun':
		result=compare_replace(left_rule,right_rule,input_rule.parameter_1)
		if (result[0]):
			input_rule.parameter_1=result[1]
			input_rule.string=input_rule.function_type+"("+result[1].string+")"
			return (1,input_rule)
	if input_rule.object_type=='bfun':
		result1=compare_replace(left_rule,right_rule,input_rule.parameter_1)
		if (result1[0]):
			input_rule.parameter_1=result1[1]
		result2=compare_replace(left_rule,right_rule,input_rule.parameter_2)
		if (result2[0]):
			input_rule.parameter_2=result2[1]
		if (result1[0] or result2[0]):
			input_rule.string=input_rule.function_type+"("+input_rule.parameter_1.string+","+input_rule.parameter_2.string+")"
			return (1,input_rule)
	return (0,input_rule)


def parse_tree(rules_objects,input_rule):
	flag=True
	while flag:
		flag=False		
		for rule in rules_objects:
			if rule.function_type=='->':
				left_rule=rule.parameter_1
				right_rule=rule.parameter_2
				result=compare_replace(left_rule,right_rule,input_rule)
				if (result[0]):
					input_rule=result[1]
					flag=True
	return input_rule

def check_variables(rule):
	global idfc_values
	if (rule.object_type=='var'):
		if rule.string not in idfc_values.keys():
			idfc_values[rule.string]='0'
	elif (rule.object_type=='bfun'):
		check_variables(rule.parameter_1)
		check_variables(rule.parameter_2)
	elif (rule.object_type=='ufun'):
		check_variables(rule.parameter_1)

def generate_cases(rule,pos):
	global idfc_count,idfc_values,idfc_start,idfc_depth
	if idfc_start==-1:
		idfc_start=0
		return 1
	elif pos<=len(idfc_values):
		keys=list(idfc_values.keys())
		if (len(idfc_values[keys[len(keys)-pos]])<len(rule.parameter_2.string)+4):
			idfc_values[keys[len(keys)-pos]]='s('+idfc_values[keys[len(keys)-pos]]+')'
			return 1
		elif pos!=len(idfc_values):
			idfc_values[keys[len(keys)-pos]]='0'
			return generate_cases(rule,pos+1)
		else:
			print ("No solution found :(")
	return 0

def idfs(rules_objects,rule):
	global idfc_values,solution_count
	if generate_cases(rule,1):
		#print (idfc_values)
		left_rule_object=idfc_replace(Rule(rule.parameter_1.string))
		right_rule_object=idfc_replace(Rule(rule.parameter_2.string))
		left_rule_object=parse_tree(rules_objects,left_rule_object)
		right_rule_object=parse_tree(rules_objects,right_rule_object)
		if idfc_compare_tree(left_rule_object,right_rule_object):
			print ("Omg!! Solution Found:")
			solution_count=solution_count+1
			for each in idfc_values:
				print ("\t",each,'->',idfc_values[each])
			more=input("One more ?")
			if 'y' in more or 'Y' in more or '1' in more:
				return idfs(rules_objects,rule)
			else:
				return 1
		return idfs(rules_objects,rule)
	else:
		return 0

class Rule:
	object_type=''
	function_type=''
	parameter_1=''
	parameter_2=''
	def explore(self,rule):
		name_pos=0
		for each in rule:
			if (each=='('):
				break
			name_pos+=1
		name=rule[:name_pos]
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
			split_index=get_middle(rule[name_pos:])
			try:
				self.parameter_1=Rule(rule[name_pos+1:split_index[0]])
				self.parameter_2=Rule(rule[split_index[0]+1:split_index[1]])
			except Exception as error:
				print ("Error: ",error)
				sys.exit()
		elif name in unary_functions:
			self.object_type='ufun'
			self.function_type=name
			if rule[name_pos]!='(' or rule[-1]!=')':
				print ("Error: Misbalance of parameters/parentheses")
				sys.exit(0)
			try:
				self.parameter_1=Rule(rule[name_pos+1:-1])
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

def read_rules():
	file=open("rules.txt","r")
	rules=file.readlines()
	file.close()
	rules_objects=[]
	for each in rules:
		each=each.replace("\n","")
		each=each.replace(" ","")
		if (each):
			rule_object=Rule(each)
			rules_objects.append(rule_object)

	## Part 1
	t=1
	t=int(t)
	while t:
		input_rule=input("P1: ")
		input_rule_object=Rule(input_rule)
		result_rule=parse_tree(rules_objects,input_rule_object)
		print ("Result: ",result_rule.string)
		t=t-1


	## Part 2
	input_rule=input("P2: ")
	input_rule_object=Rule(input_rule)
	check_variables(input_rule_object)
	if input_rule_object.function_type=='->':
		idfs(rules_objects,input_rule_object)
	else:
		print("Error: Not an equational rule i.e., x->y")

if __name__ == "__main__":
    read_rules()
    
### Done