# -*- coding: utf-8 -*-
from collections import namedtuple #https://docs.python.org/2/library/collections.html


'''
Namedtuples são imutáveis.
Pode-se eliminar uma entrada do dicionário com del().

-----

O seguinte só é útil se quisermos que, em vez de obtermos o KeyError,
ele crie uma nova entrada tendo em conta o namedtuple table_entry.

self.table= defaultdict(table_entry)
'''


class Symbol_Table:

    def __init__(self):
        self.table_entry = namedtuple('table_entry', ['type', 'memaddress'])
        self.table = {}

    def set_value(self, name, vartype, registry):
        self.table[name] = self.table_entry(vartype, registry)

    def get_type(self, name):
        try:
            return self.table[name].type
        except KeyError:
            return False

    def get_memaddress(self, name):
        try:
            return self.table[name].memaddress
        except KeyError:
            return False

    def has_key(self, name):
        return self.table.has_key(name)
