"""
URL configuration for photo_portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from gallery import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.GalleryListView.as_view(),name='gallery_list'),
    path('my-galleries/', views.user_galleries, name='user_galleries'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('gallery/<int:pk>/', views.GalleryDetailView.as_view(), name='gallery_detail'),
    path('gallery/<int:gallery_id>/add_image/', views.add_image_to_gallery, name='add_image_to_gallery'),
    path('gallery/<int:gallery_id>/edit/', views.edit_gallery, name='edit_gallery'),
    path('galeria/<int:pk>/eliminar/', views.GalleryDeleteView.as_view(), name='delete_gallery'),
    path('gallery/add/', views.add_gallery, name='add_gallery'),
    path('imagen/<int:image_id>/eliminar/', views.delete_image, name='delete_image'),
    path('imagen/<int:image_id>/editar/', views.edit_image, name='edit_image'),
]
