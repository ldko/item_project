import logging

from django.conf import settings as project_settings
import requests

from item_app.models import Item, Favorite


log = logging.getLogger(__name__)


class BDR_Favorite:
    """Favorite BDR Item"""

    def __init__(self, bdr_id, user, access, notes=None):
        self.bdr_id = bdr_id
        self.user = user
        self.access = access
        self.notes = notes
        self.bdr_item_uri = f'{project_settings.BDR_BASE_URI}/items/{bdr_id}/'
        self.item = self.save_item()
        self.favorite = None
        if self.item:
            self.favorite = self.save_favorite()

    def save_item(self):
        """Create or update item data in the database."""
        bdr_item_data = self.get_item_data()
        if 'error' in bdr_item_data:
            # Could not successfully retrieve item
            log.debug('Failed to retrieve data for {self.bdr_id}: {bdr_item_data["error"]}')
            return None
        item, created = Item.objects.get_or_create(bdr_id=self.bdr_id)
        item.title = bdr_item_data['title']
        item.description = bdr_item_data['description']
        item.uri = bdr_item_data['uri']
        item.thumbnail = bdr_item_data['thumbnail']
        item.save()
        self.item_created = created
        return item

    def save_favorite(self):
        """Create or update info about a user's favorite item in the database."""
        favorite, created = Favorite.objects.get_or_create(item=self.item, user=self.user)
        favorite.access = self.access
        favorite.notes = self.notes
        favorite.save()
        self.favorite_created = created
        return favorite

    def get_item_data(self):
        """Retrieve item data from BDR API."""
        log.debug(f'Requesting data at {self.bdr_item_uri}')
        try:
            response = requests.get(self.bdr_item_uri)
            # Error on bad status code
            response.raise_for_status()
        except requests.RequestException as err:
            return {'error': err}
        response_json = response.json()
        item_data = {
            'title': response_json.get('primary_title', ''),
            'description': response_json.get('abstract', [''])[0],
            'thumbnail': response_json.get('thumbnail', ''),
            'uri': response_json.get('uri', '')
        }
        log.debug(f'Data for {self.bdr_id}: {item_data}')
        return item_data
