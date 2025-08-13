from rest_framework.serializers import ModelSerializer

from .models import Match, Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "team_tag", "team_rating", "vlr_id", "last_updated"]


class MatchSerializer(ModelSerializer):
    class Meta:
        model = Match
        fields = [
            "event",
            "team1",
            "team2",
            "date_played",
            "vlr_id",
            "is_finished",
            "team1_score",
            "team2_score",
        ]
