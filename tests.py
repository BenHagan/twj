from django.test import TestCase
from django.core.urlresolvers import reverse

from rango.models import Category, Page


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


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

    def test_index_view_displays_categories(self):

        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

    def test_about_view_displays_text(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is my about page')

    def test_category_view_displays_category_and_pages(self):

        category = add_cat('Django')
        Page(category=category, title='Django Homepage',
             url='http://www.django.com').save()

        response = self.client.get(reverse('category', args=['django']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Django</h1>')
        self.assertContains(
            response,
            '<a href="http://www.django.com">Django Homepage</a>')
