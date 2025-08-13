from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Team, Match
from .serializers import MatchSerializer, TeamSerializer


class TeamListView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "vlr_id"


class MatchListView(ListAPIView):
    queryset = Match.objects.all().order_by("-date_played")
    serializer_class = MatchSerializer


class MatchDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = "vlr_id"


class UpcomingMatchView(ListAPIView):
    queryset = Match.objects.filter(is_finished=False).order_by("-date_played")
    serializer_class = MatchSerializer
