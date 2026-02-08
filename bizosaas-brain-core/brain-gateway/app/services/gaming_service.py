from sqlalchemy.orm import Session
from app.models.gaming import Tournament, Match, PlayerGamingStats
from app.models.user import User
import math
import random
from typing import List, Optional
import uuid

class GamingService:
    def __init__(self, db: Session):
        self.db = db

    def generate_single_elimination_bracket(self, tournament_id: uuid.UUID):
        tournament = self.db.query(Tournament).filter(Tournament.id == tournament_id).first()
        if not tournament:
            return None
        
        # 1. Get participants (for now, assume they are registered in a many-to-many or JSON settings)
        # In a real app, you'd have a tournament_participants table. 
        # For this boilerplate, let's assume we fetch them from tournament.settings['participants']
        participant_ids = tournament.settings.get('participant_ids', [])
        if not participant_ids:
            return []

        # 2. Add Byes to reach power of 2
        num_participants = len(participant_ids)
        next_pow2 = 1 << (num_participants - 1).bit_length()
        num_byes = next_pow2 - num_participants
        
        # Pad with None for byes
        bracket_slots = participant_ids + [None] * num_byes
        random.shuffle(bracket_slots) # Random seeding for now

        # 3. Create Round 1 Matches
        matches = []
        for i in range(0, next_pow2, 2):
            p1 = bracket_slots[i]
            p2 = bracket_slots[i+1]
            
            match = Match(
                tournament_id=tournament_id,
                round=1,
                position=i // 2,
                player1_id=p1,
                player2_id=p2,
                status="scheduled" if p1 and p2 else "completed" # Automatic win if bye
            )
            
            # Handle Bye Auto-win
            if p1 and not p2:
                match.winner_id = p1
                match.score1 = 1
                match.score2 = 0
            elif p2 and not p1:
                match.winner_id = p2
                match.score1 = 0
                match.score2 = 1
            
            self.db.add(match)
            matches.append(match)
        
        self.db.commit()
        return matches

    def update_mmr(self, user_id: uuid.UUID, game_id: uuid.UUID, tenant_id: uuid.UUID, actual_score: float, opponent_mmr: float):
        stats = self.db.query(PlayerGamingStats).filter(
            PlayerGamingStats.user_id == user_id,
            PlayerGamingStats.game_id == game_id,
            PlayerGamingStats.tenant_id == tenant_id
        ).first()

        if not stats:
            stats = PlayerGamingStats(
                user_id=user_id,
                game_id=game_id,
                tenant_id=tenant_id,
                mmr=1000.0
            )
            self.db.add(stats)

        # Elo Logic
        K = 32
        expected_score = 1 / (1 + math.pow(10, (opponent_mmr - stats.mmr) / 400))
        stats.mmr = stats.mmr + K * (actual_score - expected_score)
        
        if actual_score == 1.0:
            stats.wins += 1
        elif actual_score == 0.0:
            stats.losses += 1
        else:
            stats.draws += 1
            
        stats.total_matches += 1
        self.db.commit()
        return stats
