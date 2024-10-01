
from .models import Match, TeamStats
from django.utils import timezone

def calculate_team_stats():
    # Reset all team stats
    TeamStats.objects.update(matches_played=0, wins=0, draws=0, losses=0, goals_scored=0, goals_conceded=0, points=0)
    
    # Only consider matches that have ended
    matches = Match.objects.filter(create_at__lt=timezone.now())
    
    for match in matches:
        left_team_stats, _ = TeamStats.objects.get_or_create(team=match.left_team)
        right_team_stats, _ = TeamStats.objects.get_or_create(team=match.right_team)
        
        # Update matches played
        left_team_stats.matches_played += 1
        right_team_stats.matches_played += 1
        
        # Update goals scored and conceded
        left_team_stats.goals_scored += match.left_score
        left_team_stats.goals_conceded += match.right_score
        right_team_stats.goals_scored += match.right_score
        right_team_stats.goals_conceded += match.left_score
        
        # Update wins, draws, and losses
        if match.left_score > match.right_score:
            left_team_stats.wins += 1
            right_team_stats.losses += 1
            left_team_stats.points += 3
        elif match.left_score < match.right_score:
            right_team_stats.wins += 1
            left_team_stats.losses += 1
            right_team_stats.points += 3
        else:
            left_team_stats.draws += 1
            right_team_stats.draws += 1
            left_team_stats.points += 1
            right_team_stats.points += 1
        
        # Save updated stats
        left_team_stats.save()
        right_team_stats.save()