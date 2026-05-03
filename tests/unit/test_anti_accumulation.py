def anti(p): return 'normal' if p>0 else 'block'
def test_anti():
    assert anti(10)=='normal' and anti(0)=='block' and anti(-1)=='block'
