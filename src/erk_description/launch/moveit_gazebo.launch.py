import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def load_yaml(package_name, file_path):
    pkg_share = get_package_share_directory(package_name)
    absolute_path = os.path.join(pkg_share, file_path)
    if not os.path.exists(absolute_path):
        src_path = os.path.expanduser(f'~/erk_ws/src/{package_name}/{file_path}')
        if os.path.exists(src_path):
            absolute_path = src_path
    try:
        with open(absolute_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except Exception:
        return {}

def generate_launch_description():
    pkg_share = get_package_share_directory('erk_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'erk.xacro')
    srdf_file = os.path.join(pkg_share, 'config', 'erk.srdf')

    robot_description_raw = xacro.process_file(xacro_file).toxml()
    
    with open(srdf_file, 'r') as f:
        srdf_raw = f.read()

    robot_description = {'robot_description': robot_description_raw}
    robot_description_semantic = {'robot_description_semantic': srdf_raw}

    # Load Kinematics Dict
    kinematics_yaml = load_yaml('erk_description', 'config/kinematics.yaml')
    robot_description_kinematics = {'robot_description_kinematics': kinematics_yaml}

    # Load Joint Limits Dict
    joint_limits_yaml = load_yaml('erk_description', 'config/joint_limits.yaml')
    robot_description_planning = {'robot_description_planning': joint_limits_yaml}

    # Load OMPL Planning Pipeline Dict
    ompl_yaml = load_yaml('erk_description', 'config/ompl_planning.yaml')
    
    # In MoveIt 2 Jazzy, planning_plugins (plural) is required and must be a list!
    if 'planning_plugin' in ompl_yaml:
        del ompl_yaml['planning_plugin']
    ompl_yaml['planning_plugins'] = ['ompl_interface/OMPLPlanner']

    ompl_planning_pipeline = {
        'moveit_default_planning_pipeline': 'ompl',
        'planning_pipelines': ['ompl'],
        'ompl': ompl_yaml
    }

    # Load Controllers Dict
    controllers_yaml = load_yaml('erk_description', 'config/moveit_controllers.yaml')
    moveit_controllers = {
        'moveit_simple_controller_manager': controllers_yaml.get('moveit_simple_controller_manager', {}),
        'moveit_controller_manager': controllers_yaml.get('moveit_controller_manager', '')
    }

    trajectory_execution = {
        'moveit_manage_controllers': True,
        'trajectory_execution.allowed_execution_duration_scaling': 1.2,
        'trajectory_execution.allowed_goal_duration_margin': 0.5,
        'trajectory_execution.allowed_start_tolerance': 0.01,
    }

    planning_scene_monitor = {
        'publish_planning_scene': True,
        'publish_geometry_updates': True,
        'publish_state_updates': True,
        'publish_transforms_updates': True,
    }

    # 1. Base Gazebo Launch
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. MoveGroup Node
    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_kinematics,
            robot_description_planning,
            ompl_planning_pipeline,
            moveit_controllers,
            trajectory_execution,
            planning_scene_monitor,
            {'use_sim_time': True}
        ]
    )

    # 3. RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_kinematics,
            robot_description_planning,
            ompl_planning_pipeline,
            {'use_sim_time': True}
        ]
    )

    return LaunchDescription([
        gazebo_launch,
        TimerAction(period=5.0, actions=[move_group_node]),
        TimerAction(period=8.0, actions=[rviz_node])
    ])
