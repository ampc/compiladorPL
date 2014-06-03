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

        self.current_label = self.parser.current_label
        self.st = self.parser.st

        #self.file_writer = self.parser.file_writer
        self.value = None
        self.table_entry = ''

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
        self.value_calculation(num)

    def value_calculation(self, num):
        self.value = int(num)

    def producer(self):
        self.print_code(code)


class Variable(Node):

    def __init__(self, name, parser):
        Node.__init__(self, 'VARIABLE', parser)
        self.name = name
        self.exists = self.st.has_key(name)
        self.type = ''

        if(self.exists):
            self.type = self.st.get_type(name)
            self.value_calculation()

    def value_calculation(self):
        table = self.st
        name = self.name

        if self.exists:
            self.var_type = table.get_type(name)
            self.value = table.get_value(name)

    def producer(self):

        pass


class BinOp(Node):
    ops = {'+': operator.add,
           '-': operator.sub,
           '/': operator.div,
           '*': operator.mul,
           '==': operator.eq,
           '/=': operator.ne,
           '>': operator.gt,
           '>=': operator.ge,
           '<': operator.lt,
           '<=': operator.le,
           }

    mops = {'+': 'add',
            '-': 'sub',
            '/': 'div',
            '*': 'mul',
            '==': 'seq',
            '/=': 'sne',
            '>': 'sgt',
            '>=': 'sge',
            '<': 'slt',
            '<=': 'sle',
            }

    def __init__(self, e1, op, e2, parser):
        Node.__init__(self, 'binop', parser)
        self.e_l = e1
        self.e_l_n = isinstance(self.e_l.value, (int, long, float))
        self.e_r = e2
        self.e_r_n = isinstance(self.e_r.value, (int, long, float))
        self.op = op
        self.mop = ''

        self.int_value_calculation()

    def int_value_calculation(self):
        l = self.e_l.value
        r = self.e_r.value
        print(l)
        print(r)
        self.value = self.ops[self.op](l, r)
        self.mop = self.mops[self.op]


class Assign(Node):

    def __init__(self, v, a, parser):
        Node.__init__(self, 'assign', parser)
        self.var = v
        self.a = a
        self.exists = self.var.exists
        self.parser = parser
        self.value_calc()

    def value_calc(self):
        self.var.value = self.a.value
        self.st.set_value(self.var.name, self.var.type,
                          self.var.value, self.parser.current_label)


class While(Node):

    def __init__(self, e):
        Node.__init__(self, 'while')
        self.e = e


class If(Node):

    def __init__(self, e, parser):
        Node.__init__(self, 'if')
        self.e = e
        self.expr_reg = self.e.table_entry
        self.else_flag = False

        self.call_label = self.parser.labels.pop()
        self.if_label = self.parser.new_label()
        self.else_label = ''

        self.branch_type = ''
        self.guess_type = ''

    def guess_type(self):
        #

    def jump(self):
        # falta registos
        # verificar se o return address esta a ser usado
        # se estiver mover a stack
        #'subi $sp, $sp, 4'
        # guardar o valor na stack
        #'sw $ra, 0($sp)'

        code = 'jal ' + self.current_label
        print(code)

    def jump_back(self):
        # falta registos
        # verificar se o return address esta a ser usado
        # obter valor do return address da stack
        # mover a stack
        code = 'jr $ra'
        print(code)

    def produce_children(self):
        if self.e.table_entry.type == 'BINARY':
            branch_flag = False
            self.e.producer(branch_flag)
        else:
            self.e.producer()

    def branch_op(self):
        branch_ops = 'bgtz ' + self.e.expr_reg + ', ' self.if_label
        print(branch_ops)
        self.parser.current_label = self.if_label

    def branch_op_else(self):
        self.else_flag = True
        self.else_label = self.parser.new_label()
        branch_ops = self.else_label
        print(branch_ops)
        self.parser.current_label = self.else_label

    def condition_control_op(self):
        self.produce_children()
        self.branch_op()
        if self.expr_reg != '':
            # completar com registos
            aaaaa

    def end_if_statement(self):
        self.jump_back()
        self.parser.current_label = self.call_label

    def producer(self):
        self.jump_back()
        self.parser.current_label = self.call_label
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
