from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from gallery.models import Gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .forms import ImageForm, GalleryForm


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

#Detalles de Galeria
# class GalleryDetailView(DetailView):
#     model = Gallery
#     template_name = 'gallery/gallery_detail.html'
#     context_object_name = 'gallery'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Agrega las imágenes asociadas a la galería en el contexto
#         context['images'] = self.object.images.all()
#         return context

class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'gallery/gallery_detail.html'
    context_object_name = 'gallery'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega las imágenes asociadas a la galería en el contexto
        context['images'] = self.object.images.all()
        # Verifica si el usuario autenticado es el propietario de la galería
        context['is_owner'] = self.request.user == self.object.user
        return context


@login_required
def add_image_to_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    # Verifica que el usuario autenticado sea el propietario de la galería
    if request.user != gallery.user:
        messages.error(request, "No tienes permiso para agregar imágenes a esta galería.")
        return redirect('gallery_detail', pk=gallery.id)
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.gallery = gallery
            new_image.save()
            messages.success(request, "Imagen agregada exitosamente.")
            return redirect('gallery_detail', pk=gallery.id)
    else:
        form = ImageForm()
    
    return render(request, 'gallery/add_image.html', {'form': form, 'gallery': gallery})

#Modificar Galerias
@login_required
def edit_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)

    # Verifica que el usuario autenticado sea el propietario de la galería
    if request.user != gallery.user:
        messages.error(request, "No tienes permiso para editar esta galería.")
        return redirect('gallery_detail', pk=gallery.id)

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, "Galería actualizada exitosamente.")
            return redirect('gallery_detail', pk=gallery.id)
    else:
        form = GalleryForm(instance=gallery)
    
    return render(request, 'gallery/edit_gallery.html', {'form': form, 'gallery': gallery})