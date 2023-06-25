import os
import sys
import signal

from birds_eye_view.run import BirdsEyeView


def main():
    # Use this toold to calibrate the Bird's Eye View
    calibrate = "-c" in sys.argv

    # Use this tool to run the Bird's Eye View
    s = BirdsEyeView(calibrate)
    s.start()
    s.join()
        
        
if __name__ == "__main__":
    main()