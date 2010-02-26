from django.db import models

# Create your models here.

class Case(models.Model):
    caseno = models.IntegerField()
    address = models.CharField(max_length=255)
    description = models.TextField()
    
    def __unicode__(self):
        return "%s - %s" % (self.caseno, self.address)
        
