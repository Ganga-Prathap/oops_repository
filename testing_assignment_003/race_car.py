from car import Car
class RaceCar(Car):
    
    sound="Peep Peep\nBeep Beep"
    
    def __init__(self,color,max_speed,acceleration,tyre_friction):
        super().__init__(color,max_speed,acceleration,tyre_friction)
        self._current_speed=0
        self._is_engine_started=False
        self._nitro=0
        
    @property
    def nitro(self):
        return self._nitro
        
    def accelerate(self):
        import math
        value=0
        if self._is_engine_started:
            if self._nitro > 0:
                value=(0.3)*self._acceleration
                self._nitro-=10
            speed=math.ceil((self._current_speed + value + self._acceleration))
            if speed <= self._max_speed:
                self._current_speed=speed
            else:
                self._current_speed=self._max_speed
        else:
            print("Start the engine to accelerate")
    
    def apply_brakes(self):
        if self._current_speed > (self._max_speed/2):
            self._nitro+=10
        self._current_speed-=self._tyre_friction
        if self._current_speed <= 0:
            self._current_speed=0
