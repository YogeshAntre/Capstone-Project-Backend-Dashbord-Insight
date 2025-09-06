import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from testapp.models import Match, Player, Batting

class Command(BaseCommand):
    help = 'Load batting data from CSV into the database safely'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'testapp', 'BATTING.csv')

        # Use latin-1 encoding to handle non-breaking spaces
        with open(csv_path, newline='', encoding="latin-1") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Skip empty batting rows
                if not row.get("BATTING"):
                    continue

                try:
                    # Get the match
                    match = Match.objects.get(match_id=row["MATCH_ID"])

                    # Get or create player
                    player, _ = Player.objects.get_or_create(name=row["BATTING"])

                    # Prevent duplicate batting entries for same player & match
                    batting_obj, created = Batting.objects.get_or_create(
                        match=match,
                        player=player,
                        defaults={
                            'runs': int(row["RUNS"] or 0),
                            'balls': int(row["BALLS"] or 0),
                            'minutes': int(row["MINUTES"]) if row["MINUTES"] else None,
                            'dismissal': row["DISMISSAL"] or None,
                            'fours': int(row["FOURS"] or 0),
                            'sixes': int(row["SIXES"] or 0),
                            'strike_rate': float(row["STRICK RATE"]) if row["STRICK RATE"] else None,
                            'batting_position': int(row["BATTING_POSITION"]) if row["BATTING_POSITION"] else None,
                            'batting_team': row["BATTING_TEAM"]
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Added {player.name} - {match}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Skipped duplicate: {player.name} - {match}"))

                except Match.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Match {row['MATCH_ID']} not found"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {row}: {e}"))
