# importing required packages
import enum, json
from utils.dir_helper import configureApplicationDirectories, isPathExists, configureFilePaths


# Object for dict
class ObjDict(dict):
    """
    Objdict class to conveniently store a state
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


# pose detection source type enumeration
class PoseDetectionSourceType(enum.Enum):
    VIDEO = 1
    WEBCAM = 2


# Function to read application configuration file
def loadApplicationConfiguration(state):
    if isPathExists(state['config-file-name']):
        with open(state['config-file-name']) as config_file:
            try:
                state['app-config'] = json.load(config_file)
                state['config-status'] = True
            except ValueError as error:
                print(error)

    return state


def configureDetectionSourceType(state):
    sourceType = state['app-config']['pose-detection']['source']['type']
    if sourceType.lower() == 'video':
        state['pose-detection-source-type'] = PoseDetectionSourceType.VIDEO
    if sourceType.lower() == 'webcam':
        state['pose-detection-source-type'] = PoseDetectionSourceType.WEBCAM
    return state


# function to configure application state
def configureApplication():
    # create application state
    state = ObjDict()

    # define application configuration file name
    state['config-file-name'] = 'app_config.json'
    state['app-config'] = {}
    state['config-status'] = False

    # load application configuration
    state = loadApplicationConfiguration(state)

    # configure application directories
    if state['config-status']:
        state = configureApplicationDirectories(state)
        state = configureFilePaths(state)
        state = configureDetectionSourceType(state)

    return state
