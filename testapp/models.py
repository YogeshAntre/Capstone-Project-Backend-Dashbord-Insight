from django.db import models

# Create your models here.
class Match(models.Model):
    match_id = models.CharField(max_length=50, unique=True)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    winner = models.CharField(max_length=100, null=True, blank=True)
    margin = models.CharField(max_length=50, null=True, blank=True)
    ground = models.CharField(max_length=100)
    match_date = models.DateField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} ({self.match_id})"
    

class Player(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50)
    batting_style = models.CharField(max_length=50, null=True, blank=True)
    bowling_style = models.CharField(max_length=50, null=True, blank=True)
    od_matches = models.IntegerField(default=0)
    domestic_team = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Bowling(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    overs = models.FloatField()
    maidens = models.IntegerField(default=0)
    runs_conceded = models.IntegerField()
    wickets = models.IntegerField()
    economy = models.FloatField()

    dot_balls = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)

    wides = models.IntegerField(default=0)
    no_balls = models.IntegerField(default=0)

    bowling_position = models.IntegerField()
    bowling_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.player.name} ({self.match.match_id}) - {self.wickets} wickets"



class Batting(models.Model):

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    runs = models.IntegerField()
    balls = models.IntegerField()
    minutes = models.IntegerField(null=True, blank=True)
    dismissal = models.CharField(max_length=100, null=True, blank=True)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    strike_rate = models.FloatField(null=True, blank=True)
    batting_position = models.IntegerField(null=True, blank=True)
    batting_team = models.CharField(max_length=100)
    class Meta:
        unique_together = ('match', 'player') 

    def __str__(self):
        return f"{self.player.name} - {self.match.match_name}"
    
    
						
