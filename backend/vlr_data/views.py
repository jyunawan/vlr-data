from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Player, Team, Match
from .serializers import MatchSerializer, PlayerSerializer, TeamSerializer


class TeamListView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
        
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "vlr_id"


class MatchListView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
        
    queryset = Match.objects.all().order_by("-date_played")
    serializer_class = MatchSerializer


class MatchDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
        
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = "vlr_id"


class UpcomingMatchView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    
    queryset = Match.objects.filter(is_finished=False).order_by("date_played")
    serializer_class = MatchSerializer
    
class PlayerDetailView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
        
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = "vlr_id"
