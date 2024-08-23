import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.book.models import Book
from apps.user.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches books data from Google Books API and populates the Book model'

    def handle(self, *args, **kwargs):
        query = "Django"  # You can replace this with any search query
        max_results = 10  # Limit the number of results
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
        response = requests.get(url)
        data = response.json()

        if 'items' in data:
            for index, item in enumerate(data['items']):
                if index >= max_results:
                    break  # Stop after processing 10 books
                
                title = item['volumeInfo'].get('title', 'No Title')
                author = ', '.join(item['volumeInfo'].get('authors', ['Unknown Author']))
                description = item['volumeInfo'].get('description', 'No Description')

                logger.info(f"Processing book: {title}")

                try:
                    created_by = CustomUser.objects.get(id=14)
                except CustomUser.DoesNotExist:
                    logger.error("CustomUser with id 14 does not exist.")
                    return
                except Exception as e:
                    logger.error(f"Unexpected error occurred when fetching CustomUser: {e}")
                    return

                try:
                    book = Book.objects.create(
                        title=title,
                        author=author,
                        description=description,
                        created_by=created_by,
                        
                    )
                    logger.info(f"Book '{book.title}' created successfully.")
                except Exception as e:
                    logger.error(f"Failed to create book '{title}': {e}")

        self.stdout.write(self.style.SUCCESS('Command executed'))
