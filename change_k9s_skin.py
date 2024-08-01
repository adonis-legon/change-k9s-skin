import os
import sys
import yaml
import subprocess


def get_all_skins(config_path):
    skin_dir = os.path.join(config_path, "skins")
    skins = []
    for file in os.listdir(skin_dir):
        if file.endswith(".yaml"):
            skins.append(os.path.splitext(file)[0])
    return skins


def get_config_path():
    k9s_config_path_cmd = "k9s info | grep config.yaml"
    result = subprocess.run(k9s_config_path_cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True)

    output = result.stdout
    error = result.stderr

    if error:
        raise Exception(f"k9s config error: {error}")

    # example output: "Config file: /Users/username/.k9s/config.yaml"
    config_file_path = output[output.find("/"):].replace('/n', '')
    return os.path.dirname(config_file_path)


def change_skin(config_path, skin_name):
    # check if the skin exists
    skin_file_path = os.path.join(config_path, "skins", f"{skin_name}.yaml")
    if not os.path.isfile(skin_file_path):
        raise Exception(f"Skin '{skin_name}' does not exist.")

    config_file_path = os.path.join(config_path, "config.yaml")

    with open(config_file_path, 'r') as file:
        data = yaml.safe_load(file)

    if 'k9s' in data and 'ui' in data['k9s'] and 'skin' in data['k9s']['ui']:
        data['k9s']['ui']['skin'] = skin_name
    else:
        raise Exception(
            "The key 'k9s:ui:skin' was not found in the k9s config file.")

    with open(config_file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


if __name__ == '__main__':
    try:
        print("Available skins:")
        skins = get_all_skins(get_config_path())
        for i, skin in enumerate(skins, start=1):
            print(f"{i}. {skin}")

        skin_number = int(
            input("Enter the number of the skin you want to change to: "))
        skin_name = skins[skin_number - 1]

        config_path = get_config_path()
        change_skin(config_path, skin_name)

        print(f"Skin changed to '{skin_name}'.")
    except Exception as e:
        print(f"Error: {e}")
