import unittest
import numpy as np
from scripts.run8_selected50_scoreline_model import (
    scoreline_matrices, derive_markets, fit_dc_rho, dc_tau
)

class ScorelineTests(unittest.TestCase):
    def test_independent_joint_matrix_is_normalized_and_market_probs_valid(self):
        lh=np.array([1.2, 2.0]); la=np.array([0.8, 1.1])
        joint,mass=scoreline_matrices(lh,la,0.0)
        self.assertTrue(np.allclose(joint.sum(axis=(1,2)),1.0))
        markets=derive_markets(joint)
        for values in markets.values():
            self.assertTrue(np.all(values>=0))
            self.assertTrue(np.all(values<=1))
        self.assertTrue(np.allclose(markets["home_win"]+markets["draw"]+markets["away_win"],1.0))
        self.assertTrue(np.all(mass<=1.0+1e-9))

    def test_dixon_coles_correction_preserves_valid_distribution(self):
        lh=np.array([1.4,0.9]); la=np.array([0.8,1.2])
        joint,mass=scoreline_matrices(lh,la,-0.08)
        self.assertTrue(np.allclose(joint.sum(axis=(1,2)),1.0))
        self.assertTrue(np.all(joint>=0))
        self.assertTrue(np.all(mass>0))

    def test_low_score_tau_matches_standard_parameterisation(self):
        lh=np.array([1.5]); la=np.array([0.7])
        tau=dc_tau(np.array([0]),np.array([0]),lh,la,0.1)
        self.assertAlmostEqual(float(tau[0]),1-1.5*0.7*0.1)

if __name__ == "__main__":
    unittest.main()
