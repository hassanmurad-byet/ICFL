from django.contrib import admin
from .models import(Player,Team,TeamStats,Referee,Match,News,League,Event,TeamPurchase,Payment)





@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id','player_name']



@admin.register(TeamStats)
class TeamStatesAdmin(admin.ModelAdmin):
    list_display = ['id','team','matches_played']

@admin.register(Referee)
class RefereeAdmin(admin.ModelAdmin):
    list_display = ['id','referee_name','total_officiated']

# @admin.register(Match)
# class MatchAdmin(admin.ModelAdmin):
#     list_display = ['id','left_team','right_team']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id','news_title','news_content']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id','team_name']

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['id','league_name']

@admin.register(TeamPurchase)
class TeampurAdmin(admin.ModelAdmin):
    list_display = ['id','teamname']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','buyer']


    
class EventInline(admin.TabularInline):
    model = Event
    extra = 1

class FootballMatchAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    list_display = ['left_team' ,'left_score','right_score', 'right_team','live','create_at']


admin.site.register(Match, FootballMatchAdmin)
