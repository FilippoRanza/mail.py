#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

from os import path


def parse_destination_file(file):
    with open(file) as f_in:
        for line in f_in.readlines():
            if not line:
                continue

            out = line.split()
            for i in out:
                yield i


def load_destination(dest):
    out = []
    for dst in dest:
        if path.isfile(dst):
            for d in parse_destination_file(dst):
                out.append(d)
        else:
            out.append(dst)
    return out
