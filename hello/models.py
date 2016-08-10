from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length = 75)
    phase = models.SmallIntegerField(choices=(
        (1, "Phase 1 - Training"),
        (2, "Phase 1 - Testing"),
        (3, "Phase 2 - Training"),
        (4, "Phase 2 - Testing"),
        (5, "Phase 3 - Training"),
        (6, "Phase 3 - Testing"),
        (7, "Phase 4 - Training"),
        (8, "Phase 4 - Testing"),
        (9, "Phase 5 - Training"),
        (10, "Phase 5 - Testing")
    ))

class ResponseBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    phase = models.SmallIntegerField(choices=(
        (1, "Phase 1 - Training"),
        (2, "Phase 1 - Testing"),
        (3, "Phase 2 - Training"),
        (4, "Phase 2 - Testing"),
        (5, "Phase 3 - Training"),
        (6, "Phase 3 - Testing"),
        (7, "Phase 4 - Training"),
        (8, "Phase 4 - Testing"),
        (9, "Phase 5 - Training"),
        (10, "Phase 5 - Testing")
    ))
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)

class Response(models.Model):
    block = models.ForeignKey(Subject, on_delete=models.CASCADE)
    response_time = models.DurationField()
    stimulus_type = models.BooleanField(choices=(
        (True, "!!!!!"),
        (False, "?????")
    ))
    stimulus = models.SmallIntegerField()
    responses = models.CharField(max_length = 5)
    correct_response = models.SmallIntegerField()
    given_response = models.SmallIntegerField()

class SymbolSet(models.Model):
    name = models.CharField(max_length=30)
    
