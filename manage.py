#!/usr/bin/env python
import os
import sys
import json
import requests

OK_CODES = (200,201,202,203,204,205,206)
AVAILABLE_ENVS = ("dev","release","prod")

def load_fixtures(env:int=8003):

    env_ports = {"dev":8003,
                "release": 8004,
                "prod":8005}

    fixtures_file = "fixtures.json"

    if not os.path.isfile(fixtures_file):
        raise Exception(f"File {fixtures_file} not exist")

    with open(fixtures_file, "r") as read_file:
        data = json.load(read_file)

    fixtures_types = data.keys()

    for fixture_type in fixtures_types:
        url = f"http://31.131.28.206:{env_ports[env]}/{fixture_type}/"
        for value in data[fixture_type]:
            try:
                res = requests.post(url, data=value)
                status = res.status_code
                if status in OK_CODES:
                    print(f"New value was created in {fixture_type}") 
                else:
                    raise Exception(f"Request was failed with status code: {status}")
            except Exception as e:
                raise Exception(f"Request was failed: {e}")


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    cmd_args = sys.argv

    if cmd_args[1] == "apply_fixtures":
        try:
            env_type = cmd_args[2]
            if env_type in AVAILABLE_ENVS:
                load_fixtures(env=env_type)

            else:
                raise Exception(f"Wrong type of environment - {env_type}")
        except Exception:
            raise Exception("Lost cmd_arg #3 - environment type")
        return True

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(cmd_args)


if __name__ == '__main__':
    main()
