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
        print('00000000000000000000',response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_by_email=response.data['created_by']

        self.assertEqual(response.data['title'], data['title'])
        # self.assertEqual(response.data['created_by'], user.id)
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
        # Reload the book from the database
        book.refresh_from_db()
        # Check the updated fields
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
        # Reload the book from the database
        book.refresh_from_db()
        # Check that the book is marked as deleted
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

    def test_list_favorites(self):
        """
        Test listing favorite books for the authenticated user.
        """
        user = self.user
        favorites = FavoriteFactory.create_batch(3, user=user)
        url = '/book/list_favorites/'
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = [favorite.book for favorite in favorites]
        serializer = BookModelSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_title(self):

        BookFactory(title='Book One', author='Author A', description='Description A', created_by=self.user),
        BookFactory(title='Book Two', author='Author B', description='Description B', created_by=self.user),
        BookFactory(title='Book Three', author='Author A', description='Description C', created_by=self.user)

        url = '/book/?title=Book One'
        # params = {'title': ''}
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




































# from rest_framework import status
# from rest_framework.test import APIClient
# from apps.book.models import Book, Favorite
# from apps.book.serializers import BookModelSerializer
# from apps.book.tests.factories import BookFactory, FavoriteFactory
# from config.test_case import ApiTestCase

# class BookViewSetTests(ApiTestCase):
#     def test_list_books(self):
#         '''
#         Test listing all books.
#         '''
#         response = self.client.get('/book/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), Book.objects.filter(is_deleted=False).count())

#     def test_create_book(self):
#         '''
#         Test creating a new book.
#         '''
#         self.authenticate(self.user)
#         data = {
#             'title': 'New Book',
#             'author': 'Author Name',
#             'description': 'Book Description'
#         }
#         response = self.client.post('/book/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Book.objects.count(), 2)
#         self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

#     def test_create_book_unauthenticated(self):
#         '''
#         Test creating a book without authentication.
#         '''
#         data = {
#             'title': 'New Book',
#             'author': 'Author Name',
#             'description': 'Book Description'
#         }
#         response = self.client.post('/book/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_update_book(self):
#         '''
#         Test updating a book.
#         '''
#         self.authenticate(self.user)
#         data = {
#             'title': 'Updated Book Title'
#         }
#         response = self.client.patch(f'/book/{self.book.id}/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.book.refresh_from_db()
#         self.assertEqual(self.book.title, 'Updated Book Title')

#     def test_delete_book(self):
#         '''
#         Test deleting a book (soft delete).
#         '''
#         self.authenticate(self.user)
#         response = self.client.delete(f'/book/{self.book.id}/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.book.refresh_from_db()
#         self.assertTrue(self.book.is_deleted)

#     def test_favorite_book(self):
#         '''
#         Test marking a book as favorite.
#         '''
#         self.authenticate(self.user)
#         response = self.client.post(f'/book/{self.book.id}/favorite/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Favorite.objects.filter(user=self.user, book=self.book).exists())

#     def test_unfavorite_book(self):
#         '''
#         Test unmarking a book as favorite.
#         '''
#         self.authenticate(self.user)
#         FavoriteFactory(user=self.user, book=self.book)
#         response = self.client.post(f'/book/{self.book.id}/unfavorite/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Favorite.objects.filter(user=self.user, book=self.book).exists())

#     def test_list_favorite_books(self):
#         '''
#         Test listing favorite books.
#         '''
#         self.authenticate(self.user)
#         FavoriteFactory(user=self.user, book=self.book)
#         response = self.client.get('/book/list_favorites/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], self.book.title)
