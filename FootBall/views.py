from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from datetime import *
from django.utils import timezone
from django.db.models import Q, F
from datetime import timedelta, datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
# from FootBall.forms import AddTeamForm,AddPlayerForm,CreateMatcherForm,UpdateMatcheForm,EventInlineFormSet,RefereeForm,NewsForm
from .models import *
from .forms import *

from django.views import View
from django.http import JsonResponse
from django.db.models import Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,UpdateView,ListView
from django.template.loader import render_to_string
from django.db.models import Exists, OuterRef


# Create your views here.
def Home(request):


    #Fetching league informations 
    league = League.objects.all()

    # Fetching matches that are created but not started yet
    now = timezone.now()
    future_matches = Match.objects.filter(create_at__gt=now).order_by('create_at').first()

    # Fetching the last scored match
    last_scored_match = Match.objects.filter(left_score__gt=0, right_score__gt=0).order_by('-create_at').first()

    # Initializing variables to store player information
    left_team_players = []
    right_team_players = []

    if last_scored_match:
        # Retrieving players for the left and right teams of the last scored match
        left_team_players = Player.objects.filter(team=last_scored_match.left_team)[:2]
        right_team_players = Player.objects.filter(team=last_scored_match.right_team)[:2]
 
    # news = News.objects.order_by('-publish_date')[:3] 
    news_ids = [1,2,4]
    latest_news = News.objects.filter(id__in=news_ids)

    # Specify the IDs of the news  you want to display for video 
    vnews_ids = [5,6,7]
    news_video = News.objects.filter(id__in=vnews_ids, news_video__isnull=False)
    # videos = News.objects.filter(news_video__isnull=False).order_by('-publish_date')[:2]

    blog_ids = [8,9]
    latest_blog = News.objects.filter(id__in=blog_ids)
   

#    point table 
    teams = TeamStats.objects.all().order_by('-points', '-goals_scored')


    
    

    context ={
        'league':league,
        'last_match': last_scored_match,
        'left_team_players':left_team_players,
        'right_team_players':right_team_players,
        'news':latest_news,
        'videos':news_video,
        'latest_blog':latest_blog,
        'future_matches':future_matches,
        'teams': teams,

    }
    return render(request, 'FootBall/Home.html', context)


# show matche details 
def MatcheInfo(request,match_id=None, team1_id=None, team2_id=None):

    match = get_object_or_404(Match, id=match_id)
    
    # scoring player in the match 
    left_team_scorers = match.scoring_players_left_team.all()
    right_team_scorers = match.scoring_players_right_team.all()

    # assist player in the match 
    left_team_assist = match.Total_assist_left_team.all()
    right_team_assist = match.Total_assist_right_team.all()

    # yelllow card player in the matches
    left_team_yellow = match.yellow_card_players_left_team.all()
    right_team_yellow = match.yellow_card_players_right_team.all()

    # Red card player in the matches 
    left_team_red = match.red_card_players_left_team.all()
    right_team_red = match.red_card_players_right_team.all()

    # player of the matches 
    player_of_matches = match.player_of_match


   # Initializing variables to store player information
    left_team_players = []
    right_team_players = []

    if match:
        # Retrieving players for the left and right teams of the last scored match
        left_team_players = Player.objects.filter(team=match.left_team)
        right_team_players = Player.objects.filter(team=match.right_team)

     
    #  head to head match details 
    team1 = get_object_or_404(Team, id=team1_id)
    team2 = get_object_or_404(Team, id=team2_id)

     # Fetch all matches between the two teams

    #  Match.objects.filter(left_score__gt=0, right_score__gt=0).order_by('-create_at')
    now = timezone.now()
    matches =  Match.objects.filter(
        (Q(left_team=team1, right_team=team2) | Q(left_team=team2, right_team=team1)) & Q(create_at__lt=now)
    ).order_by('create_at')

    total_matches = matches.count()
    team1_wins = matches.filter(
        Q(left_team=team1, left_score__gt=F('right_score')) | Q(right_team=team1, right_score__gt=F('left_score'))
    ).count()
    team2_wins = matches.filter(
        Q(left_team=team2, left_score__gt=F('right_score')) | Q(right_team=team2, right_score__gt=F('left_score'))
    ).count()
    draws = matches.filter(left_score=F('right_score')).count()



    # live matche time  and live match event 
    events = match.events.order_by('event_time')

    #  show point table 
    point = TeamStats.objects.all().order_by('-points', '-goals_scored')



    context = {
        'matches': match,
        'left_team_players':left_team_players,
        'right_team_players':right_team_players,

        'left_team_scoring_p':left_team_scorers,
        'right_team_scoring_p':right_team_scorers,

        'left_team_assist':left_team_assist,
        'right_team_assist':right_team_assist,

        'left_team_yellow':left_team_yellow,
        'right_team_yellow':right_team_yellow,

        'left_team_red':left_team_red,
        'right_team_red':right_team_red,  
        'player_of_matches':player_of_matches, 


        'team1': team1,
        'team2': team2,
        'total_matches': total_matches,
        'team1_wins': team1_wins,
        'team2_wins': team2_wins,
        'draws': draws,

        'allmatches':matches,
        'events':events,
        'teams':point




       
    }
    return render(request, 'FootBall/matchinfo.html',context)



  
