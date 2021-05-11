# Create your views here.
# from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

from .save_detection import show_video


class LoadFileVideo(APIView):
    def post(self, request):
        filename = 'file'
        path = settings.MEDIA_ROOT + '/' + str(request.FILES[filename])
        default_storage.save(path, ContentFile(request.FILES[filename].read()))
        # show_video(path)
        return Response({'success': 'Video load in media.'}, status=200)
        # return Response(show_video(path), content_type='multipart/x-mixed-replace; boundary=frame', status=200)
