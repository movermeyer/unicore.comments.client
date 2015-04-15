import json
from datetime import datetime
import pytz

from unicore.comments.client.base import BaseClient, BaseClientObject


class CommentClient(BaseClient):
    base_path = '/comments/'

    def get_comment_page(self, app_uuid, content_uuid,
                         after=None, limit=None, offset=None):
        query = {
            'app_uuid': app_uuid,
            'content_uuid': content_uuid
        }
        for k, v in zip(('after', 'limit', 'offset'), (after, limit, offset)):
            if v is not None:
                query[k] = v

        data = self.get('', params=query)
        return CommentPage(self, data)

    def create_comment(self, data):
        new_data = self.post('', data=data)
        return Comment(self, new_data)

    def create_flag(self, data):
        resp = self._request_no_parse('post', '/flags/', data=json.dumps(data))
        return resp.status_code == 201

    def delete_flag(self, comment_uuid, user_uuid):
        resp = self._request_no_parse(
            'delete', '/flags/%s/%s/' % (comment_uuid, user_uuid))
        return resp.status_code == 200


class Comment(BaseClientObject):

    def set(self, field, value):
        if field == 'uuid':
            raise ValueError('uuid cannot be set')
        self.data[field] = value

    def get(self, field):
        return self.data[field]

    def flag(self, user_uuid):
        flag_data = {
            'app_uuid': self.get('app_uuid'),
            'comment_uuid': self.get('uuid'),
            'user_uuid': user_uuid,
            'submit_datetime': datetime.now(pytz.utc).isoformat()
        }
        is_new = self.client.create_flag(flag_data)
        if is_new:
            self.set('flag_count', self.get('flag_count') + 1)

    def unflag(self, user_uuid):
        was_deleted = self.client.delete_flag(self.get('uuid'), user_uuid)
        if was_deleted:
            self.set('flag_count', self.get('flag_count') - 1)


class CommentPage(object):

    def __init__(self, client, data):
        self.client = client
        self.data = data

    @property
    def offset(self):
        return self.data['offset']

    @property
    def limit(self):
        return self.data['limit']

    @property
    def after(self):
        return self.data['after']

    @property
    def metadata(self):
        return self.data['metadata']

    @property
    def state(self):
        return self.metadata.get('state')

    def __len__(self):
        return self.data['count']

    def __iter__(self):
        for comment_data in self.data['objects']:
            yield Comment(self.client, comment_data)