def livematch(request):
    current_time = timezone.now()
    live_matches = Match.objects.filter(live=True)
    live_matches_data = []

     # Fetching matches that are created but not started yet
    now = timezone.now()
    future_matches = Match.objects.filter(create_at__gt=now).order_by('create_at').first()

    # all next match 
    all_future_match = Match.objects.filter(create_at__gt=now).order_by('create_at')
    future_matches_excluding_first = all_future_match[1:] 



    for match in live_matches:
        # Retrieve the last event for the match
        last_event = match.events.last()


        elapsed_time_seconds = (current_time - match.create_at).total_seconds()
        halftime_duration = 10 * 60  # Halftime duration in seconds

        if elapsed_time_seconds < 45 * 60:
            elapsed_time = elapsed_time_seconds
            halftime = False
            match_end = False
        elif 45 * 60 <= elapsed_time_seconds < (45 * 60) + halftime_duration:
            elapsed_time = 45 * 60
            halftime = True
            match_end = False
        elif (45 * 60) + halftime_duration <= elapsed_time_seconds < (90 * 60) + halftime_duration:
            elapsed_time = elapsed_time_seconds - halftime_duration
            halftime = False
            match_end = False
        else:
            elapsed_time = 90 * 60
            halftime = False
            match_end = True

        match_data = {
            'object': match,
            'elapsed_time': elapsed_time,
            'halftime': halftime,
            'match_end': match_end,
            'events': match.events.order_by('event_time'),
            'last_event': last_event,
            'start_time': match.create_at.timestamp(),
        }
        live_matches_data.append(match_data)

    context = {
        'live_matches': live_matches_data,
        'future_matches':future_matches,
        'future_matches_excluding_first':future_matches_excluding_first,
    }
    return render(request, 'FootBall/match.html', context)





# news section 
def players(request):



    context ={
      
    }

    return render (request,'FootBall/players.html', context)


# news section 
def blogs(request):
    return render (request,'FootBall/blog.html')

# news section 
def contact(request):
    return render (request,'FootBall/contact.html')

# news section 
def single_players(request):
    return render (request,'FootBall/single_ply.html')



