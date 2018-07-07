from enum import IntEnum

class Behavior(IntEnum):
    NONE = 0,
    SEEK = 2,
    FLEE = 4,
    ARRIVE = 8,
    WANDER = 16,
    COHESION = 32,
    SEPARATION = 64,
    ALIGNMENT = 128,
    OBSTACLE_AVOIDANCE = 256,
    WALL_AVOIDANCE = 512,
    FOLLOW_PATH = 1024,
    PURSUIT = 2048,
    EVADE = 4096,
    INTERPOSE = 8192,
    HIDE = 16384,
    FLOCK = 32768,
    OFFSET_PURSUIT = 65536

    @classmethod
    def str(cls,behavior):
        s = []
        if behavior == 0:
            return "none"
        
        if behavior & Behavior.SEEK > 0 :
            s.append("seek")
        
        if behavior & Behavior.FLEE > 0 :
            s.append("flee")
        
        if behavior & Behavior.ARRIVE > 0 :
            s.append("arrive")
        
        if behavior & Behavior.WANDER > 0 :
            s.append("wander")
        
        if behavior & Behavior.COHESION > 0 :
            s.append("cohesion")
        
        if behavior & Behavior.SEPARATION > 0 :
            s.append("separation")
        
        if behavior & Behavior.ALIGNMENT > 0 :
            s.append("alignment")
        
        if behavior & Behavior.OBSTACLE_AVOIDANCE > 0 :
            s.append("obstacle_avoidance")
        
        if behavior & Behavior.WALL_AVOIDANCE > 0 :
            s.append("wall_avoidance")
        
        if behavior & Behavior.FOLLOW_PATH > 0 :
            s.append("follow_path")
        
        if behavior & Behavior.PURSUIT > 0 :
            s.append("pursuit")

        if behavior & Behavior.EVADE > 0 :
            s.append("evade")

        if behavior & Behavior.INTERPOSE > 0 :
            s.append("interpose")

        if behavior & Behavior.HIDE > 0 :
            s.append("hide")
        
        if behavior & Behavior.FLOCK > 0 :
            s.append("flock")
        
        if behavior & Behavior.OFFSET_PURSUIT > 0 :
            s.append("offset_pursuit")
        
        return "{"+" | ".join(s)+"}"
        
        
        


if __name__=='__main__':
    behavior = Behavior.FLEE | Behavior.ARRIVE | Behavior.WANDER | Behavior.OFFSET_PURSUIT
    behavior = Behavior.SEEK
    print(Behavior.str(behavior))
    
