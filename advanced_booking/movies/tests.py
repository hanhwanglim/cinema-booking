from datetime import date

from django.urls import reverse
from django.test import TestCase

from .models import Movie


def create_movie(title):
    """
    Create a new movie with the given title.
    """
    return Movie.objects.create(
        title=title,
        director='John Doe',
        lead_actor='Person 1, Person 2, Person 3',
        certificate='PG',
        duration=199,
        rating=5.1,
        premier_date=date(2020, 1, 1)
    )


class MovieViewTests(TestCase):
    def test_movie_empty_index_page(self):
        """
        The movie index page should not be displaying any movies.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No movies are available.")
        self.assertQuerysetEqual(response.context['movie_list'], [])

    def test_movie_index_page(self):
        """
        The movie index page should display the movies.
        """
        for i in range(3):
            create_movie(f'Title of Movie {i + 1}')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        for i in range(3):
            self.assertContains(response, f'Title of Movie {i + 1}')

        self.assertEqual(len(response.context['movie_list']), 3)
