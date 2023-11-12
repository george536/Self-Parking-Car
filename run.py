"""Args utilization"""
import sys

from birds_eye_view.run import BirdsEyeView
from parking_spot_labeller.run import ParkingSpotLabeller
from python_ipc.IpcClient import IpcClient

CALIBRATION_FLAG = "-calibrate"
LABELLER_FLAG = "-labeller"
LOAD_SPOTS_FLAG = "-load_spots"
IPC_CLIENT_FLAG = "-ipc_client"

def main():
    """Starts Carla tools"""
    running_tools = []

    if LABELLER_FLAG in sys.argv:
        ParkingSpotLabeller().run()
        sys.exit()

    # Use this tool to calibrate the Bird's Eye View
    calibrate = CALIBRATION_FLAG in sys.argv
    # Use this tool to send images data over ipc
    ipc_on = IPC_CLIENT_FLAG in sys.argv
    # use this to load saved spots into world
    should_load_spots = LOAD_SPOTS_FLAG in sys.argv

    running_tools.append(BirdsEyeView(calibrate, ipc_on, should_load_spots))

    if ipc_on:
        running_tools.append(IpcClient())

    for tool in running_tools:
        tool.start()

    for tool in running_tools:
        tool.join()

if __name__ == "__main__":
    main()
