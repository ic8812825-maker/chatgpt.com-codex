def test_z_score_cases():
    cases=[(1.1050,1.1000,0.0020,2.5),(1.0950,1.1000,0.0020,-2.5),(1.1000,1.1000,0.0020,0)]
    for p,e,a,x in cases: assert round((p-e)/a,6)==x
