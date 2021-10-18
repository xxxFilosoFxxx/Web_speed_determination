from backend.app import celery
from backend.speed_detection.detection_frame import DetectionPeople


@celery.task(bind=True)
def video_processing(self, path, filename) -> dict:
    new_video = DetectionPeople(path)
    self.update_state(state='PROGRESS', meta={'filename': filename})
    video = new_video.save_frames(filename)
    return {'filename': filename, 'video': video}
