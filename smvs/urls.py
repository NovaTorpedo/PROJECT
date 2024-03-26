from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("login",views.login_view, name="login"),
    path("logout",views.logout_view, name="logout"),
    path("register",views.register, name="register"),
    path("create_election",views.createElection, name="createElection"),
    path("create_candidate",views.createCandidate, name="createCandidate"),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('voting/<uuid:election_id>/', views.vote, name='voting'),
    path('votesubmit', views.vote_submit, name='vote_submit'),
    path('joinelection', views.join_election, name='join_election'),
    path('voting-statistics/', views.voting_statistics, name='voting_statistics'),
]
