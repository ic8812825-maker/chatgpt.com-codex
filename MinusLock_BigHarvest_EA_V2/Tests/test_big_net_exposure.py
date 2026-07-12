A=1.60; B=0.25; C=0.60
gross=A+B-C
assert abs(gross-1.25)<1e-9
assert gross > 1.0
assert abs((gross-1.0)-0.25)<1e-9
print("PASS big net exposure")