# team list for buy ....................................................................user part 
@login_required
def team_list(request):
    # Check if the user has already purchased a team
    existing_purchase = TeamPurchase.objects.filter(buyer=request.user).first()

    if existing_purchase:
        if existing_purchase.status == 'Accepted':
            return redirect('FootBall:user_dashboard')  # Redirect to dashboard if the purchase is accepted
        elif existing_purchase.status == 'Panding':
            # Show a message that the purchase is pending
            return render(request, 'FootBall/team.html', {
                'teams': Team.objects.all(),
                'message': 'Your purchase is pending approval.',
            })
        elif existing_purchase.status == 'Rejected':
            # Show the team list again if the purchase was rejected
            return render(request, 'FootBall/team.html', {
                'teams': Team.objects.all(),
                'message': 'Your purchase was rejected. Please try again.',
            })
        
    teams = Team.objects.all().annotate(
        sold_out=Exists(TeamPurchase.objects.filter(teamname=OuterRef('pk'), status='Accepted'))
    )
    return render(request, 'FootBall/team.html', {'teams': teams})


# @login_required
# def buy_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
# Check if the team is already sold out
    if TeamPurchase.objects.filter(teamname=team, status='Accepted').exists():
        return redirect('FootBall:team_list')  # Redirect back to team list if the team is sold out

    existing_purchase = TeamPurchase.objects.filter(buyer=request.user).first()

    if existing_purchase:
        if existing_purchase.status == 'Accepted':
            return redirect('FootBall:user_dashboard')  # Redirect to dashboard if the purchase is accepted
        elif existing_purchase.status == 'Pending':
            return redirect('FootBall:team_list')  # Redirect back to team list if the purchase is pending
        elif existing_purchase.status == 'Rejected':
            existing_purchase.delete()  # Optionally delete the rejected purchase record

    if request.method == 'POST':
        purchase = TeamPurchase(teamname=team, buyer=request.user, status='Pending')
        purchase.save()
        return redirect('FootBall:team_list') 

    return render(request, 'FootBall/buy_team.html', {'team': team})



@login_required
def invoice_view(request, purchase_id):
    # Retrieve the purchase and its payment details
    purchase = get_object_or_404(TeamPurchase, id=purchase_id, buyer=request.user, status='Pending')
    payment = Payment.objects.filter(buyer=request.user, team=purchase.teamname).order_by('-payment_date').first()

    context = {
        'purchase': purchase,
        'payment': payment,
    }

    return render(request, 'FootBall/invoice.html', context)




@login_required
def buy_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if TeamPurchase.objects.filter(teamname=team, status='Accepted').exists():
        return redirect('FootBall:team_list')

    existing_purchase = TeamPurchase.objects.filter(buyer=request.user).first()

    if existing_purchase:
        if existing_purchase.status == 'Accepted':
            return redirect('FootBall:user_dashboard')
        elif existing_purchase.status == 'Pending':
            return redirect('FootBall:team_list')
        elif existing_purchase.status == 'Rejected':
            existing_purchase.delete()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            amount = form.cleaned_data['amount']

            # Save payment details
            Payment.objects.create(
                buyer=request.user,
                team=team,
                account_number=account_number,
                amount=amount
            )

            # Create a pending team purchase
            purchase = TeamPurchase(teamname=team, buyer=request.user, status='Pending')
            purchase.save()

            # Redirect to invoice view after payment
            return redirect('FootBall:invoice_view', purchase_id=purchase.id)

    else:
        form = PaymentForm()

    return render(request, 'FootBall/buy_team.html', {'team': team, 'form': form})




# user dashboard ....................................../
@login_required
def user_dashboard(request):
    purchases = TeamPurchase.objects.filter(buyer=request.user, status='Accepted')

  
    # Create a dictionary to store the match count for each purchased team
    match_counts = {}
    
    for purchase in purchases:
        team = purchase.teamname
        # Count all matches where the team is either the left_team or the right_team
        match_count = Match.objects.filter(Q(left_team=team) | Q(right_team=team)).count()
        match_counts[team.id] = match_count

    return render(request, 'FootBall/user_dashboard.html', {'purchases': purchases,'match_counts':match_count})


