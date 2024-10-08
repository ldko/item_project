from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    bdr_id = models.CharField(max_length=12, primary_key=True)
    title = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=500, blank=True)
    thumbnail = models.CharField(max_length=100, blank=True)
    uri = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.bdr_id}: {self.title}'


class Favorite(models.Model):
    PRIVATE = 'Private'
    PUBLIC = 'Public'
    ACCESS_CHOICES = [
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    access = models.CharField(max_length=7, choices=ACCESS_CHOICES)
    added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def is_public(self):
        return self.access == self.PUBLIC

    class Meta:
        ordering = ['-added']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    favorite = models.ManyToManyField(Favorite)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
