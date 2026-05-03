def q(z): return min(max(0.01+0.01*min(abs(z)/2,1),0.01),0.02)
def test_q():
    for z,v in [(0,0.01),(1,0.015),(1.5,0.0175),(2,0.02),(3,0.02)]: assert round(q(z),4)==v
