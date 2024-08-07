# accounts/models.py
from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):

    reports_to = models.CharField(max_length=25)
    position = models.CharField(max_length=20, default="developer")
    team = models.CharField(max_length=50)
    user_refresh_token = models.CharField(max_length=255,null=True)

    def __str__(self):
        return f"{self.username}"

class TeamLead(models.Model):
    tl = models.OneToOneField(User, on_delete=models.CASCADE, related_name="team_lead")


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="devs")
    lead = models.ForeignKey(TeamLead,on_delete=models.CASCADE, related_name="devs")

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50,unique=True)
    lead = models.ForeignKey(TeamLead,on_delete=models.CASCADE,related_name="Lead_teams")
    developers = models.ManyToManyField(Developer,related_name="teams")

