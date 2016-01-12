import iterable

from requests.compat import urljoin

import error
from .api_requestor import APIRequestor


class IterableObject(object):

    PATHS = {
        # users
        'user': 'users/get',

        # lists
        'lists': 'lists',
        'subscribe': 'lists/subscribe',
        'unsubscribe': 'lists/unsubscribe',

        # commerce
        'track_purchase': 'commerce/trackPurchase',

        # workflows
        'trigger_workflow': 'workflows/triggerWorkflow'
    }

    @classmethod
    def get_url(cls, endpoint):
        return urljoin(iterable.api_base, cls.PATHS.get(endpoint))


class User(IterableObject):

    def __init__(self, email, id=None, data_fields=None):
        self.email = email
        self.id = id
        self.data_fields = data_fields or {}

    @classmethod
    def retrieve(cls, email):
        instance = cls(email)
        instance.refresh()
        return instance

    def refresh(self):
        requestor = APIRequestor()
        response = requestor.request(
            'post', self.get_url('user'), {'email': self.email}, root_field='user')
        self.refresh_from(response)
        return self

    def refresh_from(self, values):
        self.email = values.get('email')
        self.id = values.get('userId')
        self.data_fields = values.get('dataFields')

    # API Actions
    def subscribe(self, list_id):
        requestor = APIRequestor()
        requestor.request('post', self.get_url('subscribe'), {'listId': list_id, 'subscribers': [{'email': self.email}]})
        return self

    def unsubscribe(self, list_id):
        requestor = APIRequestor()
        requestor.request('post', self.get_url('unsubscribe'), {'listId': list_id, 'subscribers': [{'email': self.email}]})
        return self

    def to_dict(self):
        return {
            'email': self.email,
            'dataFields': self.data_fields,
            'userId': self.id
        }


class List(IterableObject):

    def __init__(self, id, name=None, size=None):
        self.id = id
        self.name = name
        self.size = size

    @classmethod
    def all(cls):
        requestor = APIRequestor()
        response = requestor.request('get', cls.get_url('lists'), root_field='lists')
        return [List(**x) for x in response]

    @classmethod
    def retrieve(cls, id):
        instance = cls(id)
        instance.refresh()
        return instance

    def refresh(self):
        requestor = APIRequestor()
        response = requestor.request('get', self.get_url('lists'), root_field='lists')
        self.refresh_from(response)
        return self

    def refresh_from(self, values):
        for l in values:
            if l.get('id') == self.id:
                self.name = l.get('name')
                self.size = l.get('size')
                return

        raise error.APIError('List with id %s does not exist.' % (self.id, ))


class Workflow(IterableObject):

    def __init__(self, id):
        self.id = id

    @classmethod
    def retrieve(cls, id):
        instance = cls(id)
        return instance

    def trigger(self, email=None, list_id=None, data_fields=None):
        if not (email or list_id):
            raise error.APIError('Must provide an email or a list_id to trigger a workflow')

        requestor = APIRequestor()
        request_obj = {'workflowId': self.id}

        if email:
            request_obj['email'] = email

        if list_id:
            request_obj['listId'] = list_id

        if data_fields:
            request_obj['dataFields'] = data_fields

        requestor.request('post', self.get_url('trigger_workflow'), request_obj)

        return True


class Commerce(IterableObject):

    @classmethod
    def track_purchase(cls, user, items, total, campaign_id=None, template_id=None, created_at=None, data_fields=None):
        request_obj = {
            'user': user.to_dict(),
            'items': [x.to_dict() for x in items],
            'total': total
        }

        if campaign_id:
            request_obj['campaignId'] = campaign_id

        if template_id:
            request_obj['templateId'] = template_id

        if created_at:
            request_obj['createdAt'] = created_at

        if data_fields:
            request_obj['data_fields'] = data_fields

        requestor = APIRequestor()
        requestor.request('post', cls.get_url('track_purchase'), request_obj)

        return True
