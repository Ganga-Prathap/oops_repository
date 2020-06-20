import pytest
from race_car import RaceCar

@pytest.fixture
def race_car():
    
    race_car_obj = RaceCar(
        color='Red',
        max_speed=30,
        acceleration=10,
        tyre_friction=3
    )
        
    return race_car_obj

# case-1
def test_create_race_car_object_instance_with_valid_details():
    
    # Arrange
    color='Blue'
    max_speed=30
    acceleration=10
    tyre_friction=5
    
    # Act
    race_car = RaceCar(
        color=color, 
        max_speed=max_speed, 
        acceleration=acceleration, 
        tyre_friction=tyre_friction
    )
    
    # Assert
    assert race_car.color == color 
    assert race_car.max_speed == max_speed 
    assert race_car.acceleration == acceleration
    assert race_car.tyre_friction == tyre_friction

# case-2
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',1,1,1)])
def test_create_race_car_object_instance_multiple_times_with_valid_details(color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    
    # Act
    race_car_1 = RaceCar(
        color=color, 
        max_speed=max_speed, 
        acceleration=acceleration, 
        tyre_friction=tyre_friction
    )
        
    race_car_2 = RaceCar(
        color=color, 
        max_speed=max_speed, 
        acceleration=acceleration, 
        tyre_friction=tyre_friction
    )
    
    # Assert
    assert race_car_1.color == color 
    assert race_car_1.max_speed == max_speed 
    assert race_car_1.acceleration == acceleration
    assert race_car_1.tyre_friction == tyre_friction
    
    assert race_car_2.color == color 
    assert race_car_2.max_speed == max_speed 
    assert race_car_2.acceleration == acceleration
    assert race_car_2.tyre_friction == tyre_friction

# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',0,10,15),('Blue',-1,10,5)])
def test_create_race_car_object_with_invalid_max_speed_value_raise_error(color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    invalid_max_speed = 'Invalid value for max_speed'
    
    # Act
    with pytest.raises(ValueError) as race_car:
        assert RaceCar(
            color=color, 
            max_speed=max_speed, 
            acceleration=acceleration, 
            tyre_friction=tyre_friction
        )
    
    # Assert
    assert str(race_car.value) == invalid_max_speed

# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',30,0,5),('Blue',30,-1,5)])
def test_create_race_car_object_with_invalid_acceleration_value_raise_error(color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    invalid_acceleration = 'Invalid value for acceleration'
    
    # Act
    with pytest.raises(ValueError) as race_car:
        assert RaceCar(
            color=color, 
            max_speed=max_speed, 
            acceleration=acceleration, 
            tyre_friction=tyre_friction
        )
    
    # Assert
    assert str(race_car.value) == invalid_acceleration
    
# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',30,10,0),('Blue',30,10,-1)])
def test_create_race_car_object_with_invalid_tyre_friction_value_raise_error(color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    invalid_tyre_friction = 'Invalid value for tyre_friction'
    
    # Act
    with pytest.raises(ValueError) as race_car:
        assert RaceCar(
            color=color, 
            max_speed=max_speed, 
            acceleration=acceleration, 
            tyre_friction=tyre_friction
        )
    
    # Assert
    assert str(race_car.value) == invalid_tyre_friction

# case-9
def test_start_engine_when_race_car_is_at_rest_and_update_is_engine_started(race_car):
    
    # Arrange
    engine_started = True
    
    # Act
    race_car.start_engine()
    
    # Assert
    assert race_car.is_engine_started == engine_started

# case-10
def test_stop_engine_when_race_car_is_in_motion_and_update_is_engine_started(race_car):
    
    # Arrange
    engine_started = False
    race_car.start_engine()
    
    # Act
    race_car.stop_engine()
    
    # Assert
    assert race_car.is_engine_started == engine_started

# case-11
def test_accelerate_race_car_when_nitro_not_available_and_update_current_speed():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=20,
        acceleration=10,
        tyre_friction=5
    )
    current_speed_value = 10
    race_car.start_engine()
    
    # Act
    race_car.accelerate()
    
    # Assert
    assert race_car.current_speed == current_speed_value
    
# case-11
def test_accelerate_race_car_when_nitro_available_and_update_current_speed():
    import math
    # Arrange
    color='Red'
    max_speed=20
    acceleration=6
    tyre_friction=3
    race_car = RaceCar(
        color=color,
        max_speed=max_speed,
        acceleration=acceleration,
        tyre_friction=tyre_friction
    )
    current_speed_value = math.ceil((2*acceleration-tyre_friction)+(0.3)*acceleration+acceleration)
    race_car.start_engine()
    race_car.accelerate()
    race_car.accelerate()
    race_car.apply_brakes()
    
    # Act
    race_car.accelerate()
    
    # Assert
    assert race_car.current_speed == current_speed_value

# case-12
def test_accelerate_race_car_when_engine_stoped_and_return_start_engine_to_accelerate(capfd):
    
     # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=20,
        acceleration=10,
        tyre_friction=5
    )
    start_engine_to_accelerate = "Start the engine to accelerate\n"
    
    # Act
    race_car.accelerate()
    output = capfd.readouterr()
    
    # Assert
    assert output.out == start_engine_to_accelerate

# case-13    
def test_accelerate_race_car_multiple_times_when_nitro_not_available_and_update_current_speed():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=100,
        acceleration=10,
        tyre_friction=5
    )
    current_speed_value = 40
    race_car.start_engine()
    
    # Act
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    
    # Assert
    assert race_car.current_speed == current_speed_value
    
def test_accelerate_race_car_multiple_times_when_nitro_available_and_update_current_speed():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=100,
        acceleration=15,
        tyre_friction=15
    )
    current_speed_value = 85
    race_car.start_engine()
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    race_car.apply_brakes()
    race_car.apply_brakes()
    race_car.apply_brakes()
    
    # Act
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    
    # Assert
    assert race_car.current_speed == current_speed_value

# case-14
def test_accelerate_race_car_when_current_speed_reaches_maximum_and_update_current_speed():  
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=30,
        acceleration=10,
        tyre_friction=5
    )
    current_speed_value = 30
    race_car.start_engine()
    
    # Act
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    
    # Assert
    assert race_car.current_speed == current_speed_value
    
# case-15
def test_apply_brakes_to_race_car_and_update_current_speed():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=100,
        acceleration=10,
        tyre_friction=10
    )
    current_speed_value = 0
    race_car.start_engine()
    race_car.accelerate()
    
    # Act
    race_car.apply_brakes()
    
    # Assert
    assert race_car.current_speed == current_speed_value

# case-15
def test_apply_brakes_to_race_car_when_current_speed_more_than_half_the_max_speed_and_update_nitro():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=100,
        acceleration=20,
        tyre_friction=10
    )
    current_speed_value = 0
    race_car.start_engine()
    race_car.accelerate()
    race_car.accelerate()
    race_car.accelerate()
    nitro_value = 10
    
    # Act
    race_car.apply_brakes()
   
    
    # Assert
    assert race_car.nitro == nitro_value
    
def test_apply_brakes_to_race_car_when_current_speed_is_equal_to_more_than_half_the_max_speed_and_nitro_value():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=100,
        acceleration=25,
        tyre_friction=10
    )
    current_speed_value = 0
    race_car.start_engine()
    race_car.accelerate()
    race_car.accelerate()
    nitro_value = 0
    
    # Act
    race_car.apply_brakes()
   
    
    # Assert
    assert race_car.nitro == nitro_value
    
def test_apply_brakes_to_race_car_when_current_speed_not_more_than_half_the_max_speed_and_nitro_value():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=100,
        acceleration=20,
        tyre_friction=10
    )
    current_speed_value = 0
    race_car.start_engine()
    race_car.accelerate()
    race_car.accelerate()
    nitro_value = 0
    
    # Act
    race_car.apply_brakes()
   
    
    # Assert
    assert race_car.nitro == nitro_value

# case-16
def test_apply_brakes_when_race_car_current_speed_is_less_than_tyre_friction_and_update_current_speed():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=20,
        acceleration=9,
        tyre_friction=10
    )
    current_speed_value = 0
    race_car.start_engine()
    race_car.accelerate()
    
    # Act
    race_car.apply_brakes()
    
    # Assert
    assert race_car.current_speed == current_speed_value

# case-17
def test_apply_brakes_when_race_car_current_speed_is_more_than_tyre_friction_and_update_current_speed():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=4,
        acceleration=4,
        tyre_friction=3
    )
    current_speed_value = 1
    race_car.start_engine()
    race_car.accelerate()
    
    # Act
    race_car.apply_brakes()
    
    # Assert
    assert race_car.current_speed == current_speed_value

# case-18
def test_sound_horn_when_race_car_engine_started_and_return_race_car_sound(capfd):
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    sound = "Peep Peep\nBeep Beep\n"
    race_car.start_engine()
    
    # Act
    race_car.sound_horn()
    output = capfd.readouterr()

    # Assert
    assert output.out == sound

# case-19
def test_sound_horn_when_race_car_engine_stoped_and_return_start_engine_to_sound_horn(capfd):
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    start_engine_to_sound = "Start the engine to sound_horn\n"
    
    # Act
    race_car.sound_horn()
    output = capfd.readouterr()

    # Assert
    assert output.out == start_engine_to_sound
    
# case-20
def test_race_car_object_instance_create_and_engine_status():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    engine_started = False
    
    # Act
    
    # Assert
    assert race_car.is_engine_started == engine_started
    
def test_race_car_object_instance_create_and_nitro_status():
    
    # Arrange
    race_car = RaceCar(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    nitro_value = 0
    
    # Act
    
    # Assert
    assert race_car.nitro == nitro_value
    
# case-21
def test_race_car_max_speed_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.max_speed = 5
        
    
    # Assert
    assert str(error.value) == attribute_error
    
# case-22
def test_race_car_acceleration_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.acceleration = 5 
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-23
def test_race_car_tyre_friction_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.tyre_friction = 5
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-24
def test_race_car_current_speed_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.current_speed = 5
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-25
def test_race_car_is_engine_started_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.is_engine_started = False
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-26
def test_race_car_color_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.color = 'Yellow'
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-26
def test_race_car_nitro_attribute_encapsulation_raise_attrubute_error(race_car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        race_car.nitro = 10
        
    # Assert
    assert str(error.value) == attribute_error