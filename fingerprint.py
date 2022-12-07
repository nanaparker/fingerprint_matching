from arguments import FingerArgs
from finger_class import FingerData

# Retrieving Arguments
dir, sample, homeDir, mod = FingerArgs().move()

# FingerPrint Matching
printer = FingerData(dir, sample, homeDir, mod)
printer.scan()
