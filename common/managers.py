from django.db import models

class AddressManager(models.Manager):
    def get_query_set(self):
        return super(AddressManager, self).get_query_set().select_related('country','city')
