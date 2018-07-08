from pygame.math import Vector2
from common.behavior import Behavior

class WanderParams:
    jitter = 5.0
    radius = 50.0
    distance = 50.0
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
    


