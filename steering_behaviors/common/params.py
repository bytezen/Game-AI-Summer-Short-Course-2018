from pygame.math import Vector2
from common.behavior import Behavior

class BehaviorParams:
    threat_scan_distance = 100
    path_follow_scan_distance = 40
    offset_pursuit_offset = 15
    # controls how far away an agent can sense the environment
    view_distance = 100
    steering_force_tweaker = 200
    
class FlockingParams:
    view_distance = 10
    separation_multiplier = 1000
    alignment_multiplier = 1000    
    
class WanderParams:
    jitter = 10.0
    radius = 25.0
    distance = 0.0
    target = Vector2(0,-1)

class ObstacleAvoidanceParams:
    min_detection_box_length = 50

class ObstacleParams:
    number = 10

class WallAvoidanceParams:
    detection_feeler_length = 50
    repel_multiplier = 10.0

class VehicleParams:
    mass = 1.0
    max_speed = 10
    max_force = 100
    max_turn_rate = 50
    init_vel = (10,0)
    init_behavior = [Behavior.NONE]

class DisplayParams:
    show_render_aids = True
    show_bounding_radius = True
    show_steering = False
    show_obstacles = True
    show_crosshair = True
    


