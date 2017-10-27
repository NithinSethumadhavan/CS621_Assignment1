from Rule import Rule

substitutions={}
values={}
begin=-1
solutions=0

def match_terms(lhs,term):
	global substitutions
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
		if lhs.string in substitutions.keys():
			if substitutions[lhs.string]!=term.string:
				return 0
		else:
			substitutions[lhs.string]=term.string
		return 1
	return 0

def substitute_helper(rule):
	global substitutions
	if rule.object_type=='var':
		if rule.string in substitutions.keys():
			return Rule(substitutions[rule.string])
	elif rule.object_type=='ufun':
		rule.parameter_1=substitute_helper(rule.parameter_1)
		rule.parameter_2=""
		rule.string=rule.function_type+"("+rule.parameter_1.string+")"
		return rule
	elif rule.object_type=='bfun':
		rule.parameter_1=substitute_helper(rule.parameter_1)
		rule.parameter_2=substitute_helper(rule.parameter_2)
		rule.string=rule.function_type+"("+rule.parameter_1.string+","+rule.parameter_2.string+")"
		return rule
	return rule


def substitute(lhs,rhs,term):
	global substitutions
	substitutions.clear()
	if match_terms(lhs,term):
		term = Rule(rhs.string)
		term = substitute_helper(term)
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


def evaluate(rules,term):
	#print("Current Term:",term.string)
	for rule in rules:
		if rule.function_type=='->':
			left_rule=rule.parameter_1
			right_rule=rule.parameter_2
			status,result=substitute(left_rule,right_rule,term)
			if (status):
				#print(rule.string,term.string)
				return evaluate(rules,result)
	return term


def part_two_match_terms(left_rule,input_rule):
	if left_rule.object_type=='ufun' and input_rule.object_type=='ufun':
		if left_rule.function_type==input_rule.function_type:
			return match_terms(left_rule.parameter_1,input_rule.parameter_1)
	elif left_rule.object_type=='bfun' and input_rule.object_type=='bfun':
		if left_rule.function_type==input_rule.function_type:
			return match_terms(left_rule.parameter_1,input_rule.parameter_1) and match_terms(left_rule.parameter_2,input_rule.parameter_2)
	elif left_rule.object_type=='con' and input_rule.object_type=='con':
		return left_rule.string==input_rule.string
	return 0

def part_two_substitute_helper(rule):
	global values
	#print ("Changes", values,rule.string)
	if rule.object_type=='var':
		if rule.string in values.keys():
			return Rule(values[rule.string])
	elif rule.object_type=='ufun':
		rule.parameter_1=part_two_substitute_helper(rule.parameter_1)
		rule.parameter_2=""
		rule.string=rule.function_type+"("+rule.parameter_1.string+")"
		return rule
	elif rule.object_type=='bfun':
		rule.parameter_1=part_two_substitute_helper(rule.parameter_1)
		rule.parameter_2=part_two_substitute_helper(rule.parameter_2)
		rule.string=rule.function_type+"("+rule.parameter_1.string+","+rule.parameter_2.string+")"
		return rule
	return rule


def part_two_type_check(rule):
	global values
	if (rule.object_type=='var'):
		if rule.string not in values.keys():
			values[rule.string]='0'
	elif (rule.object_type=='bfun'):
		part_two_type_check(rule.parameter_1)
		part_two_type_check(rule.parameter_2)
	elif (rule.object_type=='ufun'):
		part_two_type_check(rule.parameter_1)


def part_two_search(rule,pos):
	global idfc_count,values,begin,idfc_depth
	if begin==-1:
		begin=0
		return 1
	elif pos<=len(values):
		keys=list(values.keys())
		if (len(values[keys[len(keys)-pos]])<len(rule.parameter_2.string)+4):
			values[keys[len(keys)-pos]]='s('+values[keys[len(keys)-pos]]+')'
			return 1
		elif pos!=len(values):
			values[keys[len(keys)-pos]]='0'
			return part_two_search(rule,pos+1)
		else:
			print ("No solution found :(")
	return 0

def part_two_main(rules_objects,rule):
	global values,solutions
	if part_two_search(rule,1):
		#print (values)
		left_rule_object=part_two_substitute_helper(Rule(rule.parameter_1.string))
		right_rule_object=part_two_substitute_helper(Rule(rule.parameter_2.string))
		left_rule_object=evaluate(rules_objects,left_rule_object)
		right_rule_object=evaluate(rules_objects,right_rule_object)
		if part_two_match_terms(left_rule_object,right_rule_object):
			print ("Omg!! Solution Found:")
			solutions=solutions+1
			for each in values:
				print ("\t",each,'->',values[each])
			more=input("One more ?")
			if 'y' in more or 'Y' in more or '1' in more:
				return part_two_main(rules_objects,rule)
			else:
				return 1
		return part_two_main(rules_objects,rule)
	else:
		return 0



def read_rules():
	#file=open("rules_new.txt","r")
	file=open("rules.txt","r")
	rules=file.readlines()
	file.close()
	rules_objects=[]
	for each in rules:
		each=each.replace("\n","")
		each=each.replace(" ","")
		if (each != ""):
			rule_object=Rule(each)
			rules_objects.append(rule_object)

	# input_rule=input("Enter Term: ")
	# input_rule_object=Rule(input_rule)
	# result_rule=evaluate(rules_objects,input_rule_object)
	# print ("Evaluated Solution:",result_rule.string)


	input_rule=input("P2: ")
	input_rule_object=Rule(input_rule)
	part_two_type_check(input_rule_object)
	if input_rule_object.function_type=='->':
		part_two_main(rules_objects,input_rule_object)
	else:
		print("Error: Not an equational rule i.e., x->y")
