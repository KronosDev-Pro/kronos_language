#!/usr/bin/python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from pathlib import Path

from generator import LIST_VALID_GENERATOR


parser = ArgumentParser(
    prog='Kronos Language (kl) v0.1.0',
    description="Kronos Language (kl) est un langage avec son transpiler embarquer"
)

parser.add_argument('-v', '--version', help='Show version of KL', action='store_true', required=False)
parser.add_argument('-f', '--file', help='filename to transpile', type=lambda p: Path(p).absolute(), required=False)
parser.add_argument('-t', '--target', choices=LIST_VALID_GENERATOR, default='python', help='Language target', required=False)
args = parser.parse_args()

from kl.main import init

if args.version:
    print(f"{parser.prog}\n")

if args.file and args.target:
    init(args.file, args.target)
