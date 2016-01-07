import requests
from requests.compat import urljoin

from .models import ListList, User


class Config(object):
    BASE_PATH = 'api.iterable.com/api/'

    API_PATHS = {
        # Lists
        'lists': 'lists',
        'subscribe': 'lists/subscribe',
        'unsubscribe': 'lists/unsubscribe',

        # Users
        'user': 'users/get',

        # Workflows
        'trigger_workflow': 'workflows/triggerWorkflow',
    }

    def __init__(self):
        self.api_url = 'https://%s' % (self.BASE_PATH, )

    def __getitem__(self, key):
        """Return the URL for a given key."""
        return urljoin(self.api_url, self.API_PATHS[key])


class IterableError(Exception):
    
    def __init__(self, data, status):
        message = '{code} ({status}) - {msg}'.format(
            code=data.get('code'),
            status=status,
            msg=data.get('msg'))
        super(IterableError, self).__init__(message)


class IterableResponse(object):

    SUCCESS = 'Success'

    def __init__(self, response):
        self.response = response

    def get_content(self, root_field=None):
        """Parse out content from a response and raise any necessary exceptions.

        Keyword arguments:
        root_field -- the dict field to key off of for returned content
        """
        if self.response.status_code != 200:
            raise IterableError(self.response.json(), self.response.status_code)

        r_json = self.response.json()

        iterable_code = r_json.get('code')

        if iterable_code and iterable_code != IterableResponse.SUCCESS:
            raise IterableError(r_json, 200)

        if root_field:
            return r_json.get(root_field)

        return r_json


class Iterable(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.config = Config()

    # Internals
    @property
    def _headers(self):
        """Headers used in every request."""
        return {'api_key': self.api_key}

    def _get(self, url, root_field=None):
        """Returns a dictionary response from a GET request.

        Arguments:
        url -- the full path for the get request

        Keyword arguments:
        root_fields -- the dict field to key off of for returned content
        """
        response = requests.get(url, headers=self._headers)
        return IterableResponse(response).get_content(root_field=root_field)

    def _post(self, url, data, root_field=None):
        """Returns a dictionary response from a POST request.

        Arguments:
        url -- the full path for the get request
        data -- the payload for the request, as a dictionary

        Keyword arguments:
        root_field -- the dict field to key off of for returned content
        """
        response = requests.post(url, json=data, headers=self._headers)
        return IterableResponse(response).get_content(root_field)

    # Lists
    def get_lists(self):
        """Get all lists."""
        data = self._get(self.config['lists'], root_field='lists')
        return ListList(self, data)

    def subscribe(self, list_id, emails):
        """Subscribe to a mailing list.

        Arguments:
        list_id -- the mailing list id to subscribe to
        emails -- either a single email as a string or a list of emails as strings
        """
        if not isinstance(emails, list):
            emails = [emails]

        users = [User(self, email=email) for email in emails]
        payload = {'listId': list_id, 'subscribers': [user.to_dict() for user in users]}
        return self._post(self.config['subscribe'], payload)

    def unsubscribe(self, list_id, emails, campaign_id=None, channel_unsubscribe=False):
        """Unsubscribe from a mailing list.

        Arguments:
        list_id -- the mailing list's id to unsubscribe from
        emails -- either a single email as a string or a list of emails as strings

        Keyword Arguments:
        campaign_id -- attribute an unsubscribe to a particular campaign
        channel_unsubscribe -- unsubscribe from the list's channel (essentially a global unsub)
        """
        if not isinstance(emails, list):
            emails = [emails]

        users = [User(self, email=email) for email in emails]
        payload = {'listId': list_id, 'subscribers': [user.to_dict() for user in users]}

        if campaign_id:
            payload['campaignId'] = campaign_id

        return self._post(self.config['unsubscribe'], payload)

    # Users
    def get_user(self, email):
        """Get a specific user.

        Arguments:
        email -- email of the user to return
        """
        data = self._post(self.config['user'], {'email': email}, root_field='user')
        return User(self, **data)

    # Workflow
    def trigger_workflow(self, email, workflow_id, data_fields):
        """Trigger a specific workflow.

        Arguments:
        email -- email of the user to trigger the workflow for
        workflow_id -- the id of the workflow to trigger
        data_fields -- dictionary of data to populate content in the associated email template
        """
        data = {
            'email': email,
            'workflowId': workflow_id,
            'dataFields': data_fields
        }

        return self._post(self.config['trigger_workflow'], data)
