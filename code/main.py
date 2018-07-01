from actors import Vehicle

class GameWorld:
    def __init__(self,width,height):
        #TODO: read this from config file        
        self._vehicles = [Vehicle(pos=(0.25*w,0.25*h),velocity=(40,0))] #[ Vehicle(pos=(0,0)) for v in range(2) ]
        self._obstacles = []
        self._walls = []

        self._paused = False
        self._window_dim = Vector2(width,height)
        self._crosshair = Vector2(width*0.5, height*0.5)

        self._show_walls = True
        self._show_obstacles = True
        self._show_path = True
        self._show_steering_force = True
        self._show_crosshair = True

        self._dirty_rect = []

    def _create_obstacles(self):
        pass

    def _create_walls(self):
        pass

    def update(self, time_elapsed):
        if self.paused:
            return

        del self._dirty_rect[:]
        
        for a in self.agents:
            a.update(time_elapsed)
            self._dirty_rect.append(a.image_rect)
            img, rect = a.update_display()
            self._dirty_rect.append(rect)

    def draw(self, surface):
        surface.blit(target_surf, target_surf.get_rect(center=self.crosshair) )
        
    def render(self, surface):
        if self.render_crosshair:
            self._dirty_rect.append(target_surf.get_rect(center=self.crosshair))
            #surface.blit(target_surf, target_surf.get_rect(center=self.crosshair))

        #for agent in self.agents:
        #    agent.render(surface)

    @property
    def dirty_rect(self):
        return self._dirty_rect
    
    def handleKeyPresses(self):
        pass

    def handleMenuItems(self):
        pass
    
    @property
    def walls(self):
        return self._walls

    @property
    def agents(self):
        return self._vehicles

    @property
    def obstacles(self):
        return self._obstacles

    @property
    def crosshair(self):
        return self._crosshair
    
    @crosshair.setter
    def crosshair(self,args):
        self._crosshair = Vector2(args)

    @property
    def paused(self):
        return self._paused
    
    @paused.setter
    def paused(self,flag):
        self._paused = flag
        
    @property
    def window_dim(self):
        return self._window_dim

    @property
    def render_steering_force(self):
        return self._show_steering_force

    @property
    def render_crosshair(self):
        return self._show_crosshair
