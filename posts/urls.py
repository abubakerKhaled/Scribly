from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<uuid:uuid>/', views.post_detail, name='post_detail'),
]