from wrapper import Algorithm
from argparse import ArgumentParser, RawTextHelpFormatter
from ctypes import CDLL
from random import sample
from time import time


def main():

    op = Options()
    t = Token(op.miss_f, op.corr_f, op.dict_f)
    
    lib = Algorithm("lib.so")
    alg = lib.use(op.alg)

    if alg is None:
        print(f"invalid algorithm: {op.alg}")
        exit()

    disp(f"\nUsing: {lib.alg_name.upper()}\n", op.verbose)

    if op.input is None:
        canon_sp = tuple(zip(t.miss_sp, t.corr_sp))
        if op.n<=0:
            disp("Using all tokens from misspell", op.verbose)
        else:
            disp(f"Using {op.n} random tokens from misspell", op.verbose)
            canon_sp = sample(canon_sp, op.n)
    else:
        canon_sp = ((op.input, None),)

    avgs, skip = [0, 0, 0, 0, 0, 0], 0
    for token, canon in canon_sp:
        
        if op.skip:
            if token in t.dict_sp:
                hud = f"\nexists in dictionary: {token}" if op.verbose else token
                print(hud)
                skip+=1
                continue

        if op.verbose:
            print("\n..................................\n")
            print(f"input:     {token}")
            if canon:
                print(f"canonical: {canon}")
            else:
                print("canonical form not provided")

        retrievals, metrics = normalise(token.lower(), canon, t.dict_sp, alg)
        avgs = [m + n for m, n in zip(avgs, metrics)]

        if op.output>0 and len(retrievals)>op.output:
            disp(f"\nshowing {op.output} retrievals:\n", op.verbose)
            lexicons = sample(retrievals, op.output)
        else:
            disp("\nretrievals:\n", op.verbose)
            lexicons = retrievals
        
        print(lexicons)
        
        if op.verbose:
            print()
            print(f"matches:   {metrics[0]}")
            print(f"distance:  {-metrics[1]}")
            print(f"time (s):  {metrics[2]}")
            print(f"accuracy:  {metrics[3]}")
            print(f"precision: {metrics[4]}")
            print(f"recall:    {metrics[5]}")

    size = len(canon_sp)-skip
    if size > 1:
        avgs = tuple(map(lambda x: x/size, avgs))

        print("\n..................................\n")
        print(f"avg_matches:   {avgs[0]}")
        print(f"avg_distance:  {-avgs[1]}")
        print(f"avg_time (s):  {avgs[2]}")
        print(f"avg_accuracy:  {avgs[3]}")
        print(f"avg_precision: {avgs[4]}")
        print(f"avg_recall:    {avgs[5]}")


def normalise(token, canon, dict_sp, alg):

    start = time()
    retrievals, score = retrive(token, dict_sp, alg)
    end = time()
    timer = end - start

    retrieval_len, dict_len = len(retrievals), len(dict_sp)
    t_pos = canon in retrievals
    precision, recall, accuracy = metrics(t_pos, retrieval_len, dict_len)

    return (retrievals, (retrieval_len, score, timer, accuracy, precision, recall))


def metrics(t_pos, retrieval_len, dict_len):
    precision = (t_pos)/retrieval_len if retrieval_len else None
    recall = float(t_pos)
    accuracy = (t_pos+dict_len-retrieval_len)/dict_len if dict_len else None
    return (precision, recall, accuracy)


def retrive(token, dict_sp, alg):

    match = set()
    max_score = -float("Inf")

    for sp in dict_sp:
        score = alg(token, sp)
        if score > max_score:
            match, max_score = {sp}, score
        elif score == max_score:
            match.add(sp)

    return (match, max_score)


def disp(string, verbose):
    if verbose:
        print(string)


class Token:

    def __init__(self, miss_f, corr_f, dict_f):
        self.miss_sp = self._parse(miss_f)
        self.corr_sp = self._parse(corr_f)
        self.dict_sp = set(self._parse(dict_f))

    def _parse(self, filename):
        try:
            f = open(filename)
        except FileNotFoundError as e:
            print(e)
            exit()

        tokens = tuple(line.strip().lower() for line in f)
        f.close()
        return tokens


class Options:
    """Parse and contain command-line arguments."""

    def __init__(self):

        parser = ArgumentParser(
            description="Finds canonical form of input token",
            formatter_class=RawTextHelpFormatter)

        parser.add_argument('-m', '--miss', type=str, default='data/misspell.txt',
                            help='Finename for misspell tokens')
        parser.add_argument('-c', '--corr', type=str, default='data/correct.txt',
                            help='Filename for canonical tokens')
        parser.add_argument('-d', '--dict', type=str, default='data/dict.txt',
                            help='Filiname for token dictionary')
        parser.add_argument('-v', '--verbose', type=int, default=0,
                            help='Turn 1 to display detailed results and metrics')
        parser.add_argument('-s', '--skip', type=int, default=0,
                            help='Turn 1 to skip tokens already in reference collection')
        parser.add_argument('-i', '--input', type=str, default=None,
                            help='Input token to find canonical form')
        parser.add_argument('-n', '--sample', type=int, default=0,
                            help='Number of misspell samples to be used if Input is not specified')
        parser.add_argument('-o', '--output', type=int, default=0,
                            help='Number of output to be displayed')
        parser.add_argument('-a', '--alg', type=str, default="needleman",
                            help='Algorithm to be used\n'
                            '2_gram:    n_gram with n = 2\n'
                            '3_gram:    n_gram with n = 3\n'
                            'needleman: Needleman–Wunsch\n'
                            'waterman:  Smith–Waterman\n'
                            'editex:    Editex with Needleman–Wunsch\n'
                            'editex_sw: Editex with Smith–Waterman\n'
                            'soundex:   Soundex')
        
        args = parser.parse_args()
        self.miss_f = args.miss
        self.corr_f = args.corr
        self.dict_f = args.dict
        self.verbose = args.verbose
        self.skip = args.skip
        self.input = args.input
        self.n = args.sample
        self.output = args.output
        self.alg = args.alg


if __name__ == "__main__":
    main()
