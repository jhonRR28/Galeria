from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from gallery.models import Gallery

# Vista de Gallery.
class GalleryListView(ListView):
    model = Gallery