from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


def delete_photo(photo):
    if default_storage.exists(photo.name):
        default_storage.delete(photo.name)


class CatFact(models.Model):
    fact = models.CharField(max_length=500)

    def __str__(self):
        return self.fact


class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                delete_photo(old_place.photo)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            delete_photo(self.photo)
        super().delete(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.pk}: {self.name} visited? {self.visited} on {self.date_visited}. ' \
               f'Notes: {notes_str}\nPhoto {photo_str}'
