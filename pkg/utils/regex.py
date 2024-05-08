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

  
       