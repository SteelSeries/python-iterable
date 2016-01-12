import iterable

from iterable.test.helper import IterableApiTestCase


class ListTest(IterableApiTestCase):

    def test_retrieve_and_refresh(self):
        self.mock_response({})

        with self.assertRaises(iterable.error.APIError):
            iterable_list = iterable.List.retrieve(1)

        self.mock_response([
            {
                'id': 1,
                'name': 'List 1',
                'size': 65000
            },
            {
                'id': 2,
                'name': 'List 2',
                'size': 400
            },
            {
                'id': 9448,
                'name': '',
                'size': 0
            }
        ])

        iterable_list = iterable.List.retrieve(1)

        self.requestor_mock.request.assert_called_with(
            'get', iterable.api_base + 'lists', root_field='lists')

        self.assertEqual(1, iterable_list.id)
        self.assertEqual('List 1', iterable_list.name)
        self.assertEqual(65000, iterable_list.size)

        self.mock_response([
            {
                'id': 1,
                'name': 'List Name 1',
                'size': 65000
            }
        ])

        iterable_list = iterable_list.refresh()

        self.requestor_mock.request.assert_called_with(
            'get', iterable.api_base + 'lists', root_field='lists')

        self.assertEqual(1, iterable_list.id)
        self.assertEqual('List Name 1', iterable_list.name)
        self.assertEqual(65000, iterable_list.size)

    def test_retrieve_all_lists(self):
        self.mock_response([
            {
                'id': 1,
                'name': 'List 1',
                'size': 65000
            },
            {
                'id': 2,
                'name': 'List 2',
                'size': 400
            },
            {
                'id': 9448,
                'name': '',
                'size': 0
            }
        ])

        lists = iterable.List.all()

        self.requestor_mock.request.assert_called_with(
            'get', iterable.api_base + 'lists', root_field='lists')

        self.assertEqual(len(lists), 3)
        self.assertTrue(isinstance(lists[0], iterable.List))

        self.assertEqual(1, lists[0].id)
        self.assertEqual('List 2', lists[1].name)
        self.assertEqual(0, lists[2].size)