@login_required
def purchased_team_info_view(request):
    # Retrieve the user's team purchase, if any
    team_purchase = TeamPurchase.objects.filter(buyer=request.user, status='Accepted').first()

    team = team_purchase.teamname if team_purchase else None
    players = team.plyers.all() if team else []  # Fetch players related to the team using the related_name 'players'


    
    
    context = {
        'team_purchase': team_purchase,
        'team': team,
        'players':players,
    }

    return render(request, 'FootBall/purchased_team_info.html', context)


@login_required
def UpdateTeam_user(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        form = AddTeamFormUser(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('FootBall:purchased_team_info')
    else:
        form =AddTeamFormUser(instance=team)

    return render(request, 'FootBall/add_team_user.html', {'form':form})



def player_team_info_view(request):
    # Retrieve the user's team purchase, if any
    team_purchase = TeamPurchase.objects.filter(buyer=request.user, status='Accepted').first()

    team = team_purchase.teamname if team_purchase else None
    players = team.plyers.all() if team else []  # Fetch players related to the team using the related_name 'players'

    context = {
        'team_purchase': team_purchase,
        'team': team,
        'players':players,
        
        
    }

    return render(request, 'FootBall/player_team_info.html', context)


# add new player of the team 
@login_required
def add_player_team(request):
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, request.FILES, user=request.user)
        if player_form.is_valid():
            new_player = player_form.save()
            return redirect('FootBall:player_team_info')  # Refresh the page to show the new player
    else:
        player_form = PlayerForm(user=request.user)
    context = {

        'player_form':player_form,
        
    }
    return render(request, 'FootBall/add_player_team.html', context)



@login_required
def team_playerinfo(request, player_id):
    player = get_object_or_404(Player, id = player_id) 
    return render(request, 'FootBall/team_player_info.html', {'player':player})






# show all matche of this team 
@login_required
def team_matche_info(request):
    # Retrieve the user's accepted team purchase
    team_purchase = TeamPurchase.objects.filter(buyer=request.user, status='Accepted').first()


    now = timezone.now()

    team = team_purchase.teamname if team_purchase else None

    # Fetching all scored matches for the team
    scored_matches = Match.objects.filter(
        (Q(left_team=team) | Q(right_team=team)) & Q(create_at__lte=now)
    ).order_by('-create_at') if team else []

    # Fetching all future matches for the team
    future_matches = Match.objects.filter(
        (Q(left_team=team) | Q(right_team=team)) & Q(create_at__gt=now)
    ).order_by('create_at') if team else []

   


    context = {
        'team_purchase': team_purchase,
        'team': team,
        'scored_matches': scored_matches,
        'future_matches': future_matches,
        'scored_matches_count': scored_matches.count() if team else 0,
        'future_matches_count': future_matches.count() if team else 0,
      
    }

    return render(request, 'FootBall/team_matche_info.html', context)





# team report 
@login_required
def teamreport_user(request):
    # teamreport = Team.objects.all()
    team_purchase = TeamPurchase.objects.filter(buyer=request.user, status='Accepted').first()

    # If the user has purchased a team, show only that team
    teamreport = Team.objects.filter(id=team_purchase.teamname.id) if team_purchase else []


    context = {
        'teamreport':teamreport,
    }
    return render(request, 'FootBall/team_report_user.html', context)


def team_report_info_view_user(request, team_id):
    team = get_object_or_404(Team, id=team_id)
  
    team_stats = TeamStats.objects.get(team=team)


     # Query for won matches
    won_matches = Match.objects.filter(
        (Q(left_team=team) & Q(left_score__gt=F('right_score'))) |
        (Q(right_team=team) & Q(right_score__gt=F('left_score')))
    )
    
    # Query for lost matches
    lost_matches = Match.objects.filter(
        (Q(left_team=team) & Q(left_score__lt=F('right_score'))) |
        (Q(right_team=team) & Q(right_score__lt=F('left_score')))
    )

     # Query for drawn matches
    draw_matches = Match.objects.filter(
        (Q(left_team=team) | Q(right_team=team)) &
        Q(left_score=F('right_score'))
    )
    

    context = {
        'team': team,
        'teams':team_stats,
        'won_matches': won_matches,
        'lost_matches': lost_matches,
        'draw_matches':draw_matches,
     
    }
    return render(request, 'FootBall/team_report_info_user.html', context)







# admin dashboard  .................................................................... admin part 
@login_required
def admin_dashboard(request):
    team = Team.objects.count()
    player = Player.objects.count()
    # matches = Match.objects.count()
    referee = Referee.objects.count()
     
    now = timezone.now()
    all_scored_match = Match.objects.filter(create_at__lte=now).order_by('create_at').count()


    #  point table  
    teamspoint = TeamStats.objects.all().order_by('-points', '-goals_scored')

    context = {
        'totalteam':team,
        'totalplayer':player,
        'totalmatcher':all_scored_match,
        'totalraferee':referee,
        'teamspoint':teamspoint
    }
    return render(request, 'FootBall/admin_dashboard.html',context)


# admin team list 
@login_required
def adminteam(request):
    teams = Team.objects.all()
    return render(request, 'FootBall/admin_team.html', {'teams': teams})



    
# class AddTeam(LoginRequiredMixin, CreateView):
#     model = Team
#     template_name = 'FootBall/add_team.html'
#     fields = ('team_name', 'coach_name', 'batch_name', 'phone', 'email','price', 'team_logo')

#     def form_valid(self, form):
#         team_obj = form.save(commit=False)
#         team_obj.user =self.request.user
#         team_obj.save()
#         return HttpResponseRedirect(reverse('admin_team'))

# add team 
@login_required
def add_team(request):
    form = AddTeamForm()
    if request.method =='POST':
        form = AddTeamForm(request.POST, request.FILES)
        if form.is_valid():
            team_obj = form.save(commit=False)
            team_obj.user =request.user
            team_obj.save()
            return HttpResponseRedirect(reverse('FootBall:admin_team'))
    return render(request, 'FootBall/add_team.html', context={'form': form})


# update team 
@login_required
def UpdateTeam(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.method == 'POST':
        form = AddTeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('FootBall:admin_team')
    else:
        form =AddTeamForm(instance=team)

    return render(request, 'FootBall/add_team.html', {'form':form})


# delete team 
from django.contrib import messages
@login_required
def DeleteTeam(request, del_id):
    team = get_object_or_404(Team, pk=del_id)
    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Team Deleted Successfully. ')

    return render(request, 'FootBall/del_team.html', {'team':team})



# player list

class Player_list(LoginRequiredMixin,ListView):
    context_object_name = 'player'
    model = Player
    template_name = 'FootBall/player_list.html'
    fields = ('player_name', 'player_jersey_no', 'player_uid', 'phone', 'email', 'play_position','batch','team')


# player info 
@login_required
def playerinfo(request, player_id):
    player = get_object_or_404(Player, id = player_id) 
    return render(request, 'FootBall/player_info.html', {'player':player})


# add Player
@login_required
def add_player(request):
    form = AddPlayerForm()
    if request.method =='POST':
        form = AddPlayerForm(request.POST, request.FILES)
        if form.is_valid():
            team_obj = form.save(commit=False)
            team_obj.user =request.user
            team_obj.save()
            return HttpResponseRedirect(reverse('FootBall:player_list'))
    return render(request, 'FootBall/add_player.html', context={'form': form})


# update player 
@login_required
def UpdatePlayer(request, pk):
    player = get_object_or_404(Player, pk=pk)

    if request.method == 'POST':
        form = AddPlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('FootBall:player_list'))
    else:
        form =AddPlayerForm(instance=player)

    return render(request, 'FootBall/add_player.html', {'form':form})

# delete player 
@login_required
def Deleteplayer(request, del_id):
    player = get_object_or_404(Player, pk=del_id)
    if request.method == 'POST':
        player.delete()
        messages.success(request, 'player Deleted Successfully. ')

    return render(request, 'FootBall/del_player.html', {'player':player})


# matche list 
@login_required
def matchelist(request):
    now = timezone.now()
    # featching all scored matches 
    all_scored_matche= Match.objects.filter(create_at__lte=now).order_by('-create_at')
    all_scored= Match.objects.filter(create_at__lte=now).order_by('-create_at').count()

    #  featching all future matches 
    all_future_match = Match.objects.filter(create_at__gt=now).order_by('create_at')
    all_future = Match.objects.filter(create_at__gt=now).order_by('create_at').count()

    # total match 
    total_match = Match.objects.count()



    context ={
        'all_scored_matche':all_scored_matche,
        'all_future_match':all_future_match,
        'all_scored':all_scored,
        'all_future':all_future,
        'total_match':total_match,
    }
    return render(request, 'FootBall/AdMatch_list.html', context)





# create match 
@login_required
def create_match(request):
    if request.method == 'POST':
        form = CreateMatcherForm(request.POST,request.FILES)
        if form.is_valid():
            match_obj = form.save(commit=False)
            match_obj.user = request.user
            match_obj.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('FootBall:matches_list'))
    else:
        form = CreateMatcherForm()

    return render(request, 'FootBall/create_match.html', {'form': form})




