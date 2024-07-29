from django.db.models import Avg
from rest_framework import status
from rest_framework.test import APIClient
from apps.book.models import Book, Favorite
from apps.book.serializers import BookModelSerializer

from apps.book.tests.factories import BookFactory, FavoriteFactory
from apps.user.tests.factories import UserFactory
from config.test_case import ApiTestCase

class TestBookViews(ApiTestCase):

    
    def test_create_book(self):

        
        """
        Test creating a new book.
        """
        user = self.user
        self.client.force_authenticate(user=user)  # Authenticate the user
        url = '/book/'
        data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'description': 'Book description',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_by_email=response.data['created_by']
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(created_by_email,user.email)


    def test_update_book(self):
        """
        Test updating a book.
        """
        user = self.user
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'description': 'Updated Description',
        }
        self.client.force_authenticate(user=user) 
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.created_by, user)

    def test_update_book_by_another_user(self):
        """
        Test updating a book by a user who is not the owner.
        """
        user = self.user
        book = BookFactory(created_by=user)
        another_user = UserFactory()
        url = f'/book/{book.id}/'
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'description': 'Updated Description',
        }
        self.client.force_authenticate(user=another_user) 
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book(self):
        """
        Test partially updating a book.
        """
        user = self.user
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Partially Updated Title'
        }
        self.client.force_authenticate(user=user) 
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Reload the book from the database
        book.refresh_from_db()
        # Check the updated field
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.created_by, user)

    def test_partial_update_by_another_user(self):
        """
        Test partially updating a book by a user who is not the owner.
        """
        user = self.user
        book = BookFactory(created_by=user)
        another_user = UserFactory()
        url = f'/book/{book.id}/'
        data = {
            'title': 'Partially Updated Title'
        }
        self.client.force_authenticate(user=another_user) 
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_book(self):
        """
        Test deleting a book (soft delete).
        """
        user = self.user
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'
        self.client.force_authenticate(user=user) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)       
        book.refresh_from_db()
        self.assertTrue(book.is_deleted)

    def test_destroy_book_by_another_user(self):
        """
        Test deleting a book by a user who is not the owner.
        """
        user = self.user
        book = BookFactory(created_by=user)
        another_user = UserFactory()
        url = f'/book/{book.id}/'
        self.client.force_authenticate(user=another_user) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_favorite_book(self):
        """
        Test marking a book as favorite.
        """
        user = self.user
        book = BookFactory()
        url = f'/book/{book.id}/favorite/'
        self.client.force_authenticate(user=user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorite.objects.filter(user=user, book=book).exists())

    def test_unfavorite_book(self):
        """
        Test unmarking a book as favorite.
        """
        user = self.user
        book = BookFactory(created_by=user)
        favorite = FavoriteFactory(user=user, book=book)
        url = f'/book/{book.id}/unfavorite/'
        self.client.force_authenticate(user=user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorite.objects.filter(user=user, book=book).exists())


    def test_filter_by_title(self):

        BookFactory(title='Book One', author='Author A', description='Description A', created_by=self.user),
        BookFactory(title='Book Two', author='Author B', description='Description B', created_by=self.user),
        BookFactory(title='Book Three', author='Author A', description='Description C', created_by=self.user)

        url = '/book/?title=Book One'
        response = self.client.get(url)
        print("Response data:", response.data)
        print("Request URL:", response.request['PATH_INFO'])
        print("Request parameters:", response.request['QUERY_STRING'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

        # author

        url = '/book/'
        params = {'author': 'Author A'}
        response = self.client.get(url, params, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(book['author'] == 'Author A' for book in response.data))








