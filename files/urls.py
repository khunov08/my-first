
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'files'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_file, name='add'),
    path('add-after/', views.add_file_after, name='add_after'),
    path('del/', views.del_file, name='del'),
    path('del-after/', views.del_file_after, name='del_after'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
