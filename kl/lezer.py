#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum, auto
from re import compile, Pattern

from typing import Generator, Tuple, Any, Callable, Optional, AnyStr, Union, TypedDict, Iterable, TypeAlias

from kl.typing_kl import CONTEXT_CREATE, CONTEXT_FUNC_TYPE, TokenBuffer, TOKEN

_CONTEXT: dict[int, CONTEXT_CREATE] = {
    0x0: (b'', [])
}
_CONTEXT_ID: set[int] = set()
_CONTEXT_PARENT: list[int] = []

def add_context(
        id: int, search_params: Optional[Union[Pattern[AnyStr], bytes]] = None, defined_context: bool = False,
        append_function: bool = False, function: Optional[CONTEXT_FUNC_TYPE] = None
    ):
    def context_decorator(fn: CONTEXT_FUNC_TYPE):
        global _CONTEXT, _CONTEXT_ID, _CONTEXT_PARENT
        
        if not fn:
            if not function: raise RuntimeError('Something goes wrong with your decorator, check the params') 
            fn = function

        print(id, search_params)

        if append_function:
            if id not in _CONTEXT_ID: raise RuntimeError('The ID context missing !')
            _CONTEXT[id][1] = [*_CONTEXT[id][1], fn]    
        elif id and search_params:
            if id in _CONTEXT_ID: raise RuntimeError('The ID context has already exist !')    
            
            if defined_context:
                if id in _CONTEXT_PARENT: raise RuntimeError('The defined context is already exist !')
                _CONTEXT_PARENT.append(id)            

            _CONTEXT_ID = {*_CONTEXT_ID, id}
            _CONTEXT[id] = (search_params, [fn])
        else: raise RuntimeError('Something goes wrong with your decorator, check the params')
        return fn
    return context_decorator

    
class Lezer:
    tokens: list[TokenBuffer]
    _len_words: int
    
    def __init__(self):
        self.tokens = []
        self._len_words = 0
        
    def from_line_to_words(self, line_content: bytes) -> Generator[Tuple[int, bytes], Any, Any]:
        words: list[bytes] = line_content.split(b' ') # TODO: cahnge to regex for not split in string value containing space
        self._len_words = len(words)
        for idx, word in enumerate(words):
            yield idx, word
            
    def run_create_context(self, word: bytes, context_var: list[bytes], context_create: list[CONTEXT_FUNC_TYPE], token):
        last_return_function: Optional[tuple[bytes, int, list[bytes]]] = None
        for function in context_create:
            if last_return_function:
                entry = last_return_function[0]
                context_id = last_return_function[1]
                context_var = last_return_function[2]
            else:
                entry = word
                context_id = 0x0
                
            last_return_function = function(entry, context_id, context_var, token)
        return last_return_function
    
    def run(self, line_content: bytes):
        var_context: Iterable[bytes] = []
        len_context_parent: int = len(_CONTEXT_PARENT)
    
        token: Optional[TokenBuffer] = None
        idx_words: int = 0
        words: Generator[Tuple[int, bytes], Any, Any] = self.from_line_to_words(line_content)
        context: int = 0x0
        context_var: list[bytes] = []

        for idx_word, word in words:
            idx_context_parent: int = 1
            entry: bytes
            context_id: int = 0
            print(word, _CONTEXT_PARENT, context_id)
            while not context and idx_context_parent <= len_context_parent:
                context_params = _CONTEXT[_CONTEXT_PARENT[idx_context_parent-1]] 
                search_param = context_params[0]
                functions_params = context_params[1]
                print("fn_p", functions_params)
                
                run_create = False
                
                context_id = _CONTEXT_PARENT[idx_context_parent-1]
                token = TokenBuffer(context_id)
                
                if isinstance(search_param, Pattern):
                    if search_param.match(word.decode()): run_create = True
                else:
                    if word == search_param: run_create = True
                    
                if run_create:
                    res = self.run_create_context(word, context_var, list(functions_params), token)
                    if res:
                        print(res)
                        token = res[0]
                idx_context_parent += 1
            if token: print(token)
                        
            # if word == b"print": token['token'] = TOKEN.PRINT; context = 'print'
            # elif VAR_PATTERN.match(word.decode()) and idx_word == 0: token = {'token': TOKEN.VAR, 'value': [{'token': TOKEN.NAME, 'value': word[:-1]}]}; context = 'var'
            
            # if context == "print":
            #     if NUMERIC_VALUE.match(word.decode()): token['value'] = {'token': TOKEN.VALUE, 'value': (word, TOKEN.NUMBER)}
            #     elif ALPHA_VALUE.match(word.decode()): token['value'] = {'token': TOKEN.VALUE, 'value': (word, TOKEN.STRING)}
            #     elif word == b',': token['value'] = {'token': TOKEN.PRINT_DELIMITER, 'value': None}
            #     elif VAR_PATTERN.match(word.decode()) and word in var_context:  token['value'] = {'token': TOKEN.VAR, 'value': word}
            # elif context == "var":
            #     if word == b'=': context += ' set'
            #     elif word == b':': context += ' type'
            # elif context == 'var set':
            #     if NUMERIC_VALUE.match(word.decode()):
            #         token['value'].append({'token': TOKEN.TYPE, 'value': TOKEN.NUMBER})
            #         token['value'].append({'token': TOKEN.VALUE, 'value': word})
            #     elif ALPHA_VALUE.match(word.decode()):
            #         token['value'].append({'token': TOKEN.TYPE, 'value': TOKEN.STRING})
            #         token['value'].append({'token': TOKEN.VALUE, 'value': word})
            #     context = ""
            # elif context == 'var type':
            #     if word == b'number':
            #         token['value'].append({'token': TOKEN.TYPE, 'value': TOKEN.NUMBER})
            #     if word == b'string':
            #         token['value'].append({'token': TOKEN.TYPE, 'value': TOKEN.STRING})
            #     context += 'var type set'
            # elif context == 'var type set':
            #     if NUMERIC_VALUE.match(word.decode()):
            #         token['value'].append({'token': TOKEN.VALUE, 'value': word})
            #     elif ALPHA_VALUE.match(word.decode()):
            #         token['value'].append({'token': TOKEN.VALUE, 'value': word})
                    
            
                
            idx_words += 1
        
        # TODO: VALIDATE TOKEN LIST
        if token: token.EOL()
        return token
        

    def tokenize(self, file_content: bytes):
        for line in file_content.splitlines():
            token = self.run(line)
            if token: self.tokens.append(token)
            
            print(self.tokens)
