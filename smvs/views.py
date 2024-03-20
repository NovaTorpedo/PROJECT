from django.shortcuts import render
from .models import User, Election, Candidate, Votes
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
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
                "message": "Invalid username or password!"
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

from django.db.models import Count, Q

def vote(request, election_id):
    user = request.user
    elections = Election.objects.filter(id=election_id)

    try:
        # Retrieve the election associated with the provided election_id
        election = Election.objects.get(id=election_id)

        # Get all candidates for the election
        candidates = election.candidates.all()

        # Create a dictionary to store candidate names and their total votes
        candidate_votes = {}

        # Create a dictionary to store user details who voted for each candidate
        user_votes = {}

        # Calculate the total votes for each candidate and store user details
        for candidate in candidates:
            votes_for_candidate = Votes.objects.filter(candidate=candidate, election__id=election_id)
            total_votes_for_candidate = votes_for_candidate.count()
            candidate_votes[candidate.full_name()] = total_votes_for_candidate

            # Store usernames of users who voted for this candidate
            user_votes[candidate.full_name()] = [vote.user.username for vote in votes_for_candidate]
    except Election.DoesNotExist:
        # If the election doesn't exist, set candidates to an empty list
        candidates = []
        candidate_votes = {}
        user_votes = {}

    try:
        # Retrieve the election associated with the provided election_id
        election = Election.objects.get(id=election_id)

        # Get all votes for this election
        votes_for_election = Votes.objects.filter(election=election)

        # Get the id of users who voted
        participating_users = [vote.user.id for vote in votes_for_election]
    except Election.DoesNotExist:
        # If the election doesn't exist, set participating_users to an empty list
        participating_users = []

    return render(request, "smvs/voting.html", {
        "elections": elections,
        "candidates": candidates,
        "votes": candidate_votes,
        "user_votes": participating_users
    })

def vote_submit(request):
    if request.method == 'POST':
        # Get the candidate ID from the form submission
        candidate_id = request.POST.get('candidate_id')

        try:
            # Retrieve the candidate based on the candidate_id
            candidate = Candidate.objects.get(id=candidate_id)

            # Create a vote record for the user and candidate
            vote, created = Votes.objects.get_or_create(user=request.user, candidate=candidate, election=candidate.elections.first())

            if created:
                # Vote was successfully recorded
                return redirect('voting', election_id=candidate.elections.first().id)  # Redirect to a success page
            else:
                # User has already voted for this candidate
                return redirect('voting', election_id=candidate.elections.first().id)  # Redirect to a failure page
        except Candidate.DoesNotExist:
            # Candidate not found
            return redirect('voting', election_id=candidate.elections.first().id)  # Redirect to a failure page
    else:
        # Invalid request method
        return HttpResponseBadRequest("Invalid request method")
    
def join_election(request):
    if request.method == 'POST':
        # Get the election ID from the form submission
        election_id = request.POST.get('code')

        return HttpResponseRedirect(reverse(vote, kwargs={"election_id":election_id}))
    else:
        # Invalid request method
        return render(request, 'index.html')