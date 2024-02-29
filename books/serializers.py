from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ("owner", "title", "author", "publication_year", "entry_date", "update_date")
    model = Book
