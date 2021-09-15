from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('load_video/', views.LoadFileVideo.as_view(), name='load_video'),
    path('live_video/<str:process_file>/', views.LoadFileVideo.live_video, name='live_video')
]
