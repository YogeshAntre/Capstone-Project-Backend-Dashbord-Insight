import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from testapp.models import Match
from datetime import datetime  # Fixed import

class Command(BaseCommand):
    help = 'Load matches data from CSV into the database'

    def handle(self, *args, **kwargs):
        # Path to matches.csv inside testapp
        csv_path = os.path.join(settings.BASE_DIR, 'testapp', 'matches.csv')

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Convert date string to date object
                    match_date_str = row['Match Date'].strip()
                    match_date = datetime.strptime(match_date_str, "%b %d, %Y").date()

                    Match.objects.create(
                        team1=row['Team 1'].strip(),
                        team2=row['Team 2'].strip(),
                        winner=row['Winner'].strip(),
                        margin=row['Margin'].strip(),
                        ground=row['Ground'].strip(),
                        match_date=match_date,
                        match_id=row['MATCH_ID'].strip()
                    )
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error loading row: {row} -> {e}"))
        
        self.stdout.write(self.style.SUCCESS('Matches loaded successfully!'))

