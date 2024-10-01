import logging
from unittest.mock import patch

from django.conf import settings as project_settings
from django.contrib.auth.models import User
from django.test import TestCase                  # TestCase requires db
from django.test import SimpleTestCase  # SimpleTestCase does not require db
from django.test.utils import override_settings

from item_app.forms import FavoriteForm

log = logging.getLogger(__name__)
TestCase.maxDiff = 1000

BDR_API_DATA = {'mods_title_full_primary_tsi': 'Picture of Person',
                'abstract': ['A picture of a person in a library'],
                'thumbnail': 'https://example.com/thumbnail',
                'uri': 'https://example.com/bdr:1234'}


class ErrorCheckTest(SimpleTestCase):
    """Checks urls."""

    @override_settings(DEBUG=True)  # for tests, DEBUG autosets to False
    def test_dev_errorcheck(self):
        """Checks that dev error_check url triggers error."""
        log.debug(f'debug, ``{project_settings.DEBUG}``')
        try:
            log.debug('about to initiate client.get()')
            response = self.client.get('/error_check/')
        except Exception as e:
            log.debug(f'e, ``{repr(e)}``')
            self.assertEqual("Exception('Raising intentional exception to check email-admins-on-error functionality.')", repr(e))

    def test_prod_errorcheck(self):
        """Checks that production error_check url returns 404."""
        log.debug(f'debug, ``{project_settings.DEBUG}``')
        response = self.client.get('/error_check/')
        self.assertEqual(404, response.status_code)


class RootTest(TestCase):
    """Tests root redirects."""

    def test_root_no_auth_redirect(self):
        """Verifies root takes you to login if not authenticated."""
        response = self.client.get('/', follow=True)
        self.assertEqual(response.redirect_chain, [('/login/', 302)])
        self.assertEqual(200, response.status_code)

    def test_root_with_auth_redirect(self):
        """Verifies root takes you to home if authenticated."""
        # Log in the user
        User.objects.create_user(username='buddy', password='test1234!')
        self.client.login(username='buddy', password='test1234!')
        response = self.client.get('/', follow=True)
        self.assertEqual(response.redirect_chain, [('/home/', 302)])
        self.assertEqual(200, response.status_code)


class HomeTest(TestCase):
    """Tests the home view."""

    def setUp(self):
        self.user = User.objects.create_user(username='buddy', password='test1234!')
        self.client.login(username='buddy', password='test1234!')

    @patch('item_app.lib.bdr_process.requests.get')
    def test_home_post(self, mock_get):
        """Tests a POST request with favorite item form data."""
        mock_get.return_value.json.return_value = BDR_API_DATA
        bdr_id = 'bdr:1234'
        access = 'Public'
        notes = 'Read this one thoroughly.'
        response = self.client.post('/home/', {'bdr_id': bdr_id,
                                               'access': access,
                                               'notes': notes})
        self.assertTrue(isinstance(response.context['form'], FavoriteForm))
        self.assertEqual(1, response.context['favorites'].count())
        favorites = response.context['favorites'].first()
        self.assertEqual(self.user, favorites.user)
        self.assertEqual(access, favorites.access)
        self.assertEqual(notes, favorites.notes)
        self.assertIn(BDR_API_DATA['mods_title_full_primary_tsi'], response.content.decode())
