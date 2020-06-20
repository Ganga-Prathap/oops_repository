import pytest
from car import Car

@pytest.fixture
def car():
    
    car_obj = Car(
        color='Red',
        max_speed=30,
        acceleration=10,
        tyre_friction=3
    )
        
    return car_obj

# case-1
def test_create_car_object_instance_with_valid_details():
    
    # Arrange
    color='Blue'
    max_speed=30
    acceleration=10
    tyre_friction=5
    
    # Act
    car = Car(
        color=color, 
        max_speed=max_speed, 
        acceleration=acceleration, 
        tyre_friction=tyre_friction
    )
    
    # Assert
    assert car.color == color 
    assert car.max_speed == max_speed 
    assert car.acceleration == acceleration
    assert car.tyre_friction == tyre_friction

# case-2
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red', 1, 1, 1)])
def test_create_car_object_instance_multiple_times_with_valid_details(
        color, max_speed, acceleration, tyre_friction):
    
    # Arrange
    
    # Act
    car_1 = Car(
        color=color, 
        max_speed=max_speed, 
        acceleration=acceleration, 
        tyre_friction=tyre_friction
    )
        
    car_2 = Car(
        color=color, 
        max_speed=max_speed, 
        acceleration=acceleration, 
        tyre_friction=tyre_friction
    )
    
    # Assert
    assert car_1.color == color 
    assert car_1.max_speed == max_speed 
    assert car_1.acceleration == acceleration
    assert car_1.tyre_friction == tyre_friction
    
    assert car_2.color == color 
    assert car_2.max_speed == max_speed 
    assert car_2.acceleration == acceleration
    assert car_2.tyre_friction == tyre_friction

# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',0,10,15),('Blue',-1,10,5)])
def test_create_car_object_with_invalid_max_speed_value_raise_error(
        color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    invalid_max_speed = 'Invalid value for max_speed'
    
    # Act
    with pytest.raises(ValueError) as car:
        assert Car(
            color=color, 
            max_speed=max_speed, 
            acceleration=acceleration, 
            tyre_friction=tyre_friction
        )
    
    # Assert
    assert str(car.value) == invalid_max_speed

# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',30,0,5),('Blue',30,-1,5)])
def test_create_car_object_with_invalid_acceleration_value_raise_error(
        color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    invalid_acceleration = 'Invalid value for acceleration'
    
    # Act
    with pytest.raises(ValueError) as car:
        assert Car(
            color=color, 
            max_speed=max_speed, 
            acceleration=acceleration, 
            tyre_friction=tyre_friction
        )
    
    # Assert
    assert str(car.value) == invalid_acceleration
    
# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction",[
    ('Red',30,10,0),('Blue',30,10,-1)])
def test_create_car_object_with_invalid_tyre_friction_value_raise_error(
        color,max_speed,acceleration,tyre_friction):
    
    # Arrange
    invalid_tyre_friction = 'Invalid value for tyre_friction'
    
    # Act
    with pytest.raises(ValueError) as car:
        assert Car(
            color=color, 
            max_speed=max_speed, 
            acceleration=acceleration, 
            tyre_friction=tyre_friction
        )
    
    # Assert
    assert str(car.value) == invalid_tyre_friction

# case-9
def test_start_engine_when_car_is_in_rest_and_update_is_engine_started(car):
    
    # Arrange
    engine_started = True
    
    # Act
    car.start_engine()
    
    # Assert
    assert car.is_engine_started == engine_started

# case-10
def test_stop_engine_when_car_is_in_motion_and_update_is_engine_started(car):
    
    # Arrange
    engine_started = False
    car.start_engine()
    
    # Act
    car.stop_engine()
    
    # Assert
    assert car.is_engine_started == engine_started

# case-11
def test_accelerate_car_when_engine_started_and_update_current_speed():
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=20,
        acceleration=10,
        tyre_friction=5
    )
    current_speed_value = 10
    car.start_engine()
    
    # Act
    car.accelerate()
    
    # Assert
    assert car.current_speed == current_speed_value

# case-12
def test_accelerate_car_when_engine_stoped_and_return_start_engine_to_accelerate(capfd):
    
     # Arrange
    car = Car(
        color='Red',
        max_speed=20,
        acceleration=10,
        tyre_friction=5
    )
    start_engine_to_accelerate = "Start the engine to accelerate\n"
    
    # Act
    car.accelerate()
    output = capfd.readouterr()
    
    # Assert
    assert output.out == start_engine_to_accelerate

# case-13    
def test_accelerate_car_multiple_times_and_update_current_speed():
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=100,
        acceleration=10,
        tyre_friction=5
    )
    current_speed_value = 40
    car.start_engine()
    
    # Act
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    
    # Assert
    assert car.current_speed == current_speed_value

# case-14
def test_accelerate_car_when_current_speed_reaches_maximum_and_update_current_speed():  
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=30,
        acceleration=10,
        tyre_friction=5
    )
    current_speed_value = 30
    car.start_engine()
    
    # Act
    car.accelerate()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    
    # Assert
    assert car.current_speed == current_speed_value
    
# case-15
def test_apply_brakes_to_car_and_update_current_speed():

    # Arrange
    car = Car(
        color='Red',
        max_speed=100,
        acceleration=10,
        tyre_friction=10
    )
    current_speed_value = 0
    car.start_engine()
    car.accelerate()
    car.accelerate()
    car.accelerate()
    
    # Act
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    
    # Assert
    assert car.current_speed == current_speed_value

# case-16
def test_apply_brakes_when_car_current_speed_is_less_than_tyre_friction_and_update_current_speed():
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=20,
        acceleration=9,
        tyre_friction=10
    )
    current_speed_value = 0
    car.start_engine()
    car.accelerate()
    
    # Act
    car.apply_brakes()
    
    # Assert
    assert car.current_speed == current_speed_value

# case-17
def test_apply_brakes_when_car_current_speed_is_more_than_tyre_friction_and_update_current_speed():
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    current_speed_value = 1
    car.start_engine()
    car.accelerate()
    
    # Act
    car.apply_brakes()
    car.apply_brakes()
    car.apply_brakes()
    
    # Assert
    assert car.current_speed == current_speed_value

# case-18
def test_sound_horn_when_car_engine_started_and_return_car_sound(capfd):
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    sound = "Beep Beep\n"
    car.start_engine()
    
    # Act
    car.sound_horn()
    output = capfd.readouterr()

    # Assert
    assert output.out == sound

# case-19
def test_sound_horn_when_car_engine_stoped_and_return_start_engine_to_sound_horn(capfd):
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    start_engine_to_sound = "Start the engine to sound_horn\n"
    
    # Act
    car.sound_horn()
    output = capfd.readouterr()

    # Assert
    assert output.out == start_engine_to_sound
    
# case-20
def test_car_object_instance_create_and_engine_status():
    
    # Arrange
    car = Car(
        color='Red',
        max_speed=130,
        acceleration=10,
        tyre_friction=3
    )
    engine_started = False
    
    # Act
    
    # Assert
    assert car.is_engine_started == engine_started
    
# case-21
def test_car_max_speed_attribute_encapsulation_raise_attrubute_error(car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        car.max_speed = 5
        
    
    # Assert
    assert str(error.value) == attribute_error
    
# case-22
def test_car_acceleration_attribute_encapsulation_raise_attrubute_error(car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        car.acceleration = 5 
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-23
def test_car_tyre_friction_attribute_encapsulation_raise_attrubute_error(car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        car.tyre_friction = 5
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-24
def test_car_current_speed_attribute_encapsulation_raise_attrubute_error(car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        car.current_speed = 5
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-25
def test_car_is_engine_started_attribute_encapsulation_raise_attrubute_error(car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        car.is_engine_started = False
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-26
def test_car_color_attribute_encapsulation_raise_attrubute_error(car):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        car.color = 'Yellow'
        
    # Assert
    assert str(error.value) == attribute_error