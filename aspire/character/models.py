from django.db import models

# Create your models here.
class Character(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    race = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    spouse = models.CharField(max_length=200, blank=True, null=True)
    wiki_url = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    dialog = models.CharField(max_length=200, blank=True, null=True)
    movie = models.CharField(max_length=200, blank=True, null=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE , related_name='quotes')

    def __str__(self):
        return self.dialog
