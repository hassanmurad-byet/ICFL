from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from django.db.models import Q
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Sum
from django.db.models.signals import post_save, m2m_changed

# Create your models here.



BATCH_CHOICES = [
    ('201','201'),
    ('202', '202'),
    ('203', '203'),
    ('211', '211'),
    ('212', '212'),
    ('213', '213'),
    ('221', '221'),
    ('222', '222'),
    ('223', '223'),
    ('231', '231'),
    ('232', '232'),
    ('233', '233'),
    ('241', '241'),
    ('242', '242'),
]

POSITION_PLAY =[
    ('GK','Goalkeeper'),
    ('SW','Sweeper'),
    ('CB','Centre Back'),
    ('FB','Full Back'),
    ('WB','Wing Back'),
    ('DM','Defensive Midfielder'),
    ('CM','Centre Midfielder'),
    ('WM','Wing Midfielder'),
    ('AM','Attacking Midfielder'),
    ('WF','Wing Forward'),
    ('CF','Centre Forward'),

]
BLOOD_CHOICES = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),

]
GROUP_CHOICES =[
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E','E'),
]
FORM_CHOICES =[
    ('DRAW', 'D'),
    ('WIN', 'W'),
    ('LOST', 'L'),

]
TEAM_STATUS = [
    ('Panding', 'Panding'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),

]


class Team(models.Model):
    team_name = models.CharField(max_length=30, verbose_name="team name")
    team_logo = models.ImageField(upload_to="team_logo", verbose_name="Team Logo")
    coach_name = models.CharField(max_length=20, verbose_name="Coach Name")
    batch_name = models.CharField(choices=BATCH_CHOICES, max_length=20)
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(max_length=50, verbose_name="Team Email")
    price = models.DecimalField(max_digits=10, decimal_places=2)
   

    def __str__(self):
        return str(self.team_name)


class Player(models.Model):
    player_name = models.CharField(max_length=50, verbose_name="player name")
    image = models.ImageField(upload_to='player_images')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="plyers")
    player_uid = models.CharField(max_length=10, verbose_name="Player ID")
    batch = models.CharField(choices=BATCH_CHOICES, max_length=20, verbose_name="Select Batch ")
    player_jersey_no = models.SmallIntegerField(default=0,verbose_name="Player Jersey No")
    phone = models.CharField(max_length=20, verbose_name="Player Phone")
    email = models.EmailField(max_length=50, verbose_name="Player Email")
    blood_group = models.CharField(choices=BLOOD_CHOICES, max_length=20, verbose_name="Blood Group")
    age = models.CharField(max_length=10, verbose_name="Player Age")
    height = models.PositiveIntegerField(default=0, verbose_name="Player Height (cm)")
    weight = models.PositiveIntegerField(default=0, verbose_name="Player Weight (kg)")
    footed = models.CharField(max_length=50, verbose_name="Footed (Left or Right)")
    play_position = models.CharField(choices=POSITION_PLAY, max_length=50, verbose_name="Position Play")

    total_goals = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Total Goals")
    Total_assist = models.PositiveIntegerField(default=0, verbose_name="Total Goals Assists")
    total_matches = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Total Matches")
    yellow_cards = models.PositiveIntegerField(default=0, verbose_name="Yellow Cards")
    red_cards = models.PositiveIntegerField(default=0, verbose_name="Red Cards")
    totalplayer_of_match = models.PositiveIntegerField(default=0, verbose_name="Total Player of the Match")

    def __str__(self):
        return self.player_name



    
class Referee(models.Model):
    referee_name = models.CharField(max_length=50, verbose_name="Referee Name")
    referee_img = models.ImageField(upload_to='referee_images')
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(max_length=50, verbose_name="Email")
    info = models.TextField()
    total_officiated = models.PositiveIntegerField(verbose_name="Total Matches Officiated")

    def __str__(self):
        return self.referee_name


class TeamStats(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="stats")
    matches_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)


    @property
    def win_percentage(self):
        if self.matches_played > 0:
            return (self.wins / self.matches_played) * 100
        return 0
    
    @property
    def loss_percentage(self):
        if self.matches_played > 0:
            return (self.losses / self.matches_played) * 100
        return 0
    
    @property
    def draws_percentage(self):
        if self.matches_played > 0:
            return (self.draws / self.matches_played) * 100
        return 0

    def __str__(self):
        return f"{self.team.name} Stats"





