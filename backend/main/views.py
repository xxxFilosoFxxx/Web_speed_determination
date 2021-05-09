# Create your views here.
# from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings


class LoadFileVideo(APIView):
    def post(self, request):
        filename = 'file'
        path = settings.MEDIA_ROOT + '/video'
        default_storage.save(path, ContentFile(request.FILES[filename].read()))
        return Response({'success': 'Video load in media.'}, status=200)
