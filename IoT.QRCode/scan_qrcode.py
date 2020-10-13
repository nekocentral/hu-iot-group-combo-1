import cv2
import pyzbar.pyzbar as pyzbar

def get_qrcode(video_index):
    '''Scans QR code based on index of video'''
    cap = cv2.VideoCapture(video_index)
    font = cv2.FONT_HERSHEY_PLAIN

    while True:
        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            return obj.data


print(get_qrcode(2))