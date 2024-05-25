import os
import toml

config = {}


def create_local_config_files():
    local_config_file = os.path.join(
        os.path.expanduser('~'), '.config', 'spaceOS', 'config.local')
    os.makedirs(os.path.dirname(local_config_file), exist_ok=True)
    # read_config
    global config
    if os.path.exists(local_config_file):
        config = toml.load(local_config_file)
    if 'console_command' not in config:
        config['console_command'] = console_command_creater()
    if 'docker_command' not in config:
        config['docker_command'] = "docker exec -it {container} /bin/bash"

    toml.dump(config, open(local_config_file, 'w'))


def console_command_creater():
    if os.name == 'nt':
        return 'start cmd /k'
    if os.name == 'posix':
        # check if gnome-terminal is installed
        if os.system('gnome-terminal') != 0:
            return 'konsole --hold -e'
        # check if gnome is installed
        if os.system('gnome-terminal') != 0:
            return 'gnome-terminal -- sh -c'
    print('OS is not supported change it manually in ~/.config/spaceOS/config.local')
    return 'echo "OS not supported"'


create_local_config_files()

print(config)
