from django.db import models

# Create your models here.
class BpdOc1(models.Model):
    id = models.IntegerField(primary_key=True)
    epochtime = models.IntegerField()
    time = models.CharField(max_length=19)
    lotno = models.CharField(max_length=14)
    prod_order = models.IntegerField()
    counter = models.IntegerField()
    value = models.CharField(max_length=39)
    avg = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bpd_oc1'