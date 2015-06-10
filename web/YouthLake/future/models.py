from django.db import models

class FilterResult(models.Model):
    filter_name = models.TextField(primary_key=True, blank=False, null=False)
    date = models.TextField(primary_key=True, blank=False, null=False)
    contract = models.TextField(primary_key=True, blank=False, null=False)
    index_v = models.IntegerField(primary_key=True, blank=False, null=False)
    direction = models.TextField(primary_key=True, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'filter_result'
        unique_together = (('filter_name', 'date', 'contract'),)

