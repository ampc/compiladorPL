class Node:
    def __init__(self,type,children=[],value=None):
		self.type = type
		self.children = children
		self.value = value

auxd = {}
depth=0		
count=0
		
		#while e if precisam de ser corrigidos
def generate(node):
	global labelcount
	global tempcount
	global count
	global depth
	global prefix
	global argcount
	label=""
	aux=0
	expr=""
	labels=[]
	dict={}
	value=node.value
	#print "generate type:" + node.type +" value:" + str(node.value)
	if node.value in auxd.keys():
		value=auxd[node.value]
	if node.type == "command":
		if depth==0:
			print "GOTO MAIN"
		for i in node.children:
			depth+=1
			expr+= str(generate(i))
			depth-=1
		if depth ==0:
			print "MAIN: "
		return expr
	if node.type =="command2":
		expr+=str(generate(node.children[0]))
		return expr
	elif node.type == "command_if":
		label="LABEL"+str(labelcount)
		labelcount+=1
		labels.insert(0,label)
		expr = "IF " + generate(node.children[0]) + " GOTO "+ label+"\n"
		count=0
		if len(node.children)==3:
			label="LABEL"+str(labelcount)
			labelcount+=1
			labels.insert(0,label)
			expr +="GOTO "+label+"\n"
		for v in range(len(node.children)):
			if v!=0:
				expr+=str(labels.pop())+" : "+str(generate(node.children[v]))
		return expr
	elif node.type == "command_while":
		label="LABEL"+str(labelcount)
		labelcount+=1
		labels.insert(0,label)
		expr = label +": "
		label="LABEL"+str(labelcount)
		labelcount+=1
		labels.insert(0,label)
		expr +="IFFALSE " + generate(node.children[0]) + " GOTO "+ label+"\n"
		count=0
		for v in range(len(node.children)):
			if v!=0:
				expr+="\n"+str(generate(node.children[v]))
		expr +="\nGOTO "+label+"\n"+label+":"
		return expr
	elif node.type in ["expression_real","expression_int"]:
		count +=1
		return node.value
	elif node.type == "expression_uminus":
		return value + str(generate(node.children[0]))
	elif node.type=="expression_binary":
		temp = str(generate(node.children[0]))
		if temp[0]=="t":
			aux+=1
		expr = temp + " " + value + " "
		temp = str(generate(node.children[1]))
		expr += temp
		if temp[0]=="t":
			aux+=1
		if  count>2:
			temp="t"+str(tempcount)
			tempcount+=1
			if aux>0:
				count-=1
			else:
				count-=2
			print temp+" = "+expr
			return temp
		return expr
	elif node.type=="command_assign":
		expr = str(node.children[0]) + " " + node.value + " " + str(generate(node.children[1]))+"\n"
		return expr