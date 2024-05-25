from typing import Tuple
import json
import re

def pull_environment_and_check(env_name: str, stuff: str) -> bool:
    is_success = False
    filne_name = f"/app/internal/config/regex.json"
    with open(filne_name, 'r') as file:
        js_data = json.load(file)
    if not js_data.get(env_name, ''):
        pass
    else:
        is_success = True

    if is_success:
        pattern = js_data[env_name]
        if re.match(pattern, stuff) is not None:
            return True
        else:
            return False

def pull_environment(env_name: str,from_variable: str) -> Tuple[str,bool]:
    filne_name = f"/app/internal/config/environment.json"
    # try:
    with open(filne_name, 'r') as file:
        js_data = json.load(file)
    if not js_data.get(from_variable, {}).get(env_name, ''):
        return f"\'{env_name}\' not found with {from_variable} key in the {filne_name} file",False
    else:
        return js_data[from_variable][env_name],True
    # except Exception as e:
    #     return f"{e}",False
