from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book
from .serializers import BookSerializer

class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    