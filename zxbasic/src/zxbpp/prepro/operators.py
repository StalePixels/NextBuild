# -*- coding: utf-8 -*-
# Operators implemented in the preprocessor


from src.zxbpp import prepro
from src.zxbpp.prepro.macrocall import MacroCall


class Concatenation(MacroCall):
    """ Implements the concatenation (a.k.a. token-paste) (##) operator.
    When in a macro body, ID1 ## ID2 becomes
    <expanded(ID1)><expanded(ID2)> (concatenated without spaces).
    Out of a macro body, ID1 and ID2 are expanded normally and "##" is
    also output as is.
    """
    def __init__(self, lineno: int, table: 'prepro.DefinesTable', left: MacroCall, right: MacroCall):
        super().__init__(lineno=lineno, table=table, id_='')
        self.left = left
        self.right = right

    def __call__(self, symbolTable: 'prepro.DefinesTable' = None) -> str:
        return self.left(symbolTable).rstrip() + self.right(symbolTable).lstrip()


class Stringizing(MacroCall):
    """ Implements stringizing operator (#). Converts the result of the
    macrocall into a BASIC string (double quotes " as delimiters, escaped as
    doubled-double quote 'Hello "dear"' => 'Hello ""dear""').
    """
    def __init__(self, lineno: int, table: 'prepro.DefinesTable', macro_call: MacroCall):
        super().__init__(lineno=lineno, table=table, id_='')
        self.macro_call = macro_call

    @staticmethod
    def stringize(s: str) -> str:
        s = s.replace('"', '""')
        return f'"{s}"'

    def __call__(self, symbolTable: 'prepro.DefinesTable' = None) -> str:
        return self.stringize(self.macro_call(symbolTable))
