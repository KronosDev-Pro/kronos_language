#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List, Callable, TypedDict, Iterable, TypeAlias
from re import Pattern
from enum import auto, Enum


class TOKEN(Enum):
    # [EXTRA]
    # $from enum import Enum, auto => from enum import Enum, auto # NO tokenizer and parser for this line, just copy
    PYTHON_CODE = auto() # if this '$' is in start line, the parser just copy line and remove it
    
    # [SYNTAX]
    # ; => \n
    EOL = auto()
    
    # [VARIABLE] 
    # x [mut] number = 16
    # x [mut] [number] = 16
    VAR = auto()
    
    TYPE = auto()
    NAME = auto()
    VALUE = auto()
    
    # [TYPE]
    # STRING => str
    # Number => int | float
    # LIST => list | tuple
    # JSON => dict
    # CHILD_TYPE => dict[str, int]
    STRING = auto()
    NUMBER = auto()
    LIST = auto()
    JSON = auto()
    CHILD_TYPE_START = auto()
    CHILD_TYPE_END = auto()
    
    # [FUNCTION]
    # func x arg1, arg2, ... {...return ...} => def x(arg1, arg2, ...): ...return ... 
    # proc x arg1, arg2, ... [...] => def x(arg1, arg2, ...): ...
    FUNC = auto()
    PROC = auto()
    FNC_ARGS = auto()
    FNC_START = auto()
    RETURN = auto()
    FNC_END = auto()
    
    # [CORE]
    # print arg1, args2
    PRINT = auto()
    PRINT_DELIMITER = auto()


class TOKEN_TYPE(TypedDict, total=False):
    token: TOKEN
    value: bytes

class TokenBuffer:
    _context: int;_token: TOKEN;_child: List[TOKEN_TYPE]
    _current_idx: int = 0;_len_child: int = 0
    
    def __init__(self, context: int) -> None: self._context = context;self._child = []
    def current(self) -> TOKEN_TYPE: return self._child[self._current_idx]
    def consume(self) -> bool: self._current_idx += 1 if (self._current_idx+1) < self._len_child else 0;return (self._current_idx+1) < self._len_child
    def add_child(self, token: TOKEN_TYPE) -> None: self._child.append(token); self._len_child += 1
    def set_token(self, token: TOKEN) -> None: self._token = token

    @property
    def get_context(self) -> int: return self._context
    @property
    def get_token(self) -> TOKEN: return self._token

    
CONTEXT_FUNC_TYPE = Callable[[bytes, int, list[bytes], TokenBuffer], tuple[bytes, int, list[bytes]]]
CONTEXT_CREATE: TypeAlias = tuple[Pattern | bytes, Iterable[CONTEXT_FUNC_TYPE]]
