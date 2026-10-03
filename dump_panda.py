import sys
import json
from moveit_configs_utils import MoveItConfigsBuilder

try:
    configs = MoveItConfigsBuilder("panda_moveit_config", package_name="panda_moveit_config").to_dict()
    with open('/home/ichim/erk_ws/panda_configs.json', 'w') as f:
        json.dump(configs, f, indent=2)
except Exception as e:
    with open('/home/ichim/erk_ws/panda_configs_error.txt', 'w') as f:
        f.write(str(e))
