import sys

from birds_eye_view.run import BirdsEyeView
from parking_spot_labeller.run import parking_labeller
from python_IPC.IPC_client import IPC_client

calibration_flag = "-c"
labeller_flag = "-l"
ipc_client_flag = "-ipc_client"

def main():
    running_tools = []

    if labeller_flag in sys.argv:
        parking_labeller().run()
        quit()

    # Use this tool to calibrate the Bird's Eye View
    calibrate = calibration_flag in sys.argv
    # Use this tool to send image data over ipc
    ipc_on = ipc_client_flag in sys.argv

    running_tools.append(BirdsEyeView(calibrate, ipc_on))

    if ipc_on:
        running_tools.append(IPC_client())

    for tool in running_tools:
        tool.start()

    for tool in running_tools:
        tool.join()

if __name__ == "__main__":
    main()