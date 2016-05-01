from django.test import TestCase
from django.core.urlresolvers import reverse

from rango.models import Category


class CategoryMethodTests(TestCase):

    def test_ensure_category_views_are_positive(self):
        cat = Category(name="Test", views=-1, likes=0)
        cat.save()
        self.assertTrue(cat.views == 0)

    def test_correct_slug_line_is_created_on_save(self):
        """
        When new Category is created, is correct slug line created.
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):

    def test_empty_index_view(self):

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])
