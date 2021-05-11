from .src.detection_frame import DetectionPeople


def show_video(video):
    print("[INFO] starting save video...")
    new_video = DetectionPeople(video)
    new_video.show_video()
