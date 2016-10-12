from django.db import models
from django.urls import reverse
from django.utils import timezone

class Phase(models.Model):
    phase_num = models.SmallIntegerField(verbose_name="Phase Number")
    training = models.BooleanField(default=True)
    passing_accuracy_percentage = models.SmallIntegerField(null=True, blank=True, verbose_name="Passing Accuracy %")
    passing_time = models.DurationField(null=True, blank=True, verbose_name="Passing Time (ms)")

    def __unicode__(self):
        return "Phase " + str(self.phase_num) + " - " + ("Training" if self.training else "Testing")

    def get_passing_time(self):
        return self.response_time.microseconds/1000.0

class Subject(models.Model):
    subject_id = models.SmallIntegerField(primary_key=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse("subject", args=[str(self.id)])

    def __unicode__(self):
        return "Subject " + str(self.subject_id)

class SymbolSet(models.Model):
    name = models.CharField(max_length=50)
    length = models.SmallIntegerField()
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    block_size = models.SmallIntegerField()

class SingleSet(models.Model):
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)
    stimulus = models.CharField(max_length=1)
    modifier = models.BooleanField()
    options = models.CharField(max_length=5)
    training = models.BooleanField()
    correct_response = models.CharField(max_length=1)

class ResponseBlock(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(ResponseBlock, self).save(*args, **kwargs)

    def date_time(self):
        return self.created

    def get_absolute_url(self):
        return reverse("response_set", args=[str(self.id)])

    def successful(self):
        responses = self.response_set.all()
        time = 0
        correct = 0
        count = 0
        for response in responses:
            time += response.get_response_time()
            count += 1
            correct += response.correct()
        if (not self.phase.passing_accuracy_percentage) or (correct/count >= self.phase.passing_accuracy_percentage/100):
            if (not self.phase.passing_time) or (time <= self.phase.passing_time):
                return "Passed"
        return "Failed"

class Response(models.Model):
    block = models.ForeignKey(ResponseBlock, on_delete=models.CASCADE)
    response_time = models.DurationField(null=True)
    modifier = models.BooleanField()
    stimulus = models.CharField(max_length=1)
    options = models.CharField(max_length=5)
    correct_response = models.CharField(max_length=1)
    given_response = models.CharField(max_length=1, null=True)

    def get_response_time(self):
        try:
            return self.response_time.microseconds/1000.0
        except:
            return 0

    def correct(self):
        if self.correct_response == self.given_response:
            return 1
        return 0

class SessionLength(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    trials = models.SmallIntegerField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(SessionLength, self).save(*args, **kwargs)
