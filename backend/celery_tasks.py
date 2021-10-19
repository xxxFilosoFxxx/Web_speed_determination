import subprocess
import os

from backend.app import celery
from backend.speed_detection.detection_frame import DetectionPeople


def convert_video(path, video):
    command = f"ffmpeg -i '{path}/{video}' -c:v libx264 -c:a aac -crf 14 '{path}/SPEED_{video}'"
    subprocess.call(command, shell=True)


@celery.task(bind=True)
def video_processing(self, path, filename) -> dict:
    new_video = DetectionPeople(path)
    self.update_state(state='PROGRESS', meta={'filename': filename})
    video = new_video.save_frames(filename)

    dir_path = os.path.dirname(path)
    convert_video(dir_path, video)
    video = 'SPEED_' + video
    return {'filename': filename, 'video': video}
