import pygame as pg
from pygame import Color
from pygame.math import Vector2
import pgzero

import math

import model as Model
from entity import MovingEntity
from soccer_ball import Ball
from wall import Wall2D
# from team import SoccerTeam
import geometry as Geometry

HORIZ_REGIONS = 6
VERT_REGIONS = 3



class Goal:
    #which side of the RECT is the goal line
    GOAL_LINE_LEFT = 'left'
    GOAL_LINE_RIGHT = 'right'    
    def __init__(self,pos,w,h,color,goal_line):
        self._scored = False
        self.pos = Vector2(pos)
        self.rect = pg.Rect(pos,(w,h))

        self.goal_line = goal_line
        if self.goal_line == Goal.GOAL_LINE_LEFT:
            self.rect.midleft = self.pos
        elif self.goal_line == Goal.GOAL_LINE_RIGHT:
            self.rect.midright = self.pos

        #the post closer to top of screen
        if self.goal_line == Goal.GOAL_LINE_LEFT:
            self._left_post = Vector2(self.rect.topleft)
            self._right_post = Vector2(self.rect.bottomleft)
            self.facing = (self._left_post - self._right_post).normalize().rotate(90)

        elif self.goal_line == Goal.GOAL_LINE_RIGHT:
            self._left_post = Vector2(self.rect.topright)
            self._right_post = Vector2(self.rect.bottomright)
            self.facing = self.facing = (self._right_post - self._left_post).normalize().rotate(90)

        self.color = Color(color)
        self.goals_scored = 0

    def draw(self,screen):
        pg.draw.rect(screen,
                     self.color,
                     self.rect,
                     1)
        

    def scored(self, ball):
        return Geometry.line_interesection(ball.prev_pos,
                                           ball.pos,
                                           self._left_post,
                                           self._right_post)

class Region(pg.Rect):
    _ID = 0
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.id = Region._ID
        Region._ID += 1

    def draw(self,screen,render_id=True):
        screen.draw.rect(self,'gray')
        if render_id:
            screen.draw.text(str(self.id),center=self.center,color='gray')
        
class SoccerPitch:
#     # TODO: Refactor the game state functionality and window 
    # into a separate class
    def __init__(self,width, height, pos = (0,0), model = Model.initial_model):
        self.model = model
        self.surface = pg.Surface((width,height))
        self.pos = Vector2(pos) #Vector2(20,20) #pos
        self.field = self.surface.get_rect()
        self.field.inflate_ip(-2,-2)

        self.walls = []
        for a,b in [(self.field.topleft, self.field.topright),
                  (self.field.topright, self.field.bottomright),
                  (self.field.bottomright, self.field.bottomleft),
                  (self.field.bottomleft, self.field.topleft)]:
            self.walls.append( Wall2D(a,b,'yellow') )

        self.home_goal = Goal( self.field.midleft,
                               self.field.width*0.08,
                               self.field.height*0.25,
                               'red',
                               Goal.GOAL_LINE_LEFT)

        self.away_goal = Goal( self.field.midright,
                               self.field.width*0.08,
                               self.field.height*0.25,
                               'darkblue',
                               Goal.GOAL_LINE_RIGHT)
        
        # self.home_team = SoccerTeam(self.model, self,'HOME')
        # self.away_team = SoccerTeam(self.model, self,'AWAY')

        #playing area with padding
        # self.playing_area = pg.Rect(20,20,width-40,height-40)
        self.playing_area = pg.Rect(0,0,width,height)
        self.regions = [None]*(HORIZ_REGIONS * VERT_REGIONS)
        self.keeper_has_ball = False
        self.game_on = False
        self.paused = False
        self.win_dim = Vector2()

        self.create_regions(self.playing_area.width // HORIZ_REGIONS,
                            self.playing_area.height // VERT_REGIONS)

        self.ball= Ball(self.walls,
                        model = self.model,
                        center = self.pos + Vector2(width*0.5,height*0.5))

        # render the pitch onto a surface. This is not drawn until draw is called
        self._render_pitch()
        
        
##        self.ball.pos = width * 0.5, height * 0.5
        
        
    def _render_pitch(self):
        surface = self.surface
        field = self.field
        
        white = Color('white')
        surface.fill(Color('darkgreen'))

        fieldmidleft = field.midleft
        fieldmidright = field.midright
        
        #goals
        self.home_goal.draw(surface)
        self.away_goal.draw(surface)

        #penalty_box - left
        goal = self.home_goal.rect        
        pb = pg.Rect(0, 0, goal.width * 3.0, field.height * 0.5)
        pb.midleft = fieldmidleft
        pg.draw.rect(surface,
                     white,
                     pb,
                     1)

        #penalty_box_arc - left
        pbarc = pg.Rect(0, 0, pb.width * 0.35, pb.height * 0.5)
        pbarc.center = pb.midright
        pg.draw.arc(surface,
                    white,
                    pbarc,
                    -math.pi * 0.5,
                    math.pi * 0.5)

        #penalty_spot - left
        pb_spot = Vector2(pbarc.midleft)
        pb_spot.x *= 0.8
        pg.draw.circle(surface,
                       white,
                       (int(pb_spot.x),int(pb_spot.y)),
                       3)

        # penalty-box - right
        pb.midright = fieldmidright
        pg.draw.rect(surface,
                     white,
                     pb,
                     1)
        #penalty_box_arc - right
        pbarc.center = pb.midleft
        pg.draw.arc(surface,
                    white,
                    pbarc,
                    math.pi * 0.5,
                    math.pi * 1.5)

        #penalty_spot -right
        pb_spot = Vector2(pbarc.midright)
        pb_spot.x += (0.2 * (field.width - pbarc.midright[0]))
        pg.draw.circle(surface,
                       white,
                       (int(pb_spot.x),int(pb_spot.y)),
                       3)
        

        # midfield
        x1,y1 = field.midtop
        x1 -= 0
        
        pg.draw.line(surface,
                     white,
                     (x1,y1),(x1,field.height),
                     1)

        # field
        pg.draw.rect(surface,
                     white,
                     field, 
                     2)

        #render the ball
##        self.ball.draw(surface)
##        self.ball.draw()

        
        # walls
        for w in self.walls:
            w.draw(surface,True)
            
        # center circle
        pg.draw.circle(surface,
                       white,
                       field.center,
                       int(field.width * 0.15),
                       1)

        pg.draw.circle(surface,
                       white,
                       field.center,
                       3)                       


        
    def create_regions(self, width , height ):
        padl,padt = self.playing_area.left, self.playing_area.top

        for i in range(len(self.regions)-1,-1,-1):
            row = i // HORIZ_REGIONS
            col = i % HORIZ_REGIONS

            self.regions[i] = Region(col * width + padl, row * height + padt, width, height)


    def update(self, dt):
        pass

    def draw(self,screen):

        #render the pitch
        screen.blit(self.surface,self.pos) 

        #render regions
        if self.model.show_regions:
            for i,r in enumerate(self.regions):
                r.draw(screen)

        self.ball.draw()                
##        self.ball.draw()

        #render the teams
        # self.home_team.draw(screen)
        # self.away_team.draw(screen)


    def toggle_pause(self):
        self.paused != self.paused

    @property
    def cx(self):
        return self.win_dim.x

    @property
    def cy(self):
        return self.win_dim.y

    def region_from_index(self, id):
        assert (id >= 0 and id < len(self.regions)), "id == {}".format(id)
        return self.regions[id]

    def pos_from_region(self, id):
        #regions are stored in reverse order
        #so need to invert the id to get its position
        #in the array
        region = self.region_from_index(len(self.regions) - 1 - id)
        return region.center
        

if __name__ =='__main__':
    import pgzrun
    from soccer_pitch import SoccerPitch

    WIDTH = 300
    HEIGHT = 300

    p = SoccerPitch(300,300)


    def draw():
        screen.fill(Color('white')[:3])
        p.draw(screen)

    pgzrun.go()
