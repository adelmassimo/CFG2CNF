import re
import itertools

left, right = 0, 1

def union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list

def loadModel(modelPath):
	file = open(modelPath).read()
	K = (file.split("Variables:\n")[0].replace("Terminals:\n","").replace("\n",""))
	V = (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n","").replace("\n",""))
	P = (file.split("Productions:\n")[1])

	return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)
#Make production easy to work with
def cleanProduction(expression):
	result = []
	#remove spaces and explode on ";"
	rawRulse = expression.replace('\n','').split(';')
	
	for rule in rawRulse:
		#Explode evry rule on "->" and make a couple
		leftSide = rule.split(' -> ')[0].replace(' ','')
		rightTerms = rule.split(' -> ')[1].split(' | ')
		for term in rightTerms:
			result.append( (leftSide, term.split(' ')) )
	return result

def cleanAlphabet(expression):
	return expression.replace('  ',' ').split(' ')

def seekAndDestroy(target, productions):
	trash, ereased = [],[]
	for production in productions:
		if target in production[right] and len(production[right]) == 1:
			trash.append(production[left])
		else:
			ereased.append(production)
			
	return trash, ereased
 
def setupDict(productions, variables, terms):
	result = {}
	for production in productions:
		#
		if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
			result[production[right][0]] = production[left]
	return result


def rewrite(target, production):
	result = []
	#get positions corresponding to the occurrences of target in production right side
	#positions = [m.start() for m in re.finditer(target, production[right])]
	positions = [i for i,x in enumerate(production[right]) if x == target]
	#for all found targets in production
	for i in range(len(positions)+1):
 		#for all combinations of all possible lenght phrases of targets
 		for element in list(itertools.combinations(positions, i)):
 			#Example: if positions is [1 4 6]
 			#now i've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
 			#erease position corresponding to the target in production right side
 			tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
 			if tadan != []:
 				result.append((production[left], tadan))
	return result

def dict2Set(dictionary):
	result = []
	for key in dictionary:
		result.append( (dictionary[key], key) )
	return result

def pprintRules(rules):
	for rule in rules:
		tot = ""
		for term in rule[right]:
			tot = tot +" "+ term
		print(rule[left]+" -> "+tot)

def prettyForm(rules):
	dictionary = {}
	for rule in rules:
		if rule[left] in dictionary:
			dictionary[rule[left]] += ' | '+' '.join(rule[right])
		else:
			dictionary[rule[left]] = ' '.join(rule[right])
	result = ""
	for key in dictionary:
		result += key+" -> "+dictionary[key]+"\n"
	return result