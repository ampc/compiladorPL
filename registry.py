# -*- coding: utf-8 -*-
from collections import namedtuple

'''
NOTA: Sempre que se entrar numa nova label, NÃO É PRECISO limpar os
registos temporários. Eles só são limpos quando se muda de programa
a ser executado...
'''


class Registry:

    def __init__(self):
        self.registry_entry = namedtuple(
            'registry_entry', ['is_used', 'value'])

        self.float = {}
        self.temporary = {}
        self.saved = {}
        self.arguments = {}
        self.results = {}
        self.r_zero = self.registry_entry(True, 0)
        self.r_return_address = self.registry_entry(False, 0)
        self.r_stack_pointer = self.registry_entry(True, 2147479548)
        self.r_frame_pointer = self.registry_entry(True, 0)
        self.r_global_pointer = self.registry_entry(True, 268468224)

        self.create_float()
        self.create_temporary()
        self.create_saved()
        self.create_arguments()
        self.create_returns()

    def create_float(self):
        for i in range(0, 16):
            self.float['$f' + str(i)] = self.registry_entry(False, None)

    def create_temporary(self):
        for i in range(0, 10):
            self.temporary['$t' + str(i)] = self.registry_entry(False, None)

    def create_saved(self):
        for i in range(0, 8):
            self.saved['$s' + str(i)] = self.registry_entry(False, None)

    def create_arguments(self):
        for i in range(0, 4):
            self.arguments['$a' + str(i)] = self.registry_entry(False, None)

    def create_returns(self):
        for i in range(0, 2):
            self.results['$v' + str(i)] = self.registry_entry(False, None)

    def assign_float(self):
        for i in range(0, 16):
            reg_to_test = '$f' + str(i * 2)
            if not self.float[reg_to_test].is_used:
                result = reg_to_test
                break

        return result

    def assign_temporary(self):
        result = ''

        for i in range(0, 10):
            reg_to_test = '$t' + str(i)
            if not self.temporary[reg_to_test].is_used:
                result = reg_to_test
                break

        return result

    def assign_saved(self):
        result = ''

        for i in range(0, 8):
            reg_to_test = '$s' + str(i)
            if not self.saved[reg_to_test].is_used:
                result = reg_to_test
                break

        return result

    def assign_argument(self):
        result = ''

        for i in range(0, 4):
            reg_to_test = '$a' + str(i)
            if not self.saved[reg_to_test].is_used:
                result = reg_to_test
                break

        return result

    def get_register(self, register):
        reg_id = register[1]

        if reg_id == 'f':
            return self.get_float(register)
        elif reg_id == 't':
            return self.get_temporary(register)
        elif reg_id == 's':
            return self.get_saved(register)
        elif reg_id == 'a':
            return self.get_argument(register)
        elif reg_id == 'r':
            return self.get_return()

    def get_float(self, register):
        try:
            return self.float[register].value
        except KeyError:
            return False

    def get_temporary(self, register):
        try:
            return self.temporary[register].value
        except KeyError:
            return False

    def get_saved(self, register):
        try:
            return self.saved[register].value
        except KeyError:
            return False

    def get_argument(self, register):
        try:
            return self.arguments[register].value
        except KeyError:
            return False

    def get_return(self):
        return self.r_return_address.value

    def set_float(self, register, new_value):
        self.float[register] = self.registry_entry(True, new_value)

    def set_temporary(self, register, new_value):
        self.temporary[register] = self.registry_entry(True, new_value)

    def set_saved(self, register, new_value):
        self.saved[register] = self.registry_entry(True, new_value)

    def set_argument(self, register, new_value):
        self.arguments[register] = self.registry_entry(True, new_value)

    def set_return(self, new_value):
        self.r_return_address = self.registry_entry(True, new_value)

    def clear_register(self, register):
        reg_id = register[1]

        if reg_id == 'f':
            self.clear_float(register)
        elif reg_id == 't':
            self.clear_temporary(register)
        elif reg_id == 's':
            self.clear_saved(register)
        elif reg_id == 'a':
            self.clear_argument(register)

    def clear_float(self, register):
        self.float[register] = self.registry_entry(False, None)

    def clear_all_temporary(self):
        self.create_temporary()

    def clear_temporary(self, register):
        self.temporary[register] = self.registry_entry(False, None)

    def clear_saved(self, register):
        self.saved[register] = self.registry_entry(False, None)

    def clear_argument(self, register):
        self.arguments[register] = self.registry_entry(False, None)

    def is_float(self, register):
        reg_id = register[1]

        if reg_id == 'f':
            return True
        else:
            return False

    def is_return_used(self):
        return self.r_return_address.is_used
