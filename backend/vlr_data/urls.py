from django.urls import path
from .views import (
    MatchDetailView,
    MatchListView,
    TeamDetailView,
    TeamListView,
    UpcomingMatchView,
    PlayerDetailView
)

urlpatterns = [
    path("teams", TeamListView.as_view(), name="team_list"),
    path("team/<str:vlr_id>", TeamDetailView.as_view(), name="team_detail"),
    path("matches", MatchListView.as_view(), name="match_list"),
    path("match/<str:vlr_id>", MatchDetailView.as_view(), name="match_detail"),
    path("upcoming_matches", UpcomingMatchView.as_view(), name="upcoming_matches"),
    path("player/<str:vlr_id>", PlayerDetailView.as_view(), name="player_detail"),
]
