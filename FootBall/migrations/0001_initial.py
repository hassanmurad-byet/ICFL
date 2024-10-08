# Generated by Django 5.0.3 on 2024-07-06 14:13

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "serial_number",
                    models.PositiveIntegerField(blank=True, null=True, unique=True),
                ),
                (
                    "left_score",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Left Team Score"
                    ),
                ),
                (
                    "right_score",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Right Team Score"
                    ),
                ),
                (
                    "left_formation",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        verbose_name="Left Team Formation 4-3-3-1",
                    ),
                ),
                (
                    "right_formation",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        verbose_name="Right Team Formation 4-4-2-1",
                    ),
                ),
                ("create_at", models.DateTimeField(verbose_name="Match Time")),
                (
                    "match_details",
                    models.TextField(blank=True, verbose_name="Match Details"),
                ),
                (
                    "location",
                    models.CharField(max_length=100, verbose_name="Match Location"),
                ),
                (
                    "img",
                    models.ImageField(blank=True, null=True, upload_to="match_images"),
                ),
                (
                    "highlights",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="videos",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
                            )
                        ],
                    ),
                ),
                ("live", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "player_name",
                    models.CharField(max_length=50, verbose_name="player name"),
                ),
                ("image", models.ImageField(upload_to="player_images")),
                (
                    "serial_number",
                    models.PositiveIntegerField(blank=True, null=True, unique=True),
                ),
                (
                    "player_uid",
                    models.CharField(max_length=10, verbose_name="Player ID"),
                ),
                (
                    "batch",
                    models.CharField(
                        choices=[
                            ("201", "201"),
                            ("202", "202"),
                            ("203", "203"),
                            ("211", "211"),
                            ("212", "212"),
                            ("213", "213"),
                            ("221", "221"),
                            ("222", "222"),
                            ("223", "223"),
                            ("231", "231"),
                            ("232", "232"),
                            ("233", "233"),
                            ("241", "241"),
                            ("242", "242"),
                        ],
                        max_length=20,
                        verbose_name="Select Batch ",
                    ),
                ),
                (
                    "player_jersey_no",
                    models.SmallIntegerField(
                        default=0, verbose_name="Player Jersey No"
                    ),
                ),
                ("phone", models.CharField(max_length=20, verbose_name="Player Phone")),
                (
                    "email",
                    models.EmailField(max_length=50, verbose_name="Player Email"),
                ),
                (
                    "blood_group",
                    models.CharField(
                        choices=[
                            ("O+", "O+"),
                            ("O-", "O-"),
                            ("A+", "A+"),
                            ("A-", "A-"),
                            ("B+", "B+"),
                            ("AB+", "AB+"),
                            ("AB-", "AB-"),
                        ],
                        max_length=20,
                        verbose_name="Blood Group",
                    ),
                ),
                ("age", models.CharField(max_length=10, verbose_name="Player Age")),
                (
                    "height",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Player Height (cm)"
                    ),
                ),
                (
                    "weight",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Player Weight (kg)"
                    ),
                ),
                (
                    "footed",
                    models.CharField(
                        max_length=50, verbose_name="Footed (Left or Right)"
                    ),
                ),
                (
                    "play_position",
                    models.CharField(
                        choices=[
                            ("GK", "Goalkeeper"),
                            ("SW", "Sweeper"),
                            ("CB", "Centre Back"),
                            ("FB", "Full Back"),
                            ("WB", "Wing Back"),
                            ("DM", "Defensive Midfielder"),
                            ("CM", "Centre Midfielder"),
                            ("WM", "Wing Midfielder"),
                            ("AM", "Attacking Midfielder"),
                            ("WF", "Wing Forward"),
                            ("CF", "Centre Forward"),
                        ],
                        max_length=50,
                        verbose_name="Position Play",
                    ),
                ),
                (
                    "total_goals",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="Total Goals"
                    ),
                ),
                (
                    "Total_assist",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Total Goals Assists"
                    ),
                ),
                (
                    "total_matches",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="Total Matches"
                    ),
                ),
                (
                    "yellow_cards",
                    models.PositiveIntegerField(default=0, verbose_name="Yellow Cards"),
                ),
                (
                    "red_cards",
                    models.PositiveIntegerField(default=0, verbose_name="Red Cards"),
                ),
                (
                    "totalplayer_of_match",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Total Player of the Match"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Referee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "referee_name",
                    models.CharField(max_length=50, verbose_name="Referee Name"),
                ),
                (
                    "serial_number",
                    models.PositiveIntegerField(blank=True, null=True, unique=True),
                ),
                ("referee_img", models.ImageField(upload_to="referee_images")),
                ("phone", models.CharField(max_length=20, verbose_name="Phone Number")),
                ("email", models.EmailField(max_length=50, verbose_name="Email")),
                ("info", models.TextField()),
                (
                    "total_officiated",
                    models.PositiveIntegerField(
                        verbose_name="Total Matches Officiated"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("goal", "goal"),
                            ("corner", "corner"),
                            ("foul", "foul"),
                            ("penalty", "penalty"),
                            ("offside", "offside"),
                            ("red", "red card"),
                            ("yellow", "yellow card"),
                        ],
                        default="None",
                        max_length=40,
                    ),
                ),
                (
                    "event_time",
                    models.PositiveIntegerField(
                        default="None", help_text="Time in minutes"
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "matche",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="FootBall.match",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "news_title",
                    models.CharField(default="", max_length=50, verbose_name="Title"),
                ),
                ("news_content", models.TextField(verbose_name="Content")),
                (
                    "news_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="news_images",
                        verbose_name="Image",
                    ),
                ),
                (
                    "news_video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="news_videos",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
                            )
                        ],
                    ),
                ),
                ("publish_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="news_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-publish_date",),
            },
        ),
        migrations.AddField(
            model_name="match",
            name="Total_assist_left_team",
            field=models.ManyToManyField(
                blank=True, related_name="left_team_Total_assist", to="FootBall.player"
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="Total_assist_right_team",
            field=models.ManyToManyField(
                blank=True, related_name="right_team_Total_assist", to="FootBall.player"
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="player_of_match",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="player_of_match",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="red_card_players_left_team",
            field=models.ManyToManyField(
                blank=True,
                related_name="left_team_red_card_matches",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="red_card_players_right_team",
            field=models.ManyToManyField(
                blank=True,
                related_name="right_team_red_card_matches",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="scoring_players_left_team",
            field=models.ManyToManyField(
                blank=True,
                related_name="left_team_scoring_matches",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="scoring_players_right_team",
            field=models.ManyToManyField(
                blank=True,
                related_name="right_team_scoring_matches",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="yellow_card_players_left_team",
            field=models.ManyToManyField(
                blank=True,
                related_name="left_team_yellow_card_matches",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="yellow_card_players_right_team",
            field=models.ManyToManyField(
                blank=True,
                related_name="right_team_yellow_card_matches",
                to="FootBall.player",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="referee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="FootBall.referee",
            ),
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "team_name",
                    models.CharField(max_length=30, verbose_name="team name"),
                ),
                (
                    "team_logo",
                    models.ImageField(upload_to="team_logo", verbose_name="Team Logo"),
                ),
                (
                    "coach_name",
                    models.CharField(max_length=20, verbose_name="Coach Name"),
                ),
                (
                    "batch_name",
                    models.CharField(
                        choices=[
                            ("201", "201"),
                            ("202", "202"),
                            ("203", "203"),
                            ("211", "211"),
                            ("212", "212"),
                            ("213", "213"),
                            ("221", "221"),
                            ("222", "222"),
                            ("223", "223"),
                            ("231", "231"),
                            ("232", "232"),
                            ("233", "233"),
                            ("241", "241"),
                            ("242", "242"),
                        ],
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(max_length=20, verbose_name="Phone Number")),
                ("email", models.EmailField(max_length=50, verbose_name="Team Email")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Panding", "Panding"),
                            ("Accepted", "Accepted"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Panding",
                        max_length=255,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_name",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="player",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plyers",
                to="FootBall.team",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="left_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="left_matches",
                to="FootBall.team",
            ),
        ),
        migrations.AddField(
            model_name="match",
            name="right_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="right_matches",
                to="FootBall.team",
            ),
        ),
        migrations.CreateModel(
            name="League",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("league_name", models.CharField(max_length=200, verbose_name="Name")),
                (
                    "info",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Informations"
                    ),
                ),
                ("times", models.DateTimeField(blank=True)),
                (
                    "teams",
                    models.ManyToManyField(
                        blank=True, related_name="league_teams", to="FootBall.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamStats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "serial_number",
                    models.PositiveIntegerField(blank=True, null=True, unique=True),
                ),
                ("matches_played", models.PositiveIntegerField(default=0)),
                ("wins", models.PositiveIntegerField(default=0)),
                ("draws", models.PositiveIntegerField(default=0)),
                ("losses", models.PositiveIntegerField(default=0)),
                ("goals_scored", models.PositiveIntegerField(default=0)),
                ("goals_conceded", models.PositiveIntegerField(default=0)),
                ("points", models.PositiveIntegerField(default=0)),
                (
                    "team",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stats",
                        to="FootBall.team",
                    ),
                ),
            ],
        ),
    ]
