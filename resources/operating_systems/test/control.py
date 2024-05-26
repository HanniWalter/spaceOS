import toml
import argparse
# comandline program
import glob


def parse_args():
    parser = argparse.ArgumentParser(
        description="Control thrusters and write to TOML file")
    parser.add_argument("-x", type=float)
    parser.add_argument("-y", type=float)
    parser.add_argument("-z", type=float)
    return parser.parse_args()


args = parse_args()

x = args.thruster0
y = args.thruster1
z = args.thruster2

for folder in glob.glob("/ship/*"):
    print(folder)
