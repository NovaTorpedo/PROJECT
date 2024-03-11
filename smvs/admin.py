from django.contrib import admin
from .models import User, Election, Candidate, Votes

# Register your models here.
admin.site.register(User)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Votes)
