from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<uuid:uuid>/', views.post_detail, name='post_detail'),
    path('<uuid:post_uuid>/share/', views.post_share, name='post_share'),
    path('<uuid:post_uuid>/comment/', views.post_comment, name='post_comment'),
]