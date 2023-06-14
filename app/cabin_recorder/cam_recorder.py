
import cv2


if __name__ == "__main__":
    device = cv2.VideoCapture(0)
    #device.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    #device.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    #device.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    #device.set(cv2.CAP_PROP_AUTO_WB, 0)
    success, raw = device.read()
    if success is False:
        print("Cannot read data from camera device")
        exit()

    while True:
        # use for camera device
        success, raw = device.read()
        if success is False:
            print("Capture Error")
            break

        cv2.imshow("Raw Image",raw)
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            device.release()
            break