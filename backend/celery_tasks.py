"""Основной функционал для работы с очередью задач (rabbitmq) с помощью celery."""
import os
import subprocess

from backend.app import celery
from backend.speed_detection.detection_frame import DetectionPeople


def convert_video(path, video):
    command_ffmpeg = f"ffmpeg -i '{path}/{video}' -c:v libx264 -c:a aac -crf 14 '{path}/SPEED_{video}'"
    command_rm_old_video = f"rm '{path}/{video}'"
    subprocess.call(command_ffmpeg, shell=True)
    subprocess.call(command_rm_old_video, shell=True)


@celery.task(bind=True)
def video_processing(self, path, filename, matrix, width) -> dict:
    # import pstats
    # import cProfile
    # profiler = cProfile.Profile()
    # profiler.enable()

    new_video = DetectionPeople(path)
    self.update_state(state='PROGRESS', meta={'filename': filename})
    video = new_video.save_frames(filename, matrix, width)

    dir_path = os.path.dirname(path)
    convert_video(dir_path, video)
    video = 'SPEED_' + video

    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.dump_stats('../resources_test/time/process_time')
    return {'filename': filename, 'video': video}
