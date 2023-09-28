import configparser
import csv
import os
import time


def write_csv(path, row, header_features=[]):
    """ write result to csv file """
    if path is not None:
        if not os.path.exists("crunch/output"):
            os.makedirs("crunch/output")

        file_exists = os.path.isfile("crunch/output/" + path)
        with open("crunch/output/" + path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            if not file_exists:
                header = ['time', 'value']
                writer.writerow(header + header_features)
            writer.writerow([time.time()] + row)


def to_list(x):
    if isinstance(x, list):
        return x
    try:
        return list(x)
    except TypeError:
        return [x]


def config(section, key=None):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../setup.cfg')

    conf = configparser.ConfigParser()
    try:
        conf.read(config_path)
    except FileNotFoundError:
        raise FileNotFoundError("Couldn't find configuration file")

    if section not in conf:
        raise Exception(f"The section named {section} does not exist in the config file.")

    if key is None:
        return conf[section]

    if key not in conf[section]:
        raise Exception(f"The value {key} does not exist in section {section} in the config file.")

    return conf[section][key]
