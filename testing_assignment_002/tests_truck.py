import pytest
from truck import Truck

@pytest.fixture
def truck():
    truck_obj = Truck(color='Blue', max_speed=1, acceleration=1, tyre_friction=1, max_cargo_weight=1)
    return truck_obj

# case-1
def test_create_truck_object_instance_with_valid_details():
    # Arrange
    color='Blue'
    max_speed=1
    acceleration=1
    tyre_friction=1
    max_cargo_weight=1
    truck = Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)
    
    # Act
    
    # Assert
    assert truck.color == color
    assert truck.max_speed == max_speed 
    assert truck.acceleration == acceleration 
    assert truck.tyre_friction == tyre_friction 
    assert truck.max_cargo_weight == max_cargo_weight
    
# case-2
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction, max_cargo_weight",[
    ('Red',1,1,1,10)
])
def test_create_truck_object_instance_multiple_times_with_valid_details(color,max_speed,acceleration,tyre_friction,max_cargo_weight):
    # Arrange
    truck1 = Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)
    truck2 = Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)

    
    # Act
    
    # Assert
    assert truck1.color == color 
    assert truck1.max_speed == max_speed 
    assert truck1.acceleration == acceleration
    assert truck1.tyre_friction == tyre_friction
    assert truck1.max_cargo_weight == max_cargo_weight
    
    assert truck2.color == color 
    assert truck2.max_speed == max_speed 
    assert truck2.acceleration == acceleration
    assert truck2.tyre_friction == tyre_friction
    assert truck2.max_cargo_weight == max_cargo_weight
    
# case-2
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction, max_cargo_weight",[
    ('Red',0,1,1,10),('Blue',-1,1,1,5)])
def test_create_truck_object_with_invalid_max_speed_value_raise_error(
    color, max_speed, acceleration, tyre_friction, max_cargo_weight):
    # Arrange
    
    # Act
    with pytest.raises(ValueError) as truck:
        assert Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)
    
    # Assert
    assert str(truck.value) == 'Invalid value for max_speed'

# case-3
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction, max_cargo_weight",[
    ('Red',5,0,1,10),('Blue',9,-1,1,5)])
def test_create_truck_object_with_invalid_acceleration_value_raise_error(
    color, max_speed, acceleration, tyre_friction, max_cargo_weight):
    # Arrange
    
    # Act
    with pytest.raises(ValueError) as truck:
        assert Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)
    
    # Assert
    assert str(truck.value) == 'Invalid value for acceleration'
    
# case-4
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction, max_cargo_weight",[
    ('Red',5,2,0,10),('Blue',9,3,-1,5)])
def test_create_truck_object_with_invalid_tyre_friction_value_raise_error(
    color, max_speed, acceleration, tyre_friction, max_cargo_weight):
    # Arrange
    
    # Act
    with pytest.raises(ValueError) as truck:
        assert Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)
    
    # Assert
    assert str(truck.value) == 'Invalid value for tyre_friction'
    
# case-5
@pytest.mark.parametrize("color, max_speed, acceleration, tyre_friction, max_cargo_weight",[
    ('Red',5,2,1,0),('Blue',9,3,2,-1)])
def test_create_truck_object_with_invalid_max_cargo_weight_value_raise_error(
    color, max_speed, acceleration, tyre_friction, max_cargo_weight):
    # Arrange
    
    # Act
    with pytest.raises(ValueError) as truck:
        assert Truck(color=color, max_speed=max_speed, acceleration=acceleration, tyre_friction=tyre_friction, max_cargo_weight=max_cargo_weight)
    
    # Assert
    assert str(truck.value) == 'Invalid value for max_cargo_weight'
    
    
# case-6
def test_start_engine_when_truck_is_at_rest_and_update_is_engine_started(truck):
    # Arrange
    engine_started = True
    
    # Act
    truck.start_engine()
    
    # Assert
    assert truck.is_engine_started == engine_started

# case-7
def test_stop_engine_when_truck_is_in_motion_and_update_is_engine_started(truck):
    # Arrange
    engine_started = False
    truck.start_engine()
    
    # Act
    truck.stop_engine()
    
    # Assert
    assert truck.is_engine_started == engine_started
    
