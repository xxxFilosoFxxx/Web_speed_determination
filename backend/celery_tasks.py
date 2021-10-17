from backend.app import celery
import time


@celery.task(bind=True)
def video_processing(self, msisdn: float, radius: float, delta: float) -> dict:
    self.update_state(state='PROGRESS',
                      meta={'msisdn': msisdn, 'radius': radius, 'delta': delta})
    return {'msisdn': msisdn, 'radius': radius, 'delta': delta}
