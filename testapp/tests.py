# from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Match, Player, Batting, Bowling
# Create your tests here.
import json
class MatchTestCase(APITestCase):
    def tearDown(self):
        pass
    def setUp(self):
        self.match=Match.objects.create(
            
            match_id="M001",
            team1="Team A",
            team2="Team B",
            winner="Team A",
            margin="10 runs",
            ground="Stadium X",
            match_date="2023-10-01"
        )
    def test_01_match_get_one(self):
      
        rep=self.client.get('http://127.0.0.1:8000/api/matches/1/')
        self.assertEqual(rep.status_code,200)
        data=json.loads(rep.content)
        self.assertEqual(data['match_id'],'M001')

        rep=self.client.get('http://127.0.0.1:8000/api/matches/88/')


        self.assertEqual(rep.status_code,404)


    def test_delete(self):
        response = self.client.delete('http://127.0.0.1:8000/api/matches/2/')
        print('delete',response)
        self.assertEqual(response.status_code, 204)
        #Verify the able to get deleted systemsettings throws 404
        response = self.client.get('http://127.0.0.1:8000/api/matches/2/')
        self.assertEqual(response.status_code, 404)

class MatchTestCasePost(APITestCase):
    def test_02_post_data(self):
        url='http://127.0.0.1:8000/api/matches/'
        userObj={
            'match_id':"M002",
            'team1':"Team A",
           'team2':"Team B",
            'winner':"Team B",
            'margin':"12 runs",
           'ground':"Stadium rX",
           'match_date':"2023-12-01"
        }
        rep=self.client.post(url,userObj,format='json')
        self.assertEqual(rep.status_code,201)
        userData = rep.json()
        print('UserData',userData)

        rep=self.client.get('http://127.0.0.1:8000/api/matches/')
        match=rep.json()
        print('Matches',match)
        self.assertEqual(len(match['results']),1)
        self.assertEqual(match['results'][0],userData)

from rest_framework.test import APITestCase
from .models import Player, Batting

class BattingTestCase(APITestCase):

    def setUp(self):
        # Create a player first (relationship base)
        self.player = Player.objects.create(
            name="Virat Kohli",
            team="India"
        )

    def test_create_batting_record(self):
        url = 'http://127.0.0.1:8000//api/batting/'
        batting_data = {
            "player": self.player.id,   # 🔑 send FK id
            "runs": 82,
            "balls": 53
        }

        response = self.client.post(url, batting_data, format='json')
        self.assertEqual(response.status_code, 201)

        created_batting = response.json()
        print("Created Batting:", created_batting)

        # Verify relationship stored correctly
        self.assertEqual(created_batting['player'], self.player.id)
        self.assertEqual(created_batting['runs'], 82)

    def test_get_batting_with_relationship(self):
        # Create batting linked to the player
        batting = Batting.objects.create(player=self.player, runs=50, balls=30)

        # Get batting detail
        response = self.client.get(f'http://127.0.0.1:8000//api/batting/{batting.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Validate relationship
        self.assertEqual(data['player'], self.player.id)
        self.assertEqual(data['runs'], 50)


