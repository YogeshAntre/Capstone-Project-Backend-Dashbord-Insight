import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from testapp.models import Match,Player,Bowling
from datetime import datetime  

class Command(BaseCommand):
    help = 'Load bowling data from CSV into the database'

    def handle(self, *args, **kwargs):
        # Path to bowling.csv (keep your file inside testapp folder)
        csv_path = os.path.join(settings.BASE_DIR, 'testapp', 'BOWLING.csv')

        with open(csv_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Match by MATCH_ID from CSV
                    match = Match.objects.get(match_id=row["MATCH_ID"])

                    # Player from BOWLING column in CSV
                    
                    player, _ = Player.objects.get_or_create(name=row["BOWLING"])

                    # Create Bowling record
                    Bowling.objects.create(
                        match=match,
                        player=player,
                        overs=float(row["OVERS"] or 0),
                        maidens=int(row["MAIDEN"] or 0),
                        runs_conceded=int(row["RUNS"] or 0),
                        wickets=int(row["WICKETS"] or 0),
                        economy=float(row["ECONOMY"] or 0),
                        dot_balls=int(row["ZEROES"] or 0),
                        fours=int(row["FOURS"] or 0),
                        sixes=int(row["SIXES"] or 0),
                        wides=int(row["WIDE BALLS"] or 0),
                        no_balls=int(row["NO BALLS"] or 0),
                        bowling_position=int(row["BOWLING_POSITION"] or 0),
                        bowling_team=row["BOWLING_TEAM"]
                    )
                except Match.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Match {row['MATCH_ID']} not found"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {row}: {e}"))