"""
diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  content('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  content('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, content
    2. Add a URL to urlpatterns:  content('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cloud_storage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('upload_file/<int:folder_id>', views.upload_file, name='upload_file'),
    path('create_folder/<int:folder_id>', views.create_folder, name='create_folder'),
    path('shared_files/<int:file_id>', views.shared_files_post, name='shared_files_post'),
    path('shared_files/', views.shared_files, name='shared_files'),
    path('files/', include('cloud_storage.urls')),
    path('delete_file/<int:pk>/', views.delete_file, name='delete_file'),
    path('delete_folder/<int:pk>/', views.delete_folder, name='delete_folder'),
]

if settings.USE_S3 is False:
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
