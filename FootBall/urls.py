
from django.urls import path
from FootBall import views

app_name = 'FootBall'

urlpatterns = [

    path("", views.Home, name="home"),
     
    #  for team buy 
    path('team-list/', views.team_list, name ="team_list"),
    path('teams/buy/<int:team_id>/', views.buy_team, name='buy_team'),

    # User dashboard 
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('purchased-team/', views.purchased_team_info_view, name='purchased_team_info'),
    path('invoice/<int:purchase_id>/', views.invoice_view, name='invoice_view'),
    path('update-team-user/<pk>/', views.UpdateTeam_user, name='update_team_user'),

    path('player-team/', views.player_team_info_view, name='player_team_info'),
    path('add-player-team/', views.add_player_team, name='add_player_team'),
    path('team-player-info/<int:player_id>/', views.team_playerinfo, name='team_player_info'),

    path('team-matche-info/', views.team_matche_info, name='team_matche_info'),

    path('team-report-user/', views.teamreport_user, name='team_report_user'),
    path('team-report-info-user/<int:team_id>/', views.team_report_info_view_user, name='team_report_info_user'),




    
    #  admin dashbord CRUD for team
    path('admin-dashboard/', views.admin_dashboard, name='admin_dash'),
    path('admin-team-list/', views.adminteam, name='admin_team'),
    path('add-team/', views.add_team, name='add_team'),
    path('update-team/<pk>/', views.UpdateTeam, name='update_team'),
    path('delete-team/<int:del_id>/', views.DeleteTeam, name='delete_team'),


    #  admin dashbord CRUD for player
    path('player-list/', views.Player_list.as_view(), name='player_list'),
    path('player-info/<int:player_id>/', views.playerinfo, name='player_info'),
    path('add-player/', views.add_player, name='add_player'),
    path('update-player/<pk>/', views.UpdatePlayer, name='update_player'),
    path('delete-player/<int:del_id>/', views.Deleteplayer, name='delete_player'),

    #  admin dashbord CRUD for Matches
    path('matches-list/', views.matchelist, name='matches_list'),
    path('create-matche/', views.create_match, name='create_matche'),
    path('update-matche/<pk>/', views.update_match.as_view(), name='update_matche'),


    #admin dashbord CURD for Refeere
    path('referee/',views.refeere, name='referee' ),
    path('add-refeere/', views.add_refeere, name='add_refeere'),
    path('update-refeere/<pk>/', views.UpdateReferee, name='update_refeere'),
    path('delete-refeere/<int:del_id>/', views.DeleteRefee, name='delete_refeere'),


    # admin dashboard CURD for News 
    path('news-list', views.newslist, name='news_list'),
    path('add-news/', views.add_News, name='add_news'),

    path('update-news/<pk>/', views.UpdateNews, name='update_news'),
    path('delete-news/<int:del_id>/', views.DeleteNews, name='delete_news'),


    # admin dashboard CURD for League
    path('league-list', views.leaguelist, name='league_list'),
    path('add-league/', views.add_league, name='add_league'),
    path('update-league/<pk>/', views.Updateleague, name='update_league'),
    path('delete-league/<int:del_id>/', views.Deleteleague, name='delete_league'),

    # admin dashboard CURD for team puchase  
    path('team-purchase/', views.teampurchase, name='team_purchase'),
    path('payment-details/', views.Paymentdetails, name='payment_details'),
    path('update-team-purchase/<pk>/', views.UpdateteamPur, name='update_team_purchase'),
    path('delete-team-purchase/<int:del_id>/', views.DeleteTeamPurchase, name='delete_team_purchase'),


    # admin dashboard CURD for team report 
    path('team-report/', views.teamreport, name='team_report'),
    path('team-report-info/<int:team_id>/', views.team_report_info_view, name='team_report_info'),



     # admin dashboard CURD for matche report 
    path('matche-report/', views.Matchereport, name='matche_report'),










   










   



    path('players/', views.players, name="players"),
    path('blogs/', views.blogs, name="blogs"),
    path('contact/', views.contact, name="contact"),
    path('single-players/', views.single_players, name="single_ply"),

    # for show live matches and information 
    path('live-matches/', views.livematch, name="live_matches"),
    path('match-info/<int:match_id>/<int:team1_id>/<int:team2_id>/',views.MatcheInfo,name='match_info'),
    path('match-info/<int:match_id>/<int:team1_id>/<int:team2_id>/', views.MatcheInfo, name='match_detail'),


   






]

