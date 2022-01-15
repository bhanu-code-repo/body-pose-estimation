# importing required packages
import os


# function to check if path exists
def isPathExists(path):
    return True if os.path.exists(path) else False


# function to configure directories
def configureApplicationDirectories(state):
    # check and configure input path
    inputPath = state['app-config']['pose-detection']['source']['dir']
    if not isPathExists(inputPath):
        os.mkdir(inputPath)
    state['input-dir-path'] = getPath(inputPath)

    # check and configure results path
    resultsPath = state['app-config']['pose-detection']['results']['dir']
    if not isPathExists(resultsPath):
        os.mkdir(resultsPath)
    state['results-dir-path'] = getPath(resultsPath)

    return state


# function to join path
def getPath(*args, single=True):
    if single:
        return os.path.join(os.getcwd(), args[0])
    else:
        if len(args) == 2:
            return os.path.join(args[0], args[1])


def configureFilePaths(state):
    # get input file path
    input_file = state['app-config']['pose-detection']['source']['name']
    state['input-file-path'] = getPath(state['input-dir-path'], input_file, single=False)

    return state
