from django import forms
from .models import Team,Player,Match,Event,Referee,News,League,TeamPurchase
from django.forms.models import inlineformset_factory



class AddTeamForm(forms.ModelForm):
    class Meta:
        model= Team
        fields = ['team_name', 'coach_name', 'batch_name', 'phone', 'email','price', 'team_logo']



class AddTeamFormUser(forms.ModelForm):
    class Meta:
        model= Team
        fields = ['coach_name', 'batch_name', 'phone', 'email', 'team_logo']


class AddPlayerForm(forms.ModelForm):
    class Meta:
        model= Player
        fields = ['player_name', 'player_jersey_no', 'player_uid','phone', 'email','age', 'height','weight','footed','blood_group','play_position','batch','team','image']



class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['player_name', 'player_jersey_no', 'player_uid','phone', 'email','age', 'height','weight','footed','blood_group','play_position','batch','team','image']
        

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlayerForm, self).__init__(*args, **kwargs)
        if user:
            purchased_team = TeamPurchase.objects.filter(buyer=user, status='Accepted').first()
            if purchased_team:
                self.fields['team'].queryset = Team.objects.filter(id=purchased_team.teamname.id)
            else:
                self.fields['team'].queryset = Team.objects.none()



# for create thew matche 
class CreateMatcherForm(forms.ModelForm):
    class Meta:
        model= Match
        fields = ['left_team', 'right_team','left_formation','right_formation','referee','match_details','location','img','highlights','create_at','live']
        
     # Use a DateTimePicker widget for the match_date_time field
    create_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )




# for update the matche form
class UpdateMatcheForm(forms.ModelForm):
    class Meta:
        model= Match
        fields = ['left_team', 'right_team', 'left_score','right_score', 'scoring_players_left_team','scoring_players_right_team', 'Total_assist_left_team','Total_assist_right_team','yellow_card_players_left_team','yellow_card_players_right_team','red_card_players_left_team','red_card_players_right_team','player_of_match','left_formation',
                  'right_formation','referee','match_details','location','img','highlights','create_at','live']

     # Use a DateTimePicker widget for the match_date_time field
    create_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )

    widgets = {
            'scoring_players_left_team': forms.CheckboxSelectMultiple,
            'scoring_players_right_team': forms.CheckboxSelectMultiple,
            'Total_assist_left_team': forms.CheckboxSelectMultiple,
            'Total_assist_right_team': forms.CheckboxSelectMultiple,
            'yellow_card_players_left_team': forms.CheckboxSelectMultiple,
            'yellow_card_players_right_team': forms.CheckboxSelectMultiple,
            'red_card_players_left_team': forms.CheckboxSelectMultiple,
            'red_card_players_right_team': forms.CheckboxSelectMultiple,
            'player_of_match': forms.Select
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.left_team and instance.right_team:
                self.fields['scoring_players_left_team'].queryset = Player.objects.filter(team=instance.left_team)
                self.fields['scoring_players_right_team'].queryset = Player.objects.filter(team=instance.right_team)
                self.fields['Total_assist_left_team'].queryset = Player.objects.filter(team=instance.left_team)
                self.fields['Total_assist_right_team'].queryset = Player.objects.filter(team=instance.right_team)
                self.fields['yellow_card_players_left_team'].queryset = Player.objects.filter(team=instance.left_team)
                self.fields['yellow_card_players_right_team'].queryset = Player.objects.filter(team=instance.right_team)
                self.fields['red_card_players_left_team'].queryset = Player.objects.filter(team=instance.left_team)
                self.fields['red_card_players_right_team'].queryset = Player.objects.filter(team=instance.right_team)
                self.fields['player_of_match'].queryset = Player.objects.filter(team__in=[instance.left_team, instance.right_team])
            else:
                self.fields['scoring_players_left_team'].queryset = Player.objects.none()
                self.fields['scoring_players_right_team'].queryset = Player.objects.none()
                self.fields['Total_assist_left_team'].queryset = Player.objects.none()
                self.fields['Total_assist_right_team'].queryset = Player.objects.none()
                self.fields['yellow_card_players_left_team'].queryset = Player.objects.none()
                self.fields['yellow_card_players_right_team'].queryset = Player.objects.none()
                self.fields['red_card_players_left_team'].queryset = Player.objects.none()
                self.fields['red_card_players_right_team'].queryset = Player.objects.none()
                self.fields['player_of_match'].queryset = Player.objects.none()

from django.forms import modelformset_factory, BaseModelFormSet

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_type', 'event_time', 'player', 'description']

    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match', None)  # Extract the match parameter
        super().__init__(*args, **kwargs)
        if match:
            # Filter players based on the teams in the match
            self.fields['player'].queryset = Player.objects.filter(team__in=[match.left_team, match.right_team])

class BaseEventFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match', None)  # Extract the match parameter
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.match = match  # Pass the match to each form

# Create a formset for the Event model
EventInlineFormSet = modelformset_factory(Event, form=EventForm, formset=BaseEventFormSet, extra=1)




class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['referee_name', 'phone', 'email', 'info','total_officiated','referee_img']



class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['news_title', 'author', 'news_content', 'news_image','news_video']



class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['league_name', 'info', 'teams', 'times']



class TeamPurchaseForm(forms.ModelForm):
    class Meta:
        model = TeamPurchase
        fields = ['status']
        

class PaymentForm(forms.Form):
    account_number = forms.CharField(max_length=20, label="Account Number")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")