import os
import sys

from Birds_Eye_View.run import BirdsEyeView

# Use this toold to calibrate the Bird's Eye View
if "-calibrate_BEV" in sys.argv:
    s = BirdsEyeView(True)
    s.start()
    s.join()
else:
    s = BirdsEyeView(False)
    s.start()
    s.join()