from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book


class BookTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_book = Book.objects.create(
            title="The Hobbit",
            owner=testuser1,
            author="J.R.R. Tolkien",
            publication_year=1937,
        )
        test_book.save()

    def test_books_model(self):
        book = Book.objects.get(id=1)
        actual_owner = str(book.owner)
        actual_title = str(book.title)
        actual_author = str(book.author)
        actual_publication_year = int(book.publication_year)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_title, "The Hobbit")
        self.assertEqual(actual_author, "J.R.R. Tolkien")
        self.assertEqual(actual_publication_year, 1937)

    def test_get_book_list(self):
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.data
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "The Hobbit")

    def test_get_book_by_id(self):
        url = reverse("book_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = response.data
        self.assertEqual(book["title"], "The Hobbit")

    def test_create_book(self):
        url = reverse("book_list")
        data = {"owner": 1, "title": "I Know Why the Caged Bird Sings", "author": "Maya Angelou", "publication_year": 1969}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        books = Book.objects.all()
        self.assertEqual(len(books), 2)
        self.assertEqual(Book.objects.get(id=2).title, "I Know Why the Caged Bird Sings")

    def test_update_book(self):
        url = reverse("book_detail", args=(1,))
        data = {
            "owner": 1,
            "title": "The Hobbit",
            "author": "John R.R. Tolkien",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=1)
        self.assertEqual(book.title, data["title"])
        self.assertEqual(book.owner.id, data["owner"])
        self.assertEqual(book.author, data["author"])

    def test_delete_book(self):
        url = reverse("book_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        books = Book.objects.all()
        self.assertEqual(len(books), 0)