import toml
#comandline program

control = {"thruster0": 5 , "thruster1": 1 , "thruster2": 1}

#write control
with open("/ship/control", "w") as f:
    f.write(toml.dumps(control))

