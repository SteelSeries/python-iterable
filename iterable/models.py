from UserList import UserList


class User(object):

    def __init__(self, client, email, userId=None, dataFields=None):
        """User representation.

        Arguments:
        client -- an instance of the iterable client to perform API calls
        email -- email of the user

        Keyword arguments:
        userId -- Iterable's user id for the user
        dataFields -- a dictionary of data fields for a given user
        """
        self.client = client
        self.id = userId
        self.email = email
        self.data_fields = dataFields or {}

        # Fields dependent on data_fields
        self.lists = self._get_lists()

    # Constructor helpers
    def _get_lists(self):
        """Parses out list IDs and creates instances of a List"""
        if 'emailListIds' not in self.data_fields:
            return []

        return [List(self.client, id=list_id) for list_id in self.data_fields.get('emailListIds')]

    # API methods
    def subscribe(self, list_id):
        """Subscribe to a mailing list."""
        response = self.client.subscribe(list_id, self.email)
        return bool(response.get('successCount'))

    def unsubscribe(self, list_id, campaign_id=None, channel_unsubscribe=False):
        """Unsubscribe from a mailing list."""
        response = self.client.unsubscribe(list_id, self.email, campaign_id, channel_unsubscribe)
        return bool(response.get('successCount'))

    # API serialization
    def to_dict(self):
        """Create a dictionary based on user information, aligning closely with Iterable's ApiUser"""
        obj = {'email': self.email}

        if self.id:
            obj['userId'] = self.id

        if self.data_fields:
            obj['dataFields'] = self.data_fields

        return obj

    def __repr__(self):
        return 'User(%s, %s, %s)' % (self.id, self.email, str(self.data_fields))

class List(object):

    def __init__(self, client, id, name=None, size=None):
        """List representation.

        Arguments:
        client -- an instance of the iterable client to perform API calls
        id -- Iterable list ID

        Keyword arguments:
        name -- name of the list
        size -- number of subscribers in the list
        """
        self.client = client
        self.id = id
        self.name = name
        self.size = size

    def __repr__(self):
        return 'List(%d)' % (self.id)


class ListList(UserList):

    def __init__(self, client, lists=None):
        """List of Lists.

        Arguments:
        client -- an instance of the iterable client to perform API calls

        Keyword arguments
        lists -- the underlying set of lists to maintain
        """
        lists = lists or []

        data = [List(client, **l) for l in lists]
        super(ListList, self).__init__(data)

    def __repr__(self):
        return 'ListList(%s)' % (', '.join(map(repr, self.data)))