# update match 

class update_match(LoginRequiredMixin,UpdateView):
    model = Match
    form_class = UpdateMatcheForm
    template_name = 'FootBall/create_match.html'
    success_url = reverse_lazy('FootBall:matches_list')  # Adjust this to your success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.object
        
        if self.request.POST:
            context['event_formset'] = EventInlineFormSet(self.request.POST, queryset=match.events.all(), match=match)
        else:
            context['event_formset'] = EventInlineFormSet(queryset=match.events.all(), match=match)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        event_formset = context['event_formset']
        
        if form.is_valid() and event_formset.is_valid():
            self.object = form.save()
            for event_form in event_formset:
                event_instance = event_form.save(commit=False)  # Do not save yet
                event_instance.matche = self.object  # Set the match instance
                event_instance.save()  # Now save the event instance
        
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))
    


# refeere list 
@login_required
def refeere(request):
    refeere = Referee.objects.all()
    return render(request, 'Football/referee.html', {'refeere':refeere})




# add refeere
@login_required
def add_refeere(request):
    form = RefereeForm()
    if request.method =='POST':
        form = RefereeForm(request.POST, request.FILES)
        if form.is_valid():
            team_obj = form.save(commit=False)
            team_obj.user =request.user
            team_obj.save()
            return HttpResponseRedirect(reverse('FootBall:referee'))
    return render(request, 'FootBall/add_referee.html', context={'form': form})






