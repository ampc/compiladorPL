import operator
#auxd = {}
#depth = 0
#count = 0
#tempcount = 0
#labelcount = 0
# while e if precisam de ser corrigidos


class Node:
    index = 0
    temps = {0: False, 1: False, 2: False, 3: False, 4:
             False, 5: False, 6: False, 7: False, 8: False, 9: False}
    stack = []

    def __init__(self, node_type, parser):
        self.type = node_type
        self.parser = parser

        self.current_label = self.parser.current_label
        self.st = self.parser.st

        # self.file_writer = self.parser.file_writer
        self.value = None
        self.table_entry = ''

    def semantic_analysis(self):
        pass

    def val_calc(self):
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
        self.val_calc(num)

    def val_calc(self, num):
        self.value = int(num)

    def producer(self):
        self.print_code(code)


class Float(Node):

    def __init__(self, num, parser):
        Node.__init__(self, 'FLOAT', parser)
        self.val_calc(num)

    def val_calc(self, num):
        self.value = float(num)


class Minus(Node):

    def __init__(self, node, parser):
        Node.__init__(self, 'MINUS', parser)
        self.node = node
        self.parser = parser

        if(self.node.type == 'INT'):
            self.value = -self.node.value
        elif(self.node.type == 'VARIABLE'):
            self.value = -self.parser.st.get_value(self.node.name)


class Variable(Node):

    def __init__(self, name, parser):
        Node.__init__(self, 'VARIABLE', parser)
        self.name = name
        self.exists = self.st.has_key(name)
        self.type = ''

        if(self.exists):
            self.type = self.st.get_type(name)
            self.val_calc()

    def val_calc(self):
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
            '*': 'mult',
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

        self.int_val_calc()
        print(self.generate())

    def int_val_calc(self):
        l = self.e_l.value
        r = self.e_r.value
        self.value = self.ops[self.op](l, r)
        self.mop = self.mops[self.op]

    def generate(self):
        code = ''
		index=Node.index
		stack=Node.stack
        if(self.e_l_n):
            code += 'li $t' + str(index) + ', ' + str(self.e_l.value)
            stack.append(index)
            temps[index] = True
            index += 1
        else:
            code += 'move $t' + str(index) + ', ' + str(self.e_l.value)
            stack.append(index)
            temps[index] = True
            index += 1
        if(self.e_r_n):
            code += 'li $t' + str(index) + ', ' + str(self.e_r.value)
            stack.append(index)
            temps[index] = True
            index += 1
        else:
            code += 'move $t' + str(i) + ', ' + str(self.e_r.value)
            stack.append(index)
            temps[index] = True
            index += 1
        if(len(stack > 1)):
            code += self.mop + ' $t' + \
                str(index) + ' $t' + str(stack.pop()) + \
                ' $t' + str(stack.pop())
            temps[index] = True
            temps[index-1] = False
            temps[index-2] = False
			stack.append(index)
        return(code)


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

    # def guess_type(self):
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
        branch_ops = 'bgtz ' + self.e.expr_reg + ', ' + self.if_label
        print(branch_ops)
        self.parser.current_label = self.if_label

    def branch_op_else(self):
        self.else_flag = True
        self.else_label = self.parser.new_label()
        branch_ops = 'j ' + self.else_label
        print(branch_ops)
        self.parser.current_label = self.else_label

    def condition_control_op(self):
        self.produce_children()
        self.branch_op()
        if self.expr_reg != '':
            # completar com registos
            apagar = 1

    def end_if_statement(self):
        self.jump_back()
        self.parser.current_label = self.call_label

    def producer(self):
        self.jump()
        self.parser.current_label = self.call_label
