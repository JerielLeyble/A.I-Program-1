#Jeriel Leyble CS330 Finished 9/19/2023
import numpy as np #
import math # This library allows me to access square root, pi, etc.
import csv # used for file manipulation

#some math stuff to help with code
#length of vector
def length(v):
    return np.sqrt(v[0] ** 2 + v[1] ** 2)
#normalize a vector
def normalize(v):
    lengthV = length(v)
    if lengthV != 0:
        return np.array([v[0] / lengthV, v[1] / lengthV])
    else:
        return np.array([0, 0])

Continue = 1
Seek = 6   
Flee = 7
Arrive = 8
Time = 0
deltaTime = 0.50
stopTime = 50.5

#character class
class character(object):
    def __init__(self):
        self.id = 0
        self.steer = 1
        self.position = np.array([0.0, 0.0], dtype=float)
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.orientation = 0.0
        self.linear = np.array([0.0, 0.0], dtype=float)
        self.angular = 0.0
        self.maxVelocity = 0.0
        self.maxLinear = 0.0
        self.maxAngular = 0.0
        self.target = 0.0
        self.rotation = 0.0
        self.arriveRadius = 0.0
        self.arriveSlow = 0.0
        self.arriveTime = 0.0
#character for continue
charactercontinue = character()
charactercontinue.id = 2601
charactercontinue.steer = 1

#character for seek
characterseek = character()
characterseek.id=2603
characterseek.steer=6
characterseek.position=np.array([-50.0,40.0])
characterseek.velocity=np.array([0.0,8.0])
characterseek.orientation=3* (math.pi / 2)
characterseek.maxVelocity=8.0
characterseek.maxLinear=2.0
characterseek.target=1.0


#character for flee
characterflee = character()
characterflee.id=2602
characterflee.steer=7
characterflee.position=np.array([-30.0,-50.0])
characterflee.velocity=np.array([2.0,7.0])
characterflee.orientation= (math.pi) / (4)
characterflee.maxVelocity = 8.0
characterflee.maxLinear = 1.5
characterflee.target = 1.0

#character for arrive
characterarrive = character()
characterarrive.id= 2604
characterarrive.steer=8
characterarrive.position=np.array([50.0,75.0])
characterarrive.velocity=np.array([-9.0,4.0])
characterarrive.orientation=math.pi
characterarrive.maxVelocity=10.0
characterarrive.maxLinear=2.0
characterarrive.target=1.0
characterarrive.arriveRadius=4.0
characterarrive.arriveSlow=32.0
characterarrive.arriveTime=1.0

#outputs from steering behavior
class steeringOutput(object):
    def __init__(self):
        self.linear = np.array([0.0, 0.0])  # linear acceleration, 2D vector (e.g., [x, y])
        self.angular = 0

#updates movement of character 
def update(character, steeringOutput, maxSpeed, deltaTime):

    #Update the position and orientation
    
    character.position += character.velocity * deltaTime
    character.orientation += character.rotation * deltaTime

    #Update the velocity and rotation
    character.velocity += steeringOutput.linear * deltaTime
    character.rotation += steeringOutput.angular * deltaTime

    #Check for speed above max and clip
    if length(character.velocity) > maxSpeed:
        character.velocity = normalize(character.velocity)
        character.velocity *= maxSpeed
    
    return {
        'position_x': character.position[0],
        'position_z': character.position[1],
        'velocity_x': character.velocity[0],
        'velocity_z': character.velocity[1],
        'linear_acceleration_x': steeringOutput.linear[0],
        'linear_acceleration_z': steeringOutput.linear[1],
        'orientation': character.orientation,
        'steering_behavior_code': character.steer,
        'collision_status': False
    }

#algorithm implementation
#continue movement
def continueAlg(charactercontinue):
    result = steeringOutput()
    result.linear = np.array([0.0, 0.0])
    result.angular = 0
    return result

#seek alg (character, target)
def seekAlg(characterseek, charactercontinue):
    result = steeringOutput()
    #get the direction to the target
    result.linear = charactercontinue.position - characterseek.position

    #accelerate at maximum rate
    result.linear = normalize(result.linear)
    result.linear *= characterseek.maxLinear

    #output steering
    result.angular = 0
    return result
#flee alg 
def fleeAlg(characterflee, charactercontinue):
    result = steeringOutput()
    #get the direction to the target
    result.linear = characterflee.position - charactercontinue.position

    #accelerate at maximum rate
    result.linear = normalize(result.linear)
    result.linear *= characterflee.maxLinear

    #output steering
    result.angular = 0
    return result

#arrive alg(currently seek, will modify to arrive)
def arriveAlg(characterarrive, charactercontinue):
    result = steeringOutput()
    timeToTarget = 0.1
    #get the direction and distance to the target
    direction = charactercontinue.position - characterarrive.position
    distance = length(direction)

    #test for arrival
    if distance < characterarrive.arriveRadius:
        return result
    
    #outside slowing-down (outer) radius, move at max speed
    elif distance > characterarrive.arriveSlow:
        arriveSpeed = characterarrive.maxVelocity

    #Between radii, scale speed to slow down 
    else:
        arriveSpeed = characterarrive.maxVelocity * distance / characterarrive.arriveSlow
    
    #Target velocity combines speed and direction    
    arriveVelocity = direction
    arriveVelocity = normalize(arriveVelocity)
    arriveVelocity *= arriveSpeed  
    #arriveVelocity = normalize(direction) * arriveSpeed
    
    #accelerate to target velocity
    result.linear = arriveVelocity - characterarrive.velocity
    result.linear /= timeToTarget
    
    #test for too fast acceleration
    if length(result.linear) > characterarrive.maxLinear:
        result.linear = normalize(result.linear)
        result.linear *= characterarrive.maxLinear

    #output steering
    result.angular = 0
    return result

#just used for testing(ignore teach)
print("success!")

#list for results
results = []

#sim loop
simulationTime = 0
while simulationTime < stopTime:
    # Call continueAlg and seekAlg functions to get steering
    continueSteering = continueAlg(charactercontinue)
    seekSteering = seekAlg(characterseek, charactercontinue)
    fleeSteering = fleeAlg(characterflee, charactercontinue)
    arriveSteering = arriveAlg(characterarrive,charactercontinue)
    
    # Update characters using the update function
    charactercontinueAttributes = update(charactercontinue, continueSteering, charactercontinue.maxVelocity, deltaTime)
    characterfleeAttributes = update(characterflee, fleeSteering, characterflee.maxVelocity, deltaTime)
    characterseekAttributes = update(characterseek, seekSteering, characterseek.maxVelocity, deltaTime)
    characterarriveAttributes = update(characterarrive, arriveSteering, characterarrive.maxVelocity, deltaTime)

    # Append the character attributes to the results list
    results.append({
        'simulation_time': simulationTime,
        'character_id': charactercontinue.id,
        **charactercontinueAttributes
    })

    results.append({
        'simulation_time': simulationTime,
        'character_id': characterflee.id,
        **characterfleeAttributes
    })

    results.append({
        'simulation_time': simulationTime,
        'character_id': characterseek.id,
        **characterseekAttributes
    })

    results.append({
        'simulation_time': simulationTime,
        'character_id': characterarrive.id,
        **characterarriveAttributes
    })

    
    # Increment simulation time
    simulationTime += deltaTime

def write_csv(filename, rows):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'simulation_time',
            'character_id',
            'position_x',
            'position_z',
            'velocity_x',
            'velocity_z',
            'linear_acceleration_x',
            'linear_acceleration_z',
            'orientation',
            'steering_behavior_code',
            'collision_status'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write rows
        for row in rows:
            writer.writerow(row)
            

# Write the results to a CSV file
write_csv('character_data.txt', results)