"""Change k9s skin"""

import os
import subprocess
import yaml


class K9sInfoException(Exception):
    """Exception for K9s Information errors

    Args:
        Exception (String): Exception message
    """


class K9sSkinNotFoundException(Exception):
    """Exception for K9s Skin Not Found errors

    Args:
        Exception (String): Exception message
    """


class K9sInvalidConfigException(Exception):
    """Exception for K9s Invalid Config errors

    Args:
        Exception (String): Exception message
    """


def get_all_skins(config_path):
    """Get all available skins from k9s installation path

    Args:
        config_path (String): path of the k9s config file

    Returns:
        Array of Strings: List of all available skins
    """
    skin_dir = os.path.join(config_path, "skins")
    skins = []
    for file in os.listdir(skin_dir):
        if file.endswith(".yaml"):
            skins.append(os.path.splitext(file)[0])
    return skins


def get_config_path():
    """Get the path of the k9s config file

    Raises:
        K9sInfoException: Error if k9s config file not found

    Returns:
        String: K9s config file path
    """
    k9s_config_path_cmd = "k9s info | grep config.yaml"
    result = subprocess.run(k9s_config_path_cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, check=True)

    output = result.stdout
    error = result.stderr

    if error:
        raise K9sInfoException(f"k9s config error: {error}")

    config_file_path = output[output.find("/"):].replace('/n', '')
    return os.path.dirname(config_file_path)


def change_skin(config_path, skin_name):
    """Change skin in the k9s config file

    Args:
        config_path (String): K9s config file path
        skin_name (String): K9s skin name

    Raises:
        K9sSkinNotFoundException: K9s Skin Not Found error
        K9sInvalidConfigException: K9s Invalid Config error
    """
    skin_file_path = os.path.join(config_path, "skins", f"{skin_name}.yaml")
    if not os.path.isfile(skin_file_path):
        raise K9sSkinNotFoundException(f"Skin '{skin_name}' does not exist.")

    config_file_path = os.path.join(config_path, "config.yaml")

    with open(config_file_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if 'k9s' in data and 'ui' in data['k9s'] and 'skin' in data['k9s']['ui']:
        data['k9s']['ui']['skin'] = skin_name
    else:
        raise K9sInvalidConfigException(
            "The key 'k9s:ui:skin' was not found in the k9s config file.")

    with open(config_file_path, 'w', encoding="utf-8") as file:
        yaml.dump(data, file, default_flow_style=False)


if __name__ == '__main__':
    try:
        _config_path = get_config_path()

        print("Available skins:")
        _skins = get_all_skins(_config_path)
        for i, skin in enumerate(_skins, start=1):
            print(f"{i}. {skin}")

        _skin_number = int(
            input("Enter the number of the skin you want to change to: "))
        _skin_name = _skins[_skin_number - 1]

        change_skin(_config_path, _skin_name)

        print(f"Skin changed to '{_skin_name}'.")
    except (K9sInfoException, K9sSkinNotFoundException, K9sInvalidConfigException) as e:
        print(f"Error: {e}")
