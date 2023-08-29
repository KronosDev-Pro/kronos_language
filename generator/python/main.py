#!/usr/bin/python
# -*- coding: utf-8 -*-
from kl.lezer import Token_Enum

class Generator:
    _name: str = "Python Generator"
    _description: str = "convert kl tokens into python language"
    
    _list_tokens: list[dict]
    result: bytes
    
    def __init__(self, tokens: list[dict]):
        self._list_tokens = tokens
        self.result = b''
        
        if self.validate():
            self.optimize()
            self.generate()
        

    def validate(self) -> bool: return True
    def optimize(self): pass
    def generate(self):
        TokenType_to_Type: dict[Token_Enum, bytes] = {
            Token_Enum.NUMBER: b' float ',
            Token_Enum.STRING: b' str ',
        }
        
        for token in self._list_tokens:
            match token['token']:
                case Token_Enum.EOL: self.result += b'\n'
                case Token_Enum.PRINT:
                    child = token['value']
                    self.result += b'print('
                    if child['token'] == Token_Enum.VALUE:
                        if isinstance(child['value'], list) or isinstance(child['value'], tuple):
                            self.result += child['value'][0]
                    elif child['token'] == Token_Enum.VAR:
                        if isinstance(child['value'], bytes):
                            self.result += child['value']
                    elif child['token'] == Token_Enum.PRINT_DELIMITER: self.result += b', '
                    self.result += b')'
                case Token_Enum.VAR:
                    childs = token['value']
                    for child in childs:
                        if child['token'] == Token_Enum.NAME: self.result = child['value']
                        elif child['token'] == Token_Enum.TYPE: self.result += b":"+TokenType_to_Type.get(child['value']) if TokenType_to_Type.get(child['value']) else ''
                        elif child['token'] == Token_Enum.VALUE: self.result += b"= "+child['value']