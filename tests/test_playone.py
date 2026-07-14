import pygame
import unittest

from Data.Classes.Team import Team
from Data.playone import Game, ballState


class PlayOneTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Game(Team(teamName="Home"), Team(teamName="Away"))
        self.game.setup()

    def test_pitch_stays_in_pitching_state_on_first_frame(self):
        self.game.pitch()
        self.assertEqual(self.game.ballState, ballState.PITCHING)

    def test_swing_can_begin_a_hit_once_ball_is_in_range(self):
        self.game.ballRect.y = 1200
        self.game.ballState = ballState.PITCHING
        self.game.swing()
        self.assertEqual(self.game.ballState, ballState.BALLHIT)


if __name__ == "__main__":
    unittest.main()
