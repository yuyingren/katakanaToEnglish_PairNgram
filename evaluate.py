#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:20:25 2022

@author: yuyingren
"""
import logging

import numpy

import argparse




def edit_distance(x, y) -> int:
    # For a more expressive version of the same, see:
    #
    #     https://gist.github.com/kylebgorman/8034009
    idim = len(x) + 1
    jdim = len(y) + 1
    table = numpy.zeros((idim, jdim), dtype=numpy.uint8)
    table[1:, 0] = 1
    table[0, 1:] = 1
    for i in range(1, idim):
        for j in range(1, jdim):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                c1 = table[i - 1][j]
                c2 = table[i][j - 1]
                c3 = table[i - 1][j - 1]
                table[i][j] = min(c1, c2, c3) + 1
    return int(table[-1][-1])



def score(gold, hypo):

    edits = edit_distance(gold, hypo)
    if edits:
        logging.warning(
            "Incorrect prediction:\t%r (predicted: %r)",
            " ".join(gold),
            " ".join(hypo),
        )
    return (edits, len(gold))

def main(args: argparse.Namespace):
    
    gold_data=[]
    with open(args.gold_path, "r") as source:
        for line in source:
            gold_data.append(line.rstrip().split("\t")[1])
            
    hypo_data=[]
    with open(args.hypo_path, "r") as preds:
        for line in preds:
            hypo_data.append(line.rstrip())
    gold_hypo_pairs=list(zip(gold_data, hypo_data))
    
    
    correct=0
    incorrect=0
    total_edits=0
    total_length=0
    
    for i in gold_hypo_pairs:
        e=score(i[0], i[1])[0]
        l=score(i[0], i[1])[1]
        if e==0:
            correct+=1
        else:
            incorrect+=1
        total_edits +=e
        total_length +=l
        
    print(f"WER:\t{100 * incorrect / (correct + incorrect):.2f}")
    print(f"CER:\t{100 * total_edits / total_length:.2f}")

if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Evaluates sequence model")
    parser.add_argument("--gold_path", help="path to gold TSV file")
    parser.add_argument("--hypo_path", help="path to hypo TXT file")

    main(parser.parse_args())