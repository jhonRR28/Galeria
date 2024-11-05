from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from gallery.models import Gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages

# Vista de Gallery.
class GalleryListView(ListView):
    model = Gallery

#Galerias del usuario
@login_required
def user_galleries(request):
    # Filtra las galerías que pertenecen al usuario autenticado
    galleries = Gallery.objects.filter(user=request.user)
    return render(request, 'gallery/user_galleries.html', {'galleries': galleries})

#Vista de Logout
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        return reverse_lazy('gallery_list') 