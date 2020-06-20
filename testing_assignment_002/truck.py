from car import Car
class Truck(Car):
    
    sound="Honk Honk"
    
    def __init__(self,color,max_speed,acceleration,tyre_friction,max_cargo_weight=None):
        if max_cargo_weight > 0:
            self._max_cargo_weight=max_cargo_weight
        else:
            raise ValueError("Invalid value for max_cargo_weight")
        super().__init__(color,max_speed,acceleration,tyre_friction)
        
        self._current_speed=0
        self._is_engine_started=False
        self.load_value=0
        
    @property
    def max_cargo_weight(self):
        return self._max_cargo_weight
        
    def load(self,value):
        if self._current_speed:
            print("Cannot load cargo during motion")
        else:
            if value < 0:
                raise ValueError("Invalid value for cargo_weight")
            else:
                temp=self.load_value + value
                if temp <= self._max_cargo_weight:
                    self.load_value=temp
                else:
                    print("Cannot load cargo more than max limit: {}".format(self._max_cargo_weight))
                
                
    
    def unload(self,value):
        if self._current_speed:
            print("Cannot unload cargo during motion")
        else:
            if value < 0:
                raise ValueError("Invalid value for cargo_weight")
            if value <= self.load_value :
                self.load_value -= value