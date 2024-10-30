from django.contrib import admin
from gallery.models import Gallery, Image, Like, Comment

# Register your models here.
admin.site.register(Gallery)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Comment)
