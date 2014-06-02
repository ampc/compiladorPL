import operator
#auxd = {}
#depth = 0
#count = 0
#tempcount = 0
#labelcount = 0
# while e if precisam de ser corrigidos


class Node:

    def __init__(self, node_type, parser):
        self.type = node_type
        self.parser = parser
        
        #self.current_registry = self.parser.current_registry
        #self.current_label = self.parser.current_label
        self.symbol_table = self.parser.symbol_table
        #self.registry_iterator = self.parser.registry_iterator

        #self.file_writer = self.parser.file_writer

        self.registry_entry = ''
        self.value = None

    def semantic_analysis(self):
        pass

    def value_calculation(self):
        pass

    def produce_children(self):
        pass

    def print_code(self, string):
        self.file_writer.append(self.current_label, string)

    def producer(self):
        pass


class Int(Node):

    def __init__(self, num, parser):
        Node.__init__(self, 'INT', parser)

    def value_calculation(self, num):
        self.value = int(num)

    def producer(self):
		self.registry_entry = self.current_registry.assign_temporary()
        self.current_registry.set_temporary(self.registry_entry, self.value)
        code = 'li ' + self.registry_entry + ' ' + str(self.value)
        self.print_code(code)


class Variable(Node):

    def __init__(self, name, parser):
        Node.__init__(self, 'VARIABLE', parser)
        self.name = name
        self.exists = False
        self.var_type = ''
        self.value_calculation()

    def value_calculation(self):
		

        table = self.symbol_table
        name = self.name

        '''if table.has_key(name):
            self.exists = True
            self.var_type = table.get_type(name)
            self.registry_entry = table.get_memaddress(name)
            self.value = self.current_registry.get_register(self.registry_entry)'''

    def producer(self):
 
        pass


class BinOp(Node):
	ops={'+': operator.add,
	'-': operator.sub,
	'/': operator.div,
	'*':operator.mul,
	'==': operator.eq,
	'/=': operator.ne,
	'>':operator.gt,
	'>=':operator.ge,
	'<':operator.lt,
	'<=':operator.le,
	}
	
	def __init__(self,e1,op,e2,parser):
		Node.__init__(self,'binop')
		self.e_l=e1
		self.e_r=e2
		self.op=op
		self.mips_op=''
		
		self.int_value_calculation()

	def int_value_calculation(self):
		l=self.e_l.value
		r=self.e_r.value
		self.value=self.ops[self.operator](l,r)
		
	

class Assign(Node):
	def __init__(self,v,a,parser):
		Node.__init__(self,'assign')
		self.v=v
		self.a=a
		
	
	
class While(Node):
	def __init__(self,e):
		Node.__init__(self,'while')
		self.e=e
		
		
class If(Node):
	def __init__(self,e):
		Node.__init__(self,'if')
		self.e=e
		
		
'''
def generate(node):
    global labelcount
    global tempcount
    global count
    global depth
    global prefix
    global argcount
    label = ""
    aux = 0
    expr = ""
    labels = []
    dict = {}
    value = node.value
    # print "generate type:" + node.type +" value:" + str(node.value)
    if node.value in auxd.keys():
        value = auxd[node.value]
    if node.type == "command":
        if depth == 0:
            print "GOTO MAIN"
        for i in node.children:
            depth += 1
            expr += str(generate(i))
            depth -= 1
        if depth == 0:
            print "MAIN: "
        return expr
    if node.type == "command2":
        expr += str(generate(node.children[0]))
        return expr
    elif node.type == "command_if":
        label = "LABEL" + str(labelcount)
        labelcount += 1
        labels.insert(0, label)
        expr = "IF " + generate(node.children[0]) + " GOTO " + label + "\n"
        count = 0
        if len(node.children) == 3:
            label = "LABEL" + str(labelcount)
            labelcount += 1
            labels.insert(0, label)
            expr += "GOTO " + label + "\n"
        for v in range(len(node.children)):
            if v != 0:
                expr += str(labels.pop()) + " : " + \
                    str(generate(node.children[v]))
        return expr
    elif node.type == "command_while":
        label = "LABEL" + str(labelcount)
        labelcount += 1
        labels.insert(0, label)
        expr = label + ": "
        label = "LABEL" + str(labelcount)
        labelcount += 1
        labels.insert(0, label)
        expr += "IFFALSE " + \
            generate(node.children[0]) + " GOTO " + label + "\n"
        count = 0
        for v in range(len(node.children)):
            if v != 0:
                expr += "\n" + str(generate(node.children[v]))
        expr += "\nGOTO " + label + "\n" + label + ":"
        return expr
    elif node.type in ["expression_real", "expression_int"]:
        count += 1
        return node.value
    elif node.type == "expression_uminus":
        return value + str(generate(node.children[0]))
    elif node.type == "expression_binary":
        temp = str(generate(node.children[0]))
        if temp[0] == "t":
            aux += 1
        expr = temp + " " + value + " "
        temp = str(generate(node.children[1]))
        expr += temp
        if temp[0] == "t":
            aux += 1
        if count > 2:
            temp = "t" + str(tempcount)
            tempcount += 1
            if aux > 0:
                count -= 1
            else:
                count -= 2
            print temp + " = " + expr
            return temp
        return expr
    elif node.type == "command_assign":
        expr = str(node.children[0]) + " " + node.value + \
            " " + str(generate(node.children[1])) + "\n"
        return expr
'''
