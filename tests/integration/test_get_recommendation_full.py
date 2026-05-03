from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_get_recommendation_full():
    r=get_recommendation(**base_args())
    for k in ['state','regime','z','v','q','beta','ev','min_move_points','scenario_up','scenario_down']:
        assert k in r
