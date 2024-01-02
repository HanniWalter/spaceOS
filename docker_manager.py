import docker
import glob
import yaml
import os as hostos


client = docker.from_env()
oss = []


class Operating_System:
    def __init__(self, path):
        self.path = path
        self.load_metadata()

    def load_metadata(self):
        with open(self.path+"/config.yaml", "r") as f:
            metadata = yaml.safe_load(f)["metadata"]
        self.name = metadata["name"]

    def has_image(self):
        return len(client.images.list(filters={"reference": "spaceos:{}".format(self.name)})) > 0

    def build_image(self):
        if self.has_image():
            return
        name = "spaceos:{}".format(self.name)
        print("Building image {}".format(name))
        image = client.images.build(path=self.path, tag=name)

    def get_image(self):
        if not self.has_image():
            self.build_image()
        return client.images.get("spaceos:{}".format(self.name))

    def run(self):
        image = self.get_image()
        container = client.containers.run(
            image, detach=True, tty=True, hostname=self.name)
        self.container = container
        return container


def is_container_running(container):
    if not container:
        return False
    container.reload()
    return container.status == "running"


def force_rebuild():
    return

# def start()


def attach_console(container):
    if not container:
        return False
    # open cmd and attach to container
    command = "docker exec -it {container} /bin/bash".format(
        container=container.name)
    hostos.system("start cmd /k " + command)


def reload_oss():
    for folder in glob.glob("resources/operating_systems/*"):
        for os in oss:
            if os.path == folder:
                continue
        oss.append(Operating_System(folder))


def get_os_folder(folder):
    for os in oss:
        if os.path == folder:
            return os
    os = Operating_System(folder)
    oss.append(os)
    return oss[-1]


def get_os_name(name):
    for os in oss:
        if os.name == name:
            return os
    return None


reload_oss()

if __name__ == "__main__":
    print(oss)
    os = oss[0]
    print(os.has_image())
    os.get_image()
