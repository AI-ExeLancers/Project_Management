from django.contrib import admin
from .models import User, TeamLead, Team, Developer

# Register your models here.
admin.site.register(User)
admin.site.register(TeamLead)
admin.site.register(Team)
admin.site.register(Developer)