from django.db import models
from django.urls import reverse

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length = 75)
    phase = models.SmallIntegerField()
    training = models.BooleanField()

    def get_absolute_url(self):
        return reverse("subject", args=[str(self.id)])

class SymbolSet(models.Model):
    name = models.CharField(max_length=50)
    length = models.SmallIntegerField()
    phase = models.SmallIntegerField()
    block_size = models.SmallIntegerField()

class SingleSet(models.Model):
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)
    stimulus = models.CharField(max_length=1)
    modifier = models.BooleanField(choices=(
        (True, "!!!!!"),
        (False, "?????")
    ))
    options = models.CharField(max_length=5)
    training = models.BooleanField()
    correct_response = models.CharField(max_length=1)

class ResponseBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    phase = models.SmallIntegerField()
    training = models.BooleanField()
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def date_time(self):
        return "Not implemented yet"

class Response(models.Model):
    block = models.ForeignKey(Subject, on_delete=models.CASCADE)
    response_time = models.DurationField(null=True)
    modifier = models.BooleanField(choices=(
        (True, "!!!!!"),
        (False, "?????")
    ))
    stimulus = models.CharField(max_length=1)
    options = models.CharField(max_length=5)
    correct_response = models.CharField(max_length=1)
    given_response = models.CharField(max_length=1, null=True)
