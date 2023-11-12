#!/usr/bin/python
# -*- coding: utf-8 -*-
from pathlib import Path
from subprocess import run
from time import monotonic_ns

from kl.lezer import Lezer
import kl.tokenizer

def init(path_file: Path, generator_name: str = ''):
    _duration: list[int] = [monotonic_ns()]
    content_file: bytes = b""

    if path_file.exists() and path_file.is_file():
        content_file = path_file.read_bytes()
    
    tokens: list[dict] | None = None
    if content_file:
        tokenizer = Lezer()
        tokenizer.tokenize(content_file)
        tokens = tokenizer.tokens

    if tokens and generator_name:
        if generator_name:
            match generator_name:
                case 'python':
                    from generator.python import Generator
                case _:
                    raise ImportError()
                
            gen = Generator(tokens)
            _duration: list[int] = [monotonic_ns() - _duration[0], monotonic_ns()]
            match generator_name:
                case 'python':
                    filename: str = f"{str(path_file).replace('.kl', '.py')}"
                    Path(filename).write_bytes(gen.result[:-1])
                    _duration[1] = monotonic_ns()
                    run(["python3", filename])
                    _duration[1] = monotonic_ns() - _duration[1]
                case _:
                    raise ImportError()
            print(f"\nKL (Transpiler) time: {_duration[0] / 1e6} ms ({_duration[0]} ns)\nExecuted time: {_duration[1] / 1e6} ms ({_duration[1]} ns)")