class Match(models.Model):
    left_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="left_matches")
    right_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="right_matches")
    left_score = models.PositiveIntegerField(default=0, verbose_name="Left Team Score")
    right_score = models.PositiveIntegerField(default=0, verbose_name="Right Team Score")

    scoring_players_left_team = models.ManyToManyField(Player, related_name="left_team_scoring_matches", blank=True)
    scoring_players_right_team = models.ManyToManyField(Player, related_name="right_team_scoring_matches", blank=True)
    Total_assist_left_team = models.ManyToManyField(Player, related_name="left_team_Total_assist", blank=True)
    Total_assist_right_team = models.ManyToManyField(Player, related_name="right_team_Total_assist", blank=True)

    yellow_card_players_left_team = models.ManyToManyField(Player, related_name="left_team_yellow_card_matches", blank=True)
    yellow_card_players_right_team = models.ManyToManyField(Player, related_name="right_team_yellow_card_matches", blank=True)
    red_card_players_left_team = models.ManyToManyField(Player, related_name="left_team_red_card_matches", blank=True)
    red_card_players_right_team = models.ManyToManyField(Player, related_name="right_team_red_card_matches", blank=True)
    player_of_match = models.ForeignKey(Player, related_name="player_of_match", on_delete=models.SET_NULL, null=True, blank=True)

    left_formation = models.CharField(max_length=10, verbose_name="Left Team Formation 4-3-3-1",blank=True,)
    right_formation = models.CharField(max_length=10, verbose_name="Right Team Formation 4-4-2-1",blank=True)
    referee = models.ForeignKey(Referee,  on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name="Match Time", auto_now_add=False)
    match_details = models.TextField(verbose_name="Match Details",blank=True)
    location = models.CharField(max_length=100, verbose_name="Match Location")
    img = models.ImageField(upload_to='match_images', null=True, blank=True)
    highlights = models.FileField(
        upload_to='videos', null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
    )
    live = models.BooleanField(default=True)
     
    # class Meta:
    #     ordering = ('create_at',)

  
    def __str__(self):
        return "{} vs {}".format(self.left_team.team_name, self.right_team.team_name)
    



    @property
    def get_left_team_name(self):
        return "".format(self.left_team.team_name)
    
    @property
    def get_right_team_name(self):
        return "".format(self.right_team.team_name)






EVENT_CHOICES = [
       ('start', 'start'),
        ('goal','goal'),
        ('corner', 'corner'),
        ('foul', 'foul'),
        ('penalty', 'penalty'),
        ('offside','offside'),
        ('red', 'red card'),
        ('yellow', 'yellow card'),
       
    ]

class Event(models.Model):
    matche = models.ForeignKey(Match, related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=40,choices=EVENT_CHOICES,  default='None',blank=True, null=True)
    event_time = models.PositiveIntegerField(help_text='Time in minutes', default=0, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='events_plyer', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.event_type} - {self.matche} - {self.event_time}'"

    


class League(models.Model):
    league_name = models.CharField(max_length=200, verbose_name='Name')
    info = models.CharField(max_length=254, verbose_name='Informations', blank=True)
    teams = models.ManyToManyField(Team, related_name='league_teams',blank=True)
    times = models.DateTimeField(auto_now_add=False, blank=True)
 
    def __str__(self):
        return self.league_name
    

class News(models.Model):   
    news_title = models.CharField(max_length=50,default="", verbose_name="Title")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_author')
    news_content = models.TextField(verbose_name="Content")
    news_image = models.ImageField(upload_to='news_images', null=True, blank=True, verbose_name="Image")
    news_video = models.FileField(
        upload_to='news_videos', null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
    )
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.news_title




class TeamPurchase(models.Model):
    teamname= models.ForeignKey(Team, on_delete=models.CASCADE, related_name='buy_team')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=TEAM_STATUS, max_length=255, default='Panding')



class Payment(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.team.team_name} by {self.buyer.username}"