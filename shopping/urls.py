from django.urls import path
from . import views

urlpatterns = [
#    path('<int:pk>/', views.single_post_page),
#    path('', views.index), #서버IP/shopping

    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>', views.category_page),
    path('manufacture/<str:slug>', views.manufacture_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]