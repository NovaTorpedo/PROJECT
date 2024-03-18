from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    pass

class Election(models.Model):
    position = models.CharField(max_length=255)
    candidates = models.ManyToManyField('Candidate', related_name='elections')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    
    def __str__(self):
        candidate_names = ', '.join(candidate.first_name for candidate in self.candidates.all())
        return f"Election candidates: {candidate_names}, created by {self.user}, begins on {self.startDateTime.strftime('%d %b %y %H:%M:%S')} and ends on {self.endDateTime.strftime('%d %b %y %H:%M:%S')} id {self.id}"
    
class Candidate(models.Model):
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 255)
    middle_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 255)
    party_affiliation = models.CharField(max_length = 255)
    profile_picture = models.ImageField(upload_to='smvs/files/profile')

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} voted for {self.candidate.first_name} {self.candidate.middle_name} {self.candidate.last_name} for {self.election.position} position"