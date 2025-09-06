from rest_framework import serializers
from .models import Match, Player, Batting, Bowling

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class BattingSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    match_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Batting
        fields = '__all__'
        extra_fields = ['player_name', 'match_details']
    
    def get_match_details(self, obj):
        return {
            'match_id': obj.match.match_id,
            'team1': obj.match.team1,
            'team2': obj.match.team2,
            'date': obj.match.match_date
        }

class BowlingSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    match_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Bowling
        fields = '__all__'
        extra_fields = ['player_name', 'match_details']
    
    def get_match_details(self, obj):
        return {
            'match_id': obj.match.match_id,
            'team1': obj.match.team1,
            'team2': obj.match.team2,
            'date': obj.match.match_date
        }