# case-8
def test_accelerate_truck_when_engine_started_and_update_current_speed():
    # Arrange
    truck = Truck(color='Blue', max_speed=1, acceleration=1, tyre_friction=1, max_cargo_weight=1)
    truck.start_engine()
    current_speed_value = 1
    
    # Act
    truck.accelerate()
    
    # Assert
    assert truck.current_speed == current_speed_value
    
# case-9
def test_accelerate_truck_when_engine_stoped_and_return_start_engine_to_accelerate(capfd):
    # Arrange
    truck = Truck(color='Blue', max_speed=1, acceleration=1, tyre_friction=1, max_cargo_weight=1)
    start_engine_to_accelerate = "Start the engine to accelerate\n"
    
    # Act
    truck.accelerate()
    output = capfd.readouterr()
    
    # Assert
    assert output.out == start_engine_to_accelerate
    
# case-10
def test_accelerate_truck_when_current_speed_reaches_maximum_and_update_current_speed():  
    # Arrange
    truck = Truck(color='Blue', max_speed=9, acceleration=3, tyre_friction=1, max_cargo_weight=1)
    truck.start_engine()
    
    # Act
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    truck.accelerate()
    current_speed_value = 9
    
    # Assert
    assert truck.current_speed == current_speed_value
    
# case-11
def test_apply_brakes_when_truck_current_speed_is_less_than_tyre_friction_and_update_current_speed():
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=3, tyre_friction=4, max_cargo_weight=1)
    truck.start_engine()
    truck.accelerate()
    
    # Act
    truck.apply_brakes()
    current_speed_value = 0
    
    # Assert
    assert truck.current_speed == current_speed_value
    
# case-12
def test_apply_brakes_when_truck_current_speed_is_more_than_tyre_friction_and_update_current_speed():
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=1)
    truck.start_engine()
    truck.accelerate()
    
    # Act
    truck.apply_brakes()
    current_speed_value = 1
    
    # Assert
    assert truck.current_speed == current_speed_value
    
# case-13
def test_sound_horn_when_truck_engine_started_and_return_car_sound(capfd):
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=1)
    truck.start_engine()
    sound = "Honk Honk\n"
    
    # Act
    truck.sound_horn()
    output = capfd.readouterr()

    # Assert
    assert output.out == sound
    
# case-14
def test_sound_horn_when_truck_engine_stoped_and_return_start_engine_to_sound_horn(capfd):
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=1)
    start_engine_to_sound = "Start the engine to sound_horn\n"
    
    # Act
    truck.sound_horn()
    output = capfd.readouterr()

    # Assert
    assert output.out == start_engine_to_sound
    
# case-15
def test_truck_object_instance_create_and_engine_status():
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=1)
    engine_started = False
    
    # Act
    
    # Assert
    assert truck.is_engine_started == engine_started
    
# case-
def test_load_when_truck_in_motion_and_print_string(capfd):
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=100)
    truck.start_engine()
    truck.accelerate()
    cannot_load = "Cannot load cargo during motion\n"
    
    # Act
    truck.load(1)
    output = capfd.readouterr()
    
    # Assert
    assert output.out == cannot_load
    

def test_load_when_truck_not_in_motion_with_invalid_load_values_raise_error():
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=100)
    truck.start_engine()
    invalid_cargo_weight = "Invalid value for cargo_weight"
    
    # Act
    with pytest.raises(ValueError) as error:
        truck.load(-1)
        
    # Assert
    assert str(error.value) == invalid_cargo_weight

def test_load_when_truck_not_in_motion_with_load_value_more_than_maximum_value_and_print_string(capfd):
    # Arrange
    color='Blue'
    max_speed=5
    acceleration=4
    tyre_friction=3
    max_cargo_weight=1
    
    truck = Truck(
        color=color,
        max_speed=max_speed,
        acceleration=acceleration,
        tyre_friction=tyre_friction,
        max_cargo_weight=max_cargo_weight
    )
    cannot_load_more = "Cannot load cargo more than max limit: {}\n".format(max_cargo_weight)
    
    # Act
    truck.load(2)
    output = capfd.readouterr()
    
    # Assert
    assert output.out == cannot_load_more
    

