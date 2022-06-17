from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
import tempfile

from .models import Book

User = get_user_model()


class BookTest(TestCase):
    image = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1')
        cls.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        cls.book = Book.objects.create(
            title='book',
            author='milad',
            description='this is book',
            price=224.41,
            cover=cls.image,
        )

    def test_image(self):
        self.assertEqual(self.book.cover, self.image)

    def test_book_list_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_book_list_url_by_name(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_book_list_page_content(self):
        response = self.client.get(reverse('book_list'))
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.book.author)
        self.assertContains(response, self.book.description)
        self.assertContains(response, self.book.cover)

    def test_book_list_template(self):
        response = self.client.get(reverse('book_list'))
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_url(self):
        response = self.client.get(f'/{self.book.id}/')
        self.assertEqual(response.status_code, 200)

    def test_book_detail_url_by_name(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_page_content(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.book.author)
        self.assertContains(response, self.book.description)
        self.assertContains(response, self.book.cover)
        self.assertContains(response, self.book.price)

    def test_404_status_if_book_if_not_exist(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id + 1]))
        self.assertEqual(response.status_code, 404)

    def test_book_create_url(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_book_create_url_by_name(self):
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)

    def test_book_create_view(self):
        response = self.client.post(reverse('book_create'), {
            'title': 'book2',
            'author': 'author2',
            'description': 'description2',
            'price': 11.66,
            'cover': self.image,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.last().title, 'book2')
        self.assertEqual(Book.objects.last().author, 'author2')
        self.assertEqual(Book.objects.last().description, 'description2')

    def test_update_view(self):
        response = self.client.post(reverse('book_update', args=[self.book.id]), {
            'title': 'book updated',
            'author': 'author updated',
            'description': 'description2 updated',
            'price': 17.00,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.last().title, 'book updated')
        self.assertEqual(Book.objects.last().author, 'author updated')
        self.assertEqual(Book.objects.last().price, 17.00)

    def test_delete_view(self):
        response = self.client.post(reverse('book_delete', args=[self.book.id]))
        self.assertEqual(response.status_code, 302)








