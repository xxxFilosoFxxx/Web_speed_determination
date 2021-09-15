from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators import gzip
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import StreamingHttpResponse
from django.conf import settings

from .src.detection_frame import DetectionPeople


class LoadFileVideo(APIView):
    filename = 'file'
    path = ''

    def post(self, request):
        self.path = settings.MEDIA_ROOT + '/' + str(request.FILES[self.filename])
        default_storage.save(self.path, ContentFile(request.FILES[self.filename].read()))
        print("[INFO] video saved successfully")
        return Response({'success': 'Video load in media.'}, status=200)

    @gzip.gzip_page
    def live_video(self, process_file):
        try:
            print("[INFO] starting save video...")
            self.path = settings.MEDIA_ROOT + '/' + str(process_file)
            new_video = DetectionPeople(self.path)
            return StreamingHttpResponse(new_video.translation_video(str(process_file)),
                                         content_type='multipart/x-mixed-replace; boundary=frame')
        except:
            pass
