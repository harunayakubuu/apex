from django.urls import path
from .views import (
    public_posts,
    public_post_detail,

    all_posts,
    post_create,
    post_update,
    post_delete
    
)

app_name = 'blog'

urlpatterns = [
    path('posts/', public_posts, name = 'public-posts'),
    path('all/posts/', all_posts, name = 'all-posts'),
    path('post/create/form/', post_create, name = 'post-create'),
    path('post/<str:slug>/', public_post_detail, name = 'public-post-detail'),
    path('post/<int:id>/update/', post_update, name = 'post-update'),
    path('post/<int:id>/delete/', post_delete, name = 'post-delete')
]