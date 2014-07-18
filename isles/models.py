# isles/models.py

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from core.models import UltraModel

from stores.models import Store

class Isle(UltraModel):
    """ Item -> ( Isle ) -> Store """
    name = models.PositiveSmallIntegerField(validators=[RegexValidator('^[0-9]{1,2}$')]) # I hate you.
    description = models.TextField(max_length=1024)
    store = models.ForeignKey(Store, related_name='isle')

    class Meta:
        unique_together = (("name", "store"),)
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('stores:detail', kwargs={'slug' : self.store.slug})
