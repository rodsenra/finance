from django.db import models

# Create your models here.

class MacroCategory(models.Model):
    name = models.CharField(max_length=200)
    income = models.BooleanField()
    def __unicode__(self):
        return unicode(self.name)
    
class MicroCategory(models.Model):
    name = models.CharField(max_length=200)
    macro = models.ForeignKey(MacroCategory)
    def __unicode__(self):
        return unicode("%s (%s)" % (self.name, self.macro.name))

class Expense(models.Model):
    category = models.ForeignKey(MicroCategory)
    value = models.FloatField()
    date = models.DateField()
    obs = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return unicode(self.category) + u" (%.2f) %s" % (self.value, self.date)
