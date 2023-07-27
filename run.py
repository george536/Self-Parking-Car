import sys

from birds_eye_view.run import BirdsEyeView
from parking_spot_labeller.run import parking_labeller

calibration_flag = "-c"
labeller_flag = "-l"

def main():
    running_tools = []

    if labeller_flag in sys.argv:
        parking_labeller().run()
        quit()

    # Use this tool to calibrate the Bird's Eye View
    calibrate = calibration_flag in sys.argv
    running_tools.append(BirdsEyeView(calibrate))

    for tool in running_tools:
        tool.start()
        tool.join()
        
        
if __name__ == "__main__":
    main()