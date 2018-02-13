# -*- coding: utf-8 -*-
#IT's assumed that starting variable is the first typed
import helper

left, right = 0, 1

# K = "a b c"
# V = "Start A B C D Z"
# P = "Start->A B A; Start->a B D; A->a a b; A->e; B->b b a D A; C ->a; D->A"
# V = "Expr Term AddOp MulOp Factor Primary"
# K = "+ - ( ) ^ number variable"


# Factor	→ Primary	| Factor ^ Primary
# Primary	→ number	| variable	| ( Expr )
# AddOp	→ +	| −
# MulOp	→ *	| /"
# Productions = []
K, V, Productions = [],[],[]
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]


def isUnitary(rule, variables):
	if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
		return True
	return False

def isUnitarys(rule):
	if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
		return True
	return False


for nonTerminal in V:
	if nonTerminal in variablesJar:
		variablesJar.remove(nonTerminal)

#Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def START(productions, variables):
	variables.append('S0')
	return [('S0', [variables[0]])] + productions
#Remove rules containing both terms and variables, like A->Bc, replacing by A->BZ and Z->c–––––––––––TERM
def TERM(productions, variables):
	newProductions = []
	#create a dictionari for all base production, like A->a, in the form dic['a'] = 'A'
	dictionary = helper.setupDict(productions, variables, terms=K)
	for production in productions:
		#check if the production is simple
		if isUnitarys(production):
			#in that case there is nothing to change
			newProductions.append(production)
		else:
			for term in K:
				for index, value in enumerate(production[right]):
					if term == value and not term in dictionary:
						#it's created a new production vaiable->term and added to it 
						dictionary[term] = variablesJar.pop()
						#Variables set it's updated adding new variable
						V.append(dictionary[term])
						newProductions.append( (dictionary[term], [term]) )
						
						production[right][index] = dictionary[term]
					elif term == value:
						production[right][index] = dictionary[term]
			newProductions.append( (production[left], production[right]) )
			
	#merge created set and the introduced rules
	return newProductions

#Eliminate non unitry rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def BIN(productions, variables):
	result = []
	for production in productions:
		k = len(production[right])
		#newVar = production[left]
		if k <= 2:
			result.append( production )
		else:
			newVar = variablesJar.pop(0)
			variables.append(newVar+'1')
			result.append( (production[left], [production[right][0]]+[newVar+'1']) )
			i = 1
#TODO
			for i in range(1, k-2 ):
				var, var2 = newVar+str(i), newVar+str(i+1)
				variables.append(var2)
				result.append( (var, [production[right][i], var2]) )
			result.append( (newVar+str(k-2), production[right][k-2:k]) ) 
	return result
	

#Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def DEL(productions):
	newSet = []
	#seekAndDestroy throw back in:
	#        – outlaws all left side of productions such that right side is equal to the outlaw
	#        – aP the productions without outlaws 
	outlaws, productions = helper.seekAndDestroy(target='e', productions=productions)

	#add new reformulation of old rules
	for outlaw in outlaws:
		for production in productions:
			#if outlaw is present in the right side of a rule
			if outlaw in production[right]:
				#the rule is rewrited in all combination of it, rewriting "e" rather than outlaw
				newSet = newSet + helper.rewrite(outlaw, production)

	#add unchanged rules and return
	return newSet + ([productions[i] for i in range(len(productions)) 
							if productions[i] not in newSet])

def unit_routine(rules, variables):
	unitaries, result = [], []
	#controllo se una regola è unaria
	for aRule in rules:
		if isUnitary(aRule, variables):
			unitaries.append( (aRule[left], aRule[right][0]) )
		else:
			result.append(aRule)
	#altrimenti controllo se posso sostituirla in tutte le altre
	for uni in unitaries:
		for rule in rules:
			if uni[right]==rule[left]:
				result.append( (uni[left],rule[right]) )
	# for rule in rules:
	# 	result.append( (rule[left], [dictionary[symbol] if symbol in dictionary else symbol for symbol in rule[right]]) )
	return result

def UNIT(productions, variables):
	i = 0
	result = unit_routine(productions, variables)
	tmp = unit_routine(result, variables)
	while result != tmp or i < 100:
		result = unit_routine(tmp, variables)
		tmp = unit_routine(result, variables)
		i+=1
	return result


if __name__ == '__main__':
	K, V, Productions = helper.loadModel('model.txt')

	Productions = START(Productions, variables=V)
	Productions = TERM(Productions, variables=V)
	Productions = BIN(Productions, variables=V)
	Productions = DEL(Productions)
	Productions = UNIT(Productions, variables=V)
	print( helper.prettyForm(Productions) )

	open('out.txt', 'w').write(	helper.prettyForm(Productions) )

