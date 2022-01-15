# importing required packages
from core.pose_detector import runPoseDetection
from utils.app_utils import configureApplication


# application entry point
def main():
    # get application initial state
    state = configureApplication()

    # run pose detection
    if state['config-status']:
        runPoseDetection(state)
    else:
        print('error loading application configuration')


# application starting point
if __name__ == "__main__":
    main()
