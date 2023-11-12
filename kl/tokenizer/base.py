from typing import Tuple, List

from ..lezer import add_context
from ..typing_kl import TokenBuffer

from . import core

# CONTEXT_FUNC_TYPE = Callable[[bytes, int, list[bytes], TokenBuffer], tuple[bytes, int, list[bytes]]]

@add_context(0x1, b'print', True)
def print_tokenizer(content: bytes, x: int, vars: List[bytes], token: TokenBuffer) -> Tuple[bytes, int, list[bytes]]:
    print("content:", content)
    print("x:", x)
    print("vars:", vars)
    return (content, x, vars)

@add_context(0x10, core.VAR_PATTERN, True)
def var_tokenizer(content: bytes, x: int, vars: List[bytes], token: TokenBuffer) -> Tuple[bytes, int, list[bytes]]:
    print("content:", content)
    print("x:", x)
    print("vars:", vars)
    
    if b':' in content:
        x = 0x20; vars.append(content[:-1])
    return (content, x, vars)

@add_context(0x20, core.TYPE_PARTTERN, False)
def type_tokenizer(content: bytes, x: int, vars: List[bytes], token: TokenBuffer) -> Tuple[bytes, int, list[bytes]]:
    print("content:", content)
    print("x:", x)
    print("vars:", vars)
    return (content, x, vars)
