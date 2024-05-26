import toml
import argparse
# comandline program
import glob


def parse_args():
    parser = argparse.ArgumentParser(
        description="Control teleporter and write to TOML file")
    parser.add_argument("--x", type=float)
    parser.add_argument("--y", type=float)
    parser.add_argument("--z", type=float)
    return parser.parse_args()


args = parse_args()

for file in glob.glob("/ship/*/log"):
    data = toml.load(file)
    if data["type"] == "teleporter":
        id = data["next_job_id"]
        x = args.x
        y = args.y
        z = args.z

        folder = file[: file.rfind("/")]
        config_file = f"{folder}/config"
        config = {
            "location": [x, y, z],
            "next_job_id": id,
        }

        toml.dump(config, open(config_file, "w"))
        break
