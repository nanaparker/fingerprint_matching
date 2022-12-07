import argparse

class FingerArgs:

    def __init__(self):
        self.parse = argparse.ArgumentParser(
            prog="fingerprint.py",
            description="This program matches a fingerprint with already existing fingerprints",
        )

        self.parse.add_argument("-f", "--sampleFile", required=True,
                                help="File path to sample fingerprint file")
        self.parse.add_argument("-d", "--fDir", required=True,
                                help="File path to stored fingerprints")
        self.parse.add_argument("--home", required=True,
                                help="Directory currently in use")
        self.parse.add_argument("-m", "--modulo", default=1000,
                                help="Defines chunk size for folders")


    def move(self):
        args = self.parse.parse_args()
        return args.fDir, args.sampleFile, args.home, args.modulo