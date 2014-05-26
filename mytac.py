class Node:
    def __init__(self,type,children=[],value=None):
		self.type = type
		self.children = children
		self.value = value

auxd = {}
		
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
	if node.type == "program":
		if depth==0:
			print "GOTO MAIN"
		for i in node.children:
			depth+=1
			expr+= str(generate(i))
			depth-=1
		if depth ==0:
			print "MAIN: "
		return expr
	elif node.type == "declaref":
		prefix=generate(node.children[0])
		label = prefix
		print label + " : "
		expr += generate(node.children[1])
		return expr
	elif node.type == "fplist":
		dict=build(node.children[0])
		if len(node.children)>1:
			expr += generate(node.children[1])
		for i in dict.keys():
			del auxd[i]
		return expr
	elif node.type == "fcall":
		if len(node.children)>1:
			expr += generate(node.children[1])
		temp="t"+str(tempcount)
		tempcount+=1
		label = str(generate(node.children[0]))
		expr += temp + " = CALL " + label + ", "+ str(argcount)
		print expr
		return temp
	elif node.type == "vlist":
		for i in node.children:
			argcount +=1
			expr += "PARAM " + generate(i) +"\n"
		return expr
	elif node.type == "return":
		expr += "RETURN "
		for i in node.children:
			expr += generate(i)
		return expr
	elif node.type == "condition":
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
	elif node.type == "loop":
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
	elif node.type in ["boolean","variable","int"]:
		count +=1
		return value
	elif node.type == "signed":
		return value + str(generate(node.children[0]))
	elif node.type=="BinOp":
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
	elif node.type=="attrib":
		expr = str(generate(node.children[0])) + " " + value + " " + str(generate(node.children[1]))+"\n"
		return expr