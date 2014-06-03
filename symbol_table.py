# -*- coding: utf-8 -*-
from collections import namedtuple

class Symbol_Table:
    def __init__(self):
        self.table_entry= namedtuple('table_entry', ['type', 'value', 'label'])
        self.table= {}
    
    def set_value(self, name, vartype, value, label):
        self.table[name]= self.table_entry(vartype, value, label)
    
    def get_type(self, name):
        try:
            return self.table[name].type
        except KeyError:
            return False
    
    def get_value(self, name):
        try:
            return self.table[name].value
        except KeyError:
            return False
    
    def get_creation_label(self, name):
        try:
            return self.table[name].creation_label
        except KeyError:
            return False
    
    def get_keys(self):
        return self.table.keys()
    
    def has_key(self, name):
        return self.table.has_key(name)
    
    def remove_symbol(self, symbol):
        self.table.pop(symbol)