from pygame.math import Vector2

class Window:
    pass

class MenuItem:
    pass


class Display:

    # display view parameters
    show_states = False
    show_ids = False
    show_support_spots = False
    show_regions = False
    show_controlling_team = False
    show_targets = False
    show_highlight_when_threatened = False
    show_frame_rate = False


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
    init_behavior = [0]

class DisplayParams:
    show_render_aids = True
    show_bounding_radius = True
    show_steering = False
    show_obstacles = True
    show_crosshair = True
 

