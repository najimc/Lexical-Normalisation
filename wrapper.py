from ctypes import CDLL
from os.path import abspath


class Algorithm:

    def __init__(self, lib):
        self.lib = CDLL(abspath(lib))
        self.args = None
        self.alg_name = ""
        self.pad = False

    def needleman_wunsch(self, token1, token2):
        return self.lib.needleman_wunsch(token1.encode('utf-8'), len(token1),
            token2.encode('utf-8'), len(token2), False)

    def smith_waterman(self, token1, token2):
        return self.lib.smith_waterman(token1.encode('utf-8'), len(token1),
            token2.encode('utf-8'), len(token2), False)

    def editex(self, token1, token2):
        alg = self.lib.needleman_wunsch if self.args else self.lib.smith_waterman
        return alg(token1.encode('utf-8'), len(token1), token2.encode('utf-8'),
            len(token2), True)

    def soundex(self, token1, token2):
        return self.lib.soundex(token1.encode('utf-8'), len(token1),
            token2.encode('utf-8'), len(token2), False)

    def n_gram(self, token1, token2):
        n = self.args
        if self.pad:
            token1, token2 = (n-1)*"_"+token1+(n-1)*"_", (n-1)*"_"+token2+(n-1)*"_"
        return -self.lib.n_gram(token1.encode('utf-8'), len(token1),
            token2.encode('utf-8'), len(token2), n)

    def use(self, alg):

        alg = alg.lower()

        if alg in {"needleman_wunsch", "needleman", "nm"}:
            self.alg_name = "Needleman Wunsch"
            return self.needleman_wunsch

        if alg in {"smith_waterman", "waterman", "sw"}:
            self.alg_name = "Smith Waterman"
            return self.smith_waterman

        if alg in {"editex", "editex_nm", "e", "e_nm", "enm"}:
            self.args, self.alg_name = True, "Editex (global)"
            return self.editex

        if alg in {"editex_sw", "editexsw", "e_sw", "esw"}:
            self.args, self.alg_name = False, "Editex (local)"
            return self.editex

        if "sound" in alg:
            self.alg_name = "Soundex"
            return self.soundex

        if "gram" in alg:
            try:
                self.args = int(alg[0])
            except ValueError:
                self.args = 2

            self.alg_name = f"{self.args}-Gram"
            if "p" in alg:
                self.pad = True
                self.alg_name += " with Padding"

            return self.n_gram

        return None
