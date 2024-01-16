import toml
import argparse
#comandline program

def parse_args():
    parser = argparse.ArgumentParser(description="Control thrusters and write to TOML file")
    parser.add_argument("--thruster0", type=float, help="Value for thruster0")
    parser.add_argument("--thruster1", type=float, help="Value for thruster1")
    parser.add_argument("--thruster2", type=float, help="Value for thruster2")
    return parser.parse_args()

args = parse_args()

thruster0 = args.thruster0
thruster1 = args.thruster1
thruster2 = args.thruster2

control = {"thruster0": thruster0 , "thruster1": thruster1 , "thruster2": thruster2}

#write control
with open("/ship/control", "w") as f:
    f.write(toml.dumps(control))

