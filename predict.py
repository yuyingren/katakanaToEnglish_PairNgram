#!/usr/bin/env python
"""Rewrites FST examples.

This script assumes the input is provided one example per line."""

__author__ = "Kyle Gorman"

import argparse
import functools
import logging
import multiprocessing
import re

from typing import Iterator

import pynini
from pynini.lib import rewrite


TOKEN_TYPES = ["byte", "utf8"]



EngLex=[]
with open("data/EnglishDict.txt", "r") as file:
    for i in file:
        EngLex.append(i.rstrip())

class Rewriter:
    def __init__(
        self,
        fst: pynini.Fst,
        input_token_type: pynini.TokenType,
        output_token_type: pynini.TokenType,
    ):
        self.rewrite = functools.partial(
            rewrite.top_rewrites,
            rule=fst,
            nshortest=5,
            input_token_type=input_token_type,
            output_token_type=output_token_type,
        )

    def __call__(self, i: str) -> str:
        try:
            return self.rewrite(i)
        except rewrite.Error:
            return "<composition failure>"


def _reader(path: str) -> Iterator[str]:
    """Reads strings from a single-column filepath."""
    with open(path, "r") as source:
        for line in source:
            yield line.rstrip()

def Lexfilter(hypo_list):
   
    # hypo_line_sub=re.sub("\[|\]|'", "", hypo_line.rstrip())
    # hypths=hypo_list.split(", ")
    
    real=[]
    for i in hypo_list:
        phrase=i.split(" ")
        if all(word in EngLex for word in phrase):
            real.append(i)
    if real!=[]:
        return real[0]
    if real ==[]:
        return hypo_list[0]

def main(args: argparse.Namespace) -> None:
    fst = pynini.Fst.read(args.fst_path)
    input_token_type = (
        args.input_token_type
        if args.input_token_type in TOKEN_TYPES
        else pynini.SymbolTable.read_text(args.input_token_type)
    )
    output_token_type = (
        args.output_token_type
        if args.output_token_type in TOKEN_TYPES
        else pynini.SymbolTable.read_text(args.output_token_type)
    )
    rewriter = Rewriter(
        fst,
        input_token_type=input_token_type,
        output_token_type=output_token_type,
    )
    LexResult=[]
    with multiprocessing.Pool(args.cores) as pool:
        for line in pool.map(rewriter, _reader(args.word_path)):
            LexResult.append(Lexfilter(line))
    # with open("results/kataEng_Test.txt", "w") as resfile:
    for i in LexResult:
        print(i)
            
            


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--word_path", required=True, help="path to file of words to rewrite"
    )
    parser.add_argument(
        "--fst_path", required=True, help="path to rewrite fst FST"
    )

    parser.add_argument(
        "--cores",
        type=int,
        default=multiprocessing.cpu_count(),
        help="number of cores (default: %(default)s)",
    )
    parser.add_argument(
        "--input_token_type", default="utf8", help="input_token type"
    )
    parser.add_argument(
        "--output_token_type", default="utf8", help="output_token type"
    )
    main(parser.parse_args())
