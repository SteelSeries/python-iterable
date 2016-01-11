class CommerceItem(object):

    def __init__(self, id, name, price, quantity,
                 sku=None, description=None, categories=None,
                 image_url=None, url=None, data_fields=None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sku = sku
        self.description = description
        self.categories = categories
        self.image_url = image_url
        self.url = url
        self.data_fields = data_fields

    def to_dict(self):
        d = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
        }

        if self.sku:
            d['sku'] = self.sku

        if self.description:
            d['description'] = self.description

        if self.categories:
            d['categories'] = self.categories

        if self.image_url:
            d['imageUrl'] = self.image_url

        if self.url:
            d['url'] = self.url

        if self.data_fields:
            d['dataFields'] = self.data_fields

        return d
