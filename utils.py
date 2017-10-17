from Rule import Rule

substitutions={}

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
	for rule in rules:
		if rule.function_type=='->':
			left_rule=rule.parameter_1
			right_rule=rule.parameter_2
			status,result=substitute(left_rule,right_rule,term)
			if (status):
				return evaluate(rules,result)
	return term

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
	print ("Evaluated Solution:",result_rule.string)
