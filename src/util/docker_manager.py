import docker
import glob
import yaml
import os as hostos
import io
import shutil
import random
import tarfile
from io import BytesIO
#with open("resources/settings.yaml", "r") as f:
#    settings = yaml.safe_load(f)["settings"]
    
client = docker.from_env()
oss = []
    
class Operating_System:
    def __init__(self, path):
        print("Loading OS from {}".format(path))
        self.path = path
        self.load_metadata()
        while True:
            self.id = random.randint(0, 100000)
            if not self.id in [os.id for os in oss]:
                break
    def load_metadata(self):
        with open(self.path+"/config.yaml", "r") as f:
            metadata = yaml.safe_load(f)["metadata"]
        self.name = metadata["name"]

    def has_image(self):
        return len(client.images.list(filters={"reference": "spaceos:{}".format(self.name)})) > 0

    def build_image(self, force=False):
        if not force and self.has_image(): 
            return
        name = "spaceos:{}".format(self.name)
        print("Building image {}".format(name))
        #create temp os folder 
        tempos = "resources/temp/os"
        shutil.copytree(self.path, tempos, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        modify_dockerfile(tempos+"/Dockerfile")
        image = client.images.build(path=tempos, tag=name)
        #image = client.images.build(fileobj=self.dockerfile, custom_context=True ,tag=name)

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

def modify_dockerfile(dockerfile):
    with open("resources/dockerfile_attachment", "r") as f:
        additional_content = f.readlines()
    additional_content[-1] = additional_content[-1]+"\n"
    with open(dockerfile, "r") as f:
        rawlines = f.readlines()
    rawlines[-1] = rawlines[-1]+"\n"
    lines = []
    for line in rawlines:                    
        lines.append(line)
        if line.upper().startswith("FROM"):
            lines += additional_content
    with open(dockerfile, "w") as f:
        f.writelines(lines)
    

def is_container_running(container):
    if not container:
        return False
    container.reload()
    return container.status == "running"

def attach_console(container):
    if not container:
        return False
    #check os
    if hostos.name == "nt":
        attach_console_windows(container)
    elif hostos.name == "posix":
        attach_console_linux(container)
    else:
        print("OS "+ hostos.name+" not supported")
        return False

def attach_console_windows(container):
    windows_command = "start cmd /k"
    # open cmd and attach to container
    command = "docker exec -it {container} /bin/bash".format(
        container=container.name)
    hostos.system(windows_command+" " + command)

def attach_console_linux(container):
    linux_command = "gnome-terminal -- sh -c"
    # open cmd and attach to container
    
    command = "docker exec -it {container} /bin/bash".format(
        container=container.name)
    hostos.system(linux_command+' "' + command+'"')

def reload_oss():
    for folder in glob.glob("resources/operating_systems/*"):
        con = False
        for os in oss:
            if os.path == folder:
                con = True
                continue
        if con:
            continue
        oss.append(Operating_System(folder))


def get_os_folder(folder):
    for os in oss:
        if os.path == folder:
            return os
    os = Operating_System(folder)
    oss.append(os)
    return oss[-1]

get_os_path = get_os_folder


def get_os_name(name):
    for os in oss:
        if os.name == name:
            return os
    return None

def get_os_id(id):
    for os in oss:
        if int(os.id) == (id):
            return os
    return None

def read_from_container(container,dir, filename):
    if not container:
        return None
    if not is_container_running(container):
        return None
    archive_data,_ = container.get_archive(dir+filename)
    archive_bytes = b"".join(archive_data)
    with tarfile.open(fileobj=BytesIO(archive_bytes), mode='r') as tar:
        # Assuming there is only one file in the archive
        file_info = tar.getmembers()[0]
        file_content = tar.extractfile(file_info).read()
        file_content = file_content.decode("utf-8")
        return file_content
        
def write_to_container(container, content: str, dir: str, filename: str):
    if not container:
        return None
    if not is_container_running(container):
        return None
    """ content should be a string """
    stream = io.BytesIO(content.encode())

    # Creating a tar archive with a single file containing the provided content
    with tarfile.open(fileobj=stream, mode='w|') as tar:
        # Creating a TarInfo object for the file
        info = tarfile.TarInfo(name=filename)
        info.size = len(content)
        
        # Adding the file to the archive
        tar.addfile(info, io.BytesIO(content.encode()))

    # Putting the archive into the container with the complete destination path
    container.put_archive(dir, stream.getvalue())

reload_oss()

if __name__ == "__main__":
    print(oss)
    os = oss[0]
    print(os.has_image())
    os.get_image()
