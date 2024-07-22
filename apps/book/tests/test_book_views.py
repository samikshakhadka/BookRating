import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.book.models import Book, Favorite

CustomUser = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    user = CustomUser.objects.create_user(username='testuser', password='password')
    return user

@pytest.fixture
def create_book(db, create_user):
    book = Book.objects.create(
        title='Sample Book',
        author='Sample Author',
        description='Sample description',
        created_by=create_user
    )
    return book

@pytest.mark.django_db
def test_list_books(api_client, create_book):
    url = reverse('book-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_create_book(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    url = reverse('book-list')
    data = {
        'title': 'New Book',
        'author': 'Author Name',
        'description': 'Book description'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['title'] == 'New Book'

@pytest.mark.django_db
def test_favorite_book(api_client, create_user, create_book):
    api_client.force_authenticate(user=create_user)
    url = reverse('book-favorite', kwargs={'pk': create_book.id})
    response = api_client.post(url)
    assert response.status_code == 201
    assert response.data['status'] == 'Book marked as favorite'

@pytest.mark.django_db
def test_unfavorite_book(api_client, create_user, create_book):
    api_client.force_authenticate(user=create_user)
    Favorite.objects.create(user=create_user, book=create_book)
    url = reverse('book-unfavorite', kwargs={'pk': create_book.id})
    response = api_client.post(url)
    assert response.status_code == 204

@pytest.mark.django_db
def test_list_favorites(api_client, create_user, create_book):
    api_client.force_authenticate(user=create_user)
    Favorite.objects.create(user=create_user, book=create_book)
    url = reverse('book-list-favorites')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == create_book.id
