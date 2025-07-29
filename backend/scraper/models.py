from django.db import models


class Team(models.Model):
    name = models.CharField("Team Name", max_length=100)
    vlr_id = models.CharField("VLR Team ID", unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    ign = models.CharField("In Game Name", max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    vlr_id = models.CharField("VLR Player ID", unique=True)

    def __str__(self):
        return self.ign


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_played = models.DateField()
    vlr_id = models.CharField("VLR Match ID", unique=True)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} on {self.date_played}"


class Map(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    map_number = models.PositiveSmallIntegerField("Map Number")
    
    class Meta:
        unique_together = ("match", "name")

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