# update refeere 
@login_required
def UpdateReferee(request, pk):
    player = get_object_or_404(Referee, pk=pk)

    if request.method == 'POST':
        form = RefereeForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('FootBall:referee'))
    else:
        form =RefereeForm(instance=player)

    return render(request, 'FootBall/add_referee.html', {'form':form})



# delete player 
@login_required
def DeleteRefee(request, del_id):
    refeere = get_object_or_404(Referee, pk=del_id)
    if request.method == 'POST':
        refeere.delete()
        messages.success(request, 'player Deleted Successfully. ')

    return render(request, 'FootBall/del_refeere.html', {'refeere':refeere})




# news crud 
@login_required
def newslist(request):
    news = News.objects.all()

    context = {
        'news':news,   
    }
    return render(request, 'FootBall/news_list.html', context)




# add refeere
@login_required
def add_News(request):
    form = NewsForm()
    if request.method =='POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_obj = form.save(commit=False)
            news_obj.user =request.user
            news_obj.save()
            return HttpResponseRedirect(reverse('FootBall:news_list'))
    return render(request, 'FootBall/add_news.html', context={'form': form})




# update news form 
@login_required
def UpdateNews(request, pk):
    news = get_object_or_404(News, pk=pk)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('FootBall:news_list'))
    else:
        form =NewsForm(instance=news)

    return render(request, 'FootBall/add_news.html', {'form':form})


