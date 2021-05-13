# Create your views here.
# from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

from .src.detection_frame import DetectionPeople


class LoadFileVideo(APIView):
    def post(self, request):
        filename = 'file'
        path = settings.MEDIA_ROOT + '/' + str(request.FILES[filename])
        default_storage.save(path, ContentFile(request.FILES[filename].read()))

        print("[INFO] starting save video...")
        new_video = DetectionPeople(path)
        # return Response({'success': 'Video load in media.'}, status=200)
        return Response(new_video.translation_video(), content_type='multipart/x-mixed-replace; boundary=frame')
