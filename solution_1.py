import sys
variables=['x','y','z','u',]
constants=['0','a','b','c','d',]
binary_functions=['+','*',]
unary_functions=['s','fact',]
changes={}

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
					#print(input_rule.string)
					flag=True
	return input_rule


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
		#print(name)
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
	

def read_rules():
	file=open("rules.txt","r")
	rules=file.readlines()
	file.close()
	rules_objects=[]
	for each in rules:
		each=each.replace(" ","")
		print(each)
		if (each):
			rule_object=Rule(each)
			rules_objects.append(rule_object)

	input_rule=input("Enter Term: ")
	input_rule_object=Rule(input_rule)
	result_rule=parse_tree(rules_objects,input_rule_object)
	print ("Result: ",result_rule.string)

if __name__ == "__main__":
    read_rules()
    
### Done