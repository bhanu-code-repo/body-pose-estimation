# importing required packages
import cv2, time, math
import mediapipe as mp
from utils.app_utils import PoseDetectionSourceType


# define pose detector class
class PoseDetector:
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=False, trackCon=0.5):
        self.lmList = None
        self.results = None
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    # function to estimate pose in image
    def findPose(self, img, draw=True):
        # convert image to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # run pose estimation process on image
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        for id, lm in enumerate(self.results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            self.lmList.append([id, cx, cy])
            if draw:
                # add circle overlay on video
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList


# function to detect pose in video
def detectPoseInVideo(state):
    # get input source path
    videoFilePath = state['input-file-path']

    # instantiate video capture
    videoCapture = cv2.VideoCapture(videoFilePath)
    previousTime = 0

    # instantiate pose detector class object
    detector = PoseDetector()
    while True:
        # load video file
        success, image = videoCapture.read()
        image = detector.findPose(image)

        # get landmarks tracking status
        lmTrackingStatus = state['app-config']['pose-detection']['landmarks']['track-landmarks']
        lmList = detector.findPosition(image, draw=not lmTrackingStatus)
        if len(lmList) > 0 and lmTrackingStatus:
            lmPoint = state['app-config']['pose-detection']['landmarks']['landmark-point']
            cv2.circle(image, (lmList[lmPoint][1], lmList[lmPoint][2]), 15, (0, 0, 255), cv2.FILLED)

        # get current time
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        # write fps rate on image
        cv2.putText(image, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # show video
        cv2.imshow('Image', image)
        cv2.waitKey(1)


# function to detect pose in video
def detectPoseFromWebcam(state):
    print('none')


# function to run pose detection
def runPoseDetection(state):
    if state['pose-detection-source-type'] == PoseDetectionSourceType.VIDEO:
        detectPoseInVideo(state)

    if state['POSE_DETECTION_SOURCE'] == PoseDetectionSourceType.WEBCAM:
        detectPoseFromWebcam(state)
