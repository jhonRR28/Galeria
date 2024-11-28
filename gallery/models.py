from django.contrib.auth.models import User
from django.db import models

#Modelo de Gallery
class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='gallery/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


#Modelo de Image
class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='gallery_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    allow_download = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} in {self.gallery.title}"







#Modelo de Like
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'image')  # Evita que un usuario de "me gusta" a la misma imagen varias veces

    def __str__(self):
        return f"{self.user.username} liked {self.image.title}"

#Modelo de Comment
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.image.title}"