from django.conf.urls import url
from django.urls import path
from .views import image_create, image_detail, image_like, list_view

urlpatterns = [
    path('', list_view, name='images-list-view'),
    path('create/', image_create, name='image-create'),
    path('like/', image_like, name='like'),
    path('detail/<int:i_d>/<str:slug>/', image_detail, name='detail'),

]
