from django.urls import path

from .views import VideoPostDetailView, AllVideoPostListView, VideoPostCreateView, VideoPostUpdateView, \
    VideoPostDeleteView

app_name = 'videos'
urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/<slug:video_slug>/', VideoPostDetailView.as_view(), name='video_post'),
    path('all-videos/', AllVideoPostListView.as_view(), name='all_video_posts'),
    path('upload/', VideoPostCreateView.as_view(), name='upload'),
    path('update/<int:pk>/<slug:slug>/', VideoPostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/<slug:slug>/', VideoPostDeleteView.as_view(), name='delete'),
]