def test_load_when_truck_not_in_motion_with_valid_load_values_and_update_load_in_truck():
    # Arrange
    color='Blue'
    max_speed=5
    acceleration=4
    tyre_friction=3
    max_cargo_weight=1
    
    truck = Truck(
        color=color,
        max_speed=max_speed,
        acceleration=acceleration,
        tyre_friction=tyre_friction,
        max_cargo_weight=max_cargo_weight
    )
    load_value = 1
    
    # Act
    truck.load(1)
    
    # Assert
    assert truck.load_value == load_value

def test_load_when_truck_not_in_motion_with_valid_load_value_equals_to_zero_and_update_load_in_truck():
    # Arrange
    color='Blue'
    max_speed=5
    acceleration=4
    tyre_friction=3
    max_cargo_weight=100
    
    truck = Truck(
        color=color,
        max_speed=max_speed,
        acceleration=acceleration,
        tyre_friction=tyre_friction,
        max_cargo_weight=max_cargo_weight
    )
    load_value = 0
    
    # Act
    truck.load(0)
    
    # Assert
    assert truck.load_value == load_value
    
# case-
def test_unload_when_truck_in_motion_and_print_string(capfd):
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=100)
    truck.start_engine()
    truck.load(1)
    truck.accelerate()
    cannot_unload = "Cannot unload cargo during motion\n"
    
    # Act
    truck.unload(1)
    output = capfd.readouterr()
    
    # Assert
    assert output.out == cannot_unload

def test_unload_when_truck_not_in_motion_with_invalid_load_values_raise_error():
    # Arrange
    truck = Truck(color='Blue', max_speed=5, acceleration=4, tyre_friction=3, max_cargo_weight=100)
    truck.start_engine()
    truck.load(5)
    invalid_cargo_weight = "Invalid value for cargo_weight"
    
    # Act
    with pytest.raises(ValueError) as error:
        truck.unload(-1)
        
    # Assert
    assert str(error.value) == invalid_cargo_weight

def test_unload_when_truck_not_in_motion_with_valid_load_value_equal_to_available_load_and_update_load_in_truck():
     # Arrange
    color='Blue'
    max_speed=5
    acceleration=4
    tyre_friction=3
    max_cargo_weight=100
    
    truck = Truck(
        color=color,
        max_speed=max_speed,
        acceleration=acceleration,
        tyre_friction=tyre_friction,
        max_cargo_weight=max_cargo_weight
    )
    
    truck.load(2)
    load_value = 0
    
    # Act
    truck.unload(2)
    
    # Assert
    assert truck.load_value == load_value
    
def test_unload_when_truck_not_in_motion_with_valid_load_value_zero_and_update_load_in_truck():
     # Arrange
    color='Blue'
    max_speed=5
    acceleration=4
    tyre_friction=3
    max_cargo_weight=100
    
    truck = Truck(
        color=color,
        max_speed=max_speed,
        acceleration=acceleration,
        tyre_friction=tyre_friction,
        max_cargo_weight=max_cargo_weight
    )
    
    truck.load(2)
    load_value = 2
    
    # Act
    truck.unload(0)
    
    # Assert
    assert truck.load_value == load_value
    


# case-21
def test_truck_max_speed_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.max_speed = 5
        
    
    # Assert
    assert str(error.value) == attribute_error
    
# case-22
def test_truck_acceleration_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.acceleration = 5 
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-23
def test_truck_tyre_friction_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.tyre_friction = 5
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-24
def test_truck_current_speed_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.current_speed = 5
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-25
def test_truck_is_engine_started_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.is_engine_started = False
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-26
def test_truck_color_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.color = 'Yellow'
        
    # Assert
    assert str(error.value) == attribute_error
    
# case-26
def test_truck_max_cargo_weight_attribute_encapsulation_raise_attrubute_error(truck):
    
    # Arrange
    attribute_error = "can't set attribute"
    
    # Act
    with pytest.raises(AttributeError) as error:
        truck.max_cargo_weight = 50
        
    # Assert
    assert str(error.value) == attribute_error




