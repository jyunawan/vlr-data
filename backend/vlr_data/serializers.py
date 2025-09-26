from rest_framework.serializers import ModelSerializer, CharField

from .models import Match, Player, Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "team_tag", "team_rating", "vlr_id", "last_updated"]


class MatchSerializer(ModelSerializer):
    team1_id = CharField(source="team1.vlr_id", read_only=True)
    team2_id = CharField(source="team2.vlr_id", read_only=True)
    team1_logo = CharField(source="team1.team_logo_url", read_only=True)
    team2_logo = CharField(source="team2.team_logo_url", read_only=True)
    team1 = CharField(source="team1.name", read_only=True)
    team2 = CharField(source="team2.name", read_only=True)
    event = CharField(source="event.vlr_url", read_only=True)
    
    class Meta:
        model = Match
        fields = [
            "event",
            "team1_id",
            "team2_id",
            "team1",
            "team2",
            "team1_logo",
            "team2_logo",
            "date_played",
            "vlr_id",
            "is_finished",
            "team1_score",
            "team2_score",
        ]
        
class PlayerSerializer(ModelSerializer):
    team = CharField(source="team.vlr_id", read_only = True)
    
    class Meta:
        model = Player
        fields = [
            "ign",
            "real_name",
            "team",
            "vlr_id"
        ]