# delete player 
@login_required
def DeleteNews(request, del_id):
    news = get_object_or_404(News, pk=del_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'News Deleted Successfully. ')

    return render(request, 'FootBall/del_news.html', {'news':news})




# League crud 
@login_required
def leaguelist(request):
    league = League.objects.all()

    context = {
        'league':league,   
    }
    return render(request, 'FootBall/league_list.html', context)


# add League
@login_required
def add_league(request):
    form = LeagueForm()
    if request.method =='POST':
        form = LeagueForm(request.POST, request.FILES)
        if form.is_valid():
            leag_obj = form.save(commit=False)
            leag_obj.user =request.user
            leag_obj.save()
            return HttpResponseRedirect(reverse('FootBall:league_list'))
    return render(request, 'FootBall/add_league.html', context={'form': form})




# update League form 
@login_required
def Updateleague(request, pk):
    news = get_object_or_404(League, pk=pk)

    if request.method == 'POST':
        form = LeagueForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('FootBall:league_list'))
    else:
        form =LeagueForm(instance=news)

    return render(request, 'FootBall/add_league.html', {'form':form})



# delete player 
@login_required
def Deleteleague(request, del_id):
    league = get_object_or_404(League, pk=del_id)
    if request.method == 'POST':
        league.delete()
        messages.success(request, 'League Deleted Successfully. ')

    return render(request, 'FootBall/del_league.html', {'league':league})



# Team Purchase .........
@login_required
def teampurchase(request):
    team_purchase = TeamPurchase.objects.all()

    context = {
        'team_purchase':team_purchase
    }
    return render(request, 'FootBall/team_purchase.html', context)


@login_required
def Paymentdetails(request):
    Paymentdetails = Payment.objects.all()

    context = {
        'Payment':Paymentdetails
    }
    return render(request, 'FootBall/payment_details.html', context)


@login_required
def UpdateteamPur(request, pk):
    news = get_object_or_404(TeamPurchase, pk=pk)

    if request.method == 'POST':
        form = TeamPurchaseForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('FootBall:team_purchase'))
    else:
        form =TeamPurchaseForm(instance=news)

    return render(request, 'FootBall/update_Teampurchase.html', {'form':form})


# delete Team purchase 
@login_required
def DeleteTeamPurchase(request, del_id):
    teampurchase = get_object_or_404(TeamPurchase, pk=del_id)
    if request.method == 'POST':
        teampurchase.delete()
        messages.success(request, 'Teampurchase Deleted Successfully. ')

    return render(request, 'FootBall/del_teampurchase.html', {'league':teampurchase})


# team report 
@login_required
def teamreport(request):
    teamreport = Team.objects.all()

    context = {
        'teamreport':teamreport,
    }
    return render(request, 'FootBall/team_report.html', context)


def team_report_info_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
  
    team_stats = TeamStats.objects.get(team=team)


     # Query for won matches
    won_matches = Match.objects.filter(
        (Q(left_team=team) & Q(left_score__gt=F('right_score'))) |
        (Q(right_team=team) & Q(right_score__gt=F('left_score')))
    )
    
    # Query for lost matches
    lost_matches = Match.objects.filter(
        (Q(left_team=team) & Q(left_score__lt=F('right_score'))) |
        (Q(right_team=team) & Q(right_score__lt=F('left_score')))
    )

     # Query for drawn matches
    draw_matches = Match.objects.filter(
        (Q(left_team=team) | Q(right_team=team)) &
        Q(left_score=F('right_score'))
    )
    

    context = {
        'team': team,
        'teams':team_stats,
        'won_matches': won_matches,
        'lost_matches': lost_matches,
        'draw_matches':draw_matches,
     
    }
    return render(request, 'FootBall/team_report_info.html', context)



# Matche report 
@login_required
def Matchereport(request):
    matche = Match.objects.all()

    context = {
        'matche':matche,
    }
    return render(request, 'FootBall/matche_report.html', context)


