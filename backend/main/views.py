# Create your views here.
# from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):
    def get(self, _):
        return Response({'message': 'Hello'}, status=200)
