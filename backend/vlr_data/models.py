from django.db import models


class Team(models.Model):
    name = models.CharField("Team Name", max_length=100)
    team_tag = models.CharField("Team Tag", max_length=5)
    team_rating = models.PositiveSmallIntegerField("Team Rating")
    vlr_id = models.CharField("VLR Team ID", unique=True)
    last_updated = models.DateTimeField("Last Updated")

    def __str__(self):
        return self.name


class Player(models.Model):
    ign = models.CharField("In Game Name", max_length=100)
    real_name = models.CharField("Real Name", max_length=200)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    vlr_id = models.CharField("VLR Player ID", unique=True)
    last_updated = models.DateTimeField("Last Updated")

    def __str__(self):
        return self.ign


class Event(models.Model):
    name = models.Charfield("Event", max_length=100)
    series = models.CharField("Series", max_length=100)
    vlr_url = models.URLField("Event Series URL", unique=True)


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_played = models.DateTimeField("Match Date")
    vlr_id = models.CharField("VLR Match ID", unique=True)
    is_finished = models.BooleanField("Match Finished")
    team1_score = models.PositiveSmallIntegerField("Team 1 Score")
    team2_score = models.PositiveSmallIntegerField("Team 2 Score")

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} on {self.date_played}"


class Map(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    map_number = models.PositiveSmallIntegerField("Map Number")
    game_id = models.CharField("VLR Game ID", unique=True)
    team1_score = models.PositiveSmallIntegerField("Team 1 Score")
    team2_score = models.PositiveSmallIntegerField("Team 2 Score")

    def __str__(self):
        return f"{self.name} - {self.match}"


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    kills = models.PositiveSmallIntegerField("Kills")
    deaths = models.PositiveSmallIntegerField("Deaths")
    assists = models.PositiveSmallIntegerField("Assists")
    acs = models.PositiveSmallIntegerField("Average Combat Score")
    agent = models.CharField("Agent Played")

    class Meta:
        unique_together = ("player", "map")

    def __str__(self):
        return f"{self.player.ign} on {self.map.name}"
