# Lexical Normalisation

Finds the canonical form for each token within a document. The program uses token matching algorithms and evaluates their performance using retrieval evaluation metrics.

## Instructions

### Build

Have `GCC` and `Make` installed in your machine (for Windows, these can be downloaded from [Cygwin](https://www.cygwin.com/) or [MinGW](http://www.mingw.org/)), then open the terminal and run:

```bash
Make
```

This will compile and create the necessary shared C library which is used by the program through Python Ctypes wrappers.

### Usage

Use the following command to run the program ([Python 3](https://www.python.org/downloads/) or higher must be installed):

```bash
python main.py
```

This predicts the best match(es) for each of the input tokens, with respect to a reference collection.

#### Optional arguments

```bash
python main.py [-h] [-m MISS] [-c CORR] [-d DICT] [-v VERBOSE] [-s SKIP] [-i INPUT] [-n SAMPLE] [-o OUTPUT] [-a ALG]
```

##### `[-a ALG]`

Sets one of the following algorithms to be used by the program:

Algorithm | `ALG`
--- | ---
Needleman Wunsch Global Alignment | `needleman` or `nm` (Default)
Smith Waterman Local Alignment | `waterman` or `sw`
Editex with Global Alignment | `editex` or `e`
Editex with local Alignment | `editex_sw` or `esw`
Soundex | `soundex`
n-Gram | `n_gram` where n is 2 or 3

For example:

```bash
python main.py -a 2_gram
```

finds the best match(es) for each of the input tokens using 2-Grams algorithm.

##### `[-v VERBOSE]`

If turned 1, displays detailed output and evaluates the predictions with respect to their corresponding canonical forms based on the following evaluation metrics:

* Precision
* Recall
* Accuracy
* Running time

##### `[-s SKIP]`

If turned 1, only evaluates tokens if they do not exist in the reference collection.

##### `[-i INPUT]`

Uses only one input token to be matched (if not specified, uses all input tokens from the document).

```bash
python main.py -i word
```

finds the best matches for `"word"`.

##### `[-n SAMPLE]`

Uses `n` random samples of input tokens to be matched (uses all input tokens if not specified).

```bash
python main.py -n 100
```

uses 100 random input tokens to be matched.

##### `[-o OUTPUT]`

Sets the maximum number of retrievals to be displayed (shows all retrievals if not specified).

```bash
python main.py -o 5
```

displays at most 5 random retrievals if there are more than 5 matches.

##### `[-m MISS] [-c CORR] [-d DICT]`

Sets the documents for input, corresponding canonical form and reference collection respectively. The defaults are:

* `-m`: `data/misspell`
* `-c`: `data/correct`
* `-d`: `data/dict`

##### `[-h HELP]`

Shows the help message and further information.

#### Example Usage

```bash
python main.py --alg needleman --sample 100 --skip 1 --verbose 1 --output 10
```

or

```bash
python main.py -a nm -n 100 -s 1 -v 1 -o 10
```

Uses Needleman Wunsch Global Alignment to match 100 random tokens that are not in the reference collection, and for each token, displays the detailed output metrics of at most 10 retrievals.

## Author

* [Najim Islam](https://github.com/najimc)
