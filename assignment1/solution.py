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
