# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Developer, TeamLead, Team

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.position == "Team Lead":
            team_lead = TeamLead.objects.create(tl=instance)
            Team.objects.create(lead=team_lead, team_name=instance.team)
        elif instance.position == "Dev":
            reports_to_user = User.objects.get(username=instance.reports_to)
            team_lead = TeamLead.objects.get(tl=reports_to_user)
            developer = Developer.objects.create(user=instance, lead=team_lead)
            team = Team.objects.get_or_create(lead=team_lead, team_name=instance.team)[0]
            team.developers.add(developer)
    else:
        if instance.position == "Team Lead":
            team_lead, _ = TeamLead.objects.get_or_create(tl=instance)
            team, _ = Team.objects.get_or_create(lead=team_lead, team_name=instance.team)
            team.team_name = instance.team  # Update the team name if it has changed
            team.save()
        elif instance.position == "Dev":
            reports_to_user = User.objects.get(username=instance.reports_to)
            team_lead = TeamLead.objects.get(tl=reports_to_user)
            developer, _ = Developer.objects.update_or_create(user=instance, defaults={'lead': team_lead})
            team, _ = Team.objects.get_or_create(lead=team_lead, team_name=instance.team)
            if developer not in team.developers.all():
                team.developers.add(developer)
