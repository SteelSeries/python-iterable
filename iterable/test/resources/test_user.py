import iterable

from iterable.test.helper import IterableApiTestCase

from iterable.resource import User


class UserTest(IterableApiTestCase):

    def test_retrieve_and_refresh(self):
        self.mock_response({
            'email': 'test@test.com',
            'userId': 1,
            'dataFields': {
                'field1': 'value1',
                'field2': 2
            }
        })

        user = User.retrieve('test@test.com')

        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'users/get', {'email': 'test@test.com'}, root_field='user')

        self.assertEqual('test@test.com', user.email)
        self.assertEqual(1, user.id)
        self.assertEqual({'field1': 'value1', 'field2': 2}, user.data_fields)

        self.mock_response({
            'email': 'test1@test.com',
            'userId': 32,
            'dataFields': {
                'field1': 'value1',
                'field2': 'value2'
            }
        })

        user = user.refresh()

        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'users/get', {'email': 'test@test.com'}, root_field='user')

        self.assertEqual('test1@test.com', user.email)
        self.assertEqual(32, user.id)
        self.assertEqual({'field1': 'value1', 'field2': 'value2'}, user.data_fields)

    def test_subscribe(self):
        self.mock_response({
            'email': 'test@test.com'
        })

        user = User.retrieve('test@test.com')

        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'users/get', {'email': 'test@test.com'}, root_field='user')

        self.mock_response({
            'successCount': 1,
            'failCount': 0
        })

        user.subscribe(8243)

        subscribe_request_data = {'listId': 8243, 'subscribers': [{'email': user.email}]}
        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'lists/subscribe', subscribe_request_data)

    def test_unsubscribe(self):
        self.mock_response({
            'email': 'test@test.com'
        })

        user = User.retrieve('test@test.com')

        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'users/get', {'email': 'test@test.com'}, root_field='user')

        self.mock_response({
            'successCount': 1,
            'failCount': 0
        })

        user.unsubscribe(8243)

        subscribe_request_data = {'listId': 8243, 'subscribers': [{'email': user.email}]}
        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'lists/unsubscribe', subscribe_request_data)
