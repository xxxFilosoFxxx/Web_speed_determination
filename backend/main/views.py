# Create your views here.
# from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

from .src.detection_frame import DetectionPeople


class LoadFileVideo(APIView):
    filename = 'file'
    path = ''

    def post(self, request):
        self.path = settings.MEDIA_ROOT + '/' + str(request.FILES[self.filename])
        default_storage.save(self.path, ContentFile(request.FILES[self.filename].read()))
        return Response({'success': 'Video load in media.'}, status=200)

    def get(self, _):
        # TODO:
        if self.path:
            print("[INFO] starting save video...")
            new_video = DetectionPeople(self.path)
            return Response(new_video.translation_video(), content_type='multipart/x-mixed-replace; boundary=frame')
        else:
            return Response(status=100)
