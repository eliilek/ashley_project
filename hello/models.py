from django.db import models
from django.urls import reverse
from django.utils import timezone
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField

class Phase(models.Model):
    phase_num = models.SmallIntegerField(verbose_name="Phase Number")
    passing_accuracy_percentage = models.SmallIntegerField(null=True, blank=True, verbose_name="Passing Accuracy %")
    passing_time = models.DurationField(null=True, blank=True, verbose_name="Passing Time (ms)")

    def __unicode__(self):
        return "Phase " + str(self.phase_num)

    def get_passing_time(self):
        return self.response_time.microseconds/1000.0

class Subject(models.Model):
    subject_id = models.SmallIntegerField(primary_key=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    training = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("subject", args=[str(self.id)])

    def __unicode__(self):
        return "Subject " + str(self.subject_id)

class SymbolSet(models.Model):
    class Meta:
        verbose_name = "Symbol Set"
    name = models.CharField(max_length=100)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    block_size = models.SmallIntegerField()

    def __unicode__(self):
        return self.name + " Set"

class Symbol(models.Model):
    name = models.CharField(max_length=50)
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __unicode__(self):
        return self.name

class SingleSet(models.Model):
    class Meta:
        verbose_name = "Single Set"
    symbol_set = models.ForeignKey(SymbolSet, on_delete=models.CASCADE)
    stimulus = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    modifier = models.BooleanField(verbose_name="!!!!!")
    option_1 = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="first")
    option_2 = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="second")
    option_3 = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="third")
    training = models.BooleanField()
    correct_response = models.CharField(max_length=1, verbose_name="Option Number of Correct Response (1, 2, or 3)")

    def __unicode__(self):
        return str(self.symbol_set) + " - " + str(self.stimulus) + " " + ("!!!!!" if self.modifier else "?????")

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
        try:
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
        except:
            return "Failed"

class Response(models.Model):
    block = models.ForeignKey(ResponseBlock, on_delete=models.CASCADE)
    response_time = models.DurationField(null=True)
    modifier = models.BooleanField(verbose_name="!!!!!")
    stimulus = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    option_1 = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="first_response")
    option_2 = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="second_response")
    option_3 = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name="third_response")
    correct_response = models.PositiveSmallIntegerField()
    given_response = models.PositiveSmallIntegerField(null=True)

    def get_response_time(self):
        try:
            return self.response_time.ms/1000.0
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
