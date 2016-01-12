import iterable

from iterable.test.helper import IterableApiTestCase


class WorkflowTest(IterableApiTestCase):

    def test_retrieve(self):
        workflow = iterable.Workflow.retrieve(1)

        self.assertEqual(1, workflow.id)

    def test_trigger_workflow(self):
        workflow = iterable.Workflow.retrieve(1)

        with self.assertRaises(iterable.error.APIError):
            workflow.trigger()

        self.mock_response({
            'msg': '',
            'code': 'success',
            'params': None
        })

        data_fields = {
            'subject_product_list': 'Rival 300 and Rival 700',
            'products': [
                {
                    'name': 'Rival 300',
                    'stock': 30,
                    'relevate_product_id': '238uf9842',
                    'price': '$49.99',
                    'image': 'path/to/img',
                    'description': 'description of rival 300',
                    'page_url': 'path/to/product'
                },
                {
                    'name': 'Rival 700',
                    'stock': 10,
                    'relevate_product_id': 'adsf3adsf',
                    'price': '$99.99',
                    'image': 'path/to/img',
                    'description': 'description of rival 700',
                    'page_url': 'path/to/product'
                }
            ]
        }

        workflow.trigger(email='test@test.com', data_fields=data_fields)

        self.requestor_mock.request.assert_called_with(
            'post', iterable.api_base + 'workflows/triggerWorkflow', {'workflowId': 1, 'email': 'test@test.com', 'dataFields': data_fields})
