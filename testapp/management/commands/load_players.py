import csv
import os
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from testapp.models import Player

class Command(BaseCommand):
    help = 'Load players data from CSV into the database'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'testapp', 'players.csv')

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    name = row["Player"].strip()
                    image_url = row.get("Image URL", "").strip()
                    dob_raw = row.get("Date of birth (age)", "").strip()
                    role = row.get("Role", "").strip()
                    batting_style = row.get("Batting", "").strip()
                    bowling_style = row.get("Bowling style", "").strip()
                    od_matches = int(row.get("ODIs", 0) or 0)
                    domestic_team = row.get("List A or domestic team", "").strip()

                    # Extract and parse clean date from messy string like:
                    # "2000 -09 -22)22 September 2000 (aged 23)"
                    date_of_birth = None
                    match = re.search(r'\d{1,2} \w+ \d{4}', dob_raw)
                    if match:
                        dob_clean = match.group(0)
                        date_of_birth = datetime.strptime(dob_clean, "%d %B %Y").date()

                    Player.objects.get_or_create(
                        name=name,
                        defaults={
                            "image_url": image_url,
                            "date_of_birth": date_of_birth,
                            "role": role,
                            "batting_style": batting_style,
                            "bowling_style": bowling_style,
                            "od_matches": od_matches,
                            "domestic_team": domestic_team
                        }
                    )

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"❌ Error loading player {row.get('Player')}: {e}"))

        self.stdout.write(self.style.SUCCESS('✅ Players loaded successfully!'))
