from django.shortcuts import render
from .models import User, Election, Candidate, Votes
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import create_candidate, create_election

# Create your views here.
def index(request):
        return render(request, "smvs/index.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign the user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "smvs/login.html", {
                "message": "Invalid username/password."
            })
    else:
        return render(request, "smvs/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "smvs/register.html", {
                "message": "Password must match"
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, "smvs/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "smvs/register.html")

def createCandidate(request):
    if request.method == "POST":
        firstname = request.POST.get(f'first_name')
        middlename = request.POST.get(f'middle_name')
        lastname = request.POST.get(f'last_name')
        email = request.POST.get(f'email')
        phonenumber = request.POST.get(f'phone_number')
        partyaffiliation = request.POST.get(f'party_affiliation')
        profilepicture = request.FILES.get(f'profile_picture')
        created_by = request.user

        candidate = Candidate(
            first_name=firstname,
            middle_name=middlename,
            last_name=lastname,
            email=email,
            phone_number=phonenumber,
            party_affiliation=partyaffiliation,
            profile_picture=profilepicture,
            created_by=created_by
        )
        candidate.save()
        return redirect(createCandidate) # Redirect to the index page after saving all the candidates
    else:
        return render(request, 'smvs/createcandidate.html')

def createElection(request):
    user = request.user
    candidates = Candidate.objects.filter(created_by=user)

    if request.method == "POST":
        position = request.POST['position']
        candidate_ids = request.POST.getlist('candidates')  # Get a list of selected candidate IDs
        start_date_time = request.POST['startDateTime']
        end_date_time = request.POST['endDateTime']
        user = request.user

        election = Election(position=position, startDateTime=start_date_time, endDateTime=end_date_time, user=user)
        election.save()

        # Assign candidates to the election using set()
        election.candidates.set(candidate_ids)

        return HttpResponseRedirect(reverse(vote, kwargs={"election_id":election.id}))

    return render(request, "smvs/createelection.html", {
        "candidates": candidates  # Pass candidates queryset to the template context
    })

def vote(request, election_id):
    return render(request,"smvs/voting.html")