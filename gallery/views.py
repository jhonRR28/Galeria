from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from gallery.models import Gallery, Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .forms import ImageForm, GalleryForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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

#Eliminar galeria
class GalleryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Gallery
    template_name = 'gallery/gallery_confirm_delete.html'  # Nombre de la plantilla de confirmación
    success_url = reverse_lazy('gallery_list')  # Redirigir a la página de inicio u otra página deseada

    def test_func(self):
        gallery = self.get_object()
        return self.request.user == gallery.user  # Solo permite al dueño eliminar

    def handle_no_permission(self):
        # Redirecciona o muestra un mensaje si el usuario no es el propietario
        return redirect('gallery_list')

#Agregar Galeria
@login_required
def add_gallery(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.user = request.user
            gallery.save()
            return redirect('user_galleries')  # Ajusta con el nombre de tu vista de galerías del usuario
    else:
        form = GalleryForm()
    
    return render(request, 'gallery/add_gallery.html', {'form': form})

#Eliminar Imagen
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    # Verifica que el usuario autenticado sea el propietario de la galería
    if image.gallery.user == request.user:
        image.delete()
        return redirect(reverse('gallery_detail', args=[image.gallery.id]))
    else:
        return redirect('gallery_list')  # Redirige a home si el usuario no es el propietario

#Modificar Imagen
@login_required
def edit_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    # Verifica que el usuario autenticado sea el propietario de la galería
    if image.gallery.user != request.user:
        return redirect('gallery_list')  # Redirige si el usuario no es el propietario

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect(reverse('gallery_detail', args=[image.gallery.id]))
    else:
        form = ImageForm(instance=image)

    return render(request, 'gallery/edit_image.html', {'form': form, 'image': image})