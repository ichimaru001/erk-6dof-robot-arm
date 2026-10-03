import sys
import json
from moveit_configs_utils import MoveItConfigsBuilder

try:
    configs = MoveItConfigsBuilder("erk_description", package_name="erk_description")
    configs.planning_pipelines(pipelines=["ompl"])
    
    with open('/home/ichim/erk_ws/erk_configs.json', 'w') as f:
        json.dump(configs.to_dict(), f, indent=2)
except Exception as e:
    with open('/home/ichim/erk_ws/erk_configs_error.txt', 'w') as f:
        f.write(str(e))
