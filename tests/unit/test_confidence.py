def c(z): return min(abs(z)/2,1)
def test_confidence():
    for z,v in [(0,0),(1,0.5),(1.5,0.75),(2,1),(3,1),(-2,1)]: assert c(z)==v
