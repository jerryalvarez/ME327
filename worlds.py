import numpy as np
from carlo.world import World
from carlo.agents import Car, RectangleBuilding, Painting
from carlo.geometry import Point
import time

human_controller = False
NUM_LANES = 3
NUM_ROWS = 20
LANE_MARKER_SPACING = 3
LANE_MARKER_LENGTH = 3
LANE_MARKER_WIDTH = 0.15
LANE_BOTTOM_OFFSET = 1
GOAL_HEIGHT = 1
GRASS_WIDTH = 1
PIXELS_PER_METER = 15

WORLD_WIDTH = 20 #smaller lane 
#WORLD_WIDTH = 30 #medium lane
#WORLD_WIDTH = 50 #largest lane

WORLD_HEIGHT = 50
#WORLD_HEIGHT = 120 # dimension for Jerry's Dell Monitor

ROAD_WIDTH = (WORLD_WIDTH - 2 * GRASS_WIDTH) / NUM_LANES

LANE_PERCENTAGE = 35 #has to be less than 40

DT = 0.1 # time steps in terms of seconds. In other words, 1/dt is the FPS.

CAR_VEL = 5
#CAR_VEL = 0

class BaseCarlo():
    def __init__(self):
        """
        Describes a base Carlo world consisting of the car, a three-lane road,
        two side boundaries, a goal line, and a starting line.
        """
        self.world = World(
            DT,
            width = WORLD_WIDTH,
            height = WORLD_HEIGHT,
            ppm = PIXELS_PER_METER
        )
        self.dt = DT
        self._add_surroundings()
        self._init_car()

    def __del__(self):
        """
        Destructor: closes the Carlo world. 
        """
        self.world.close()

    def _add_surroundings(self):
        """
        Adds in the surroundings to the world, including:
            - road boundaries on each side (RectangleBuildings)
            - lane markings (Paintings)
            - finish line (Painting)
            - start line (Painting)
        """
        # add lane boundaries
        self.leftlane = RectangleBuilding(
            Point(
                GRASS_WIDTH + ROAD_WIDTH + ROAD_WIDTH * (LANE_PERCENTAGE/100),
                (WORLD_HEIGHT / 2) - (2 / PIXELS_PER_METER)
            ),
            Point(LANE_MARKER_WIDTH, WORLD_HEIGHT),
            color = 'Gray'
        )
        self.world.add(self.leftlane) 
        
        self.rightlane = RectangleBuilding(
            Point(
                GRASS_WIDTH + ROAD_WIDTH * 2 - ROAD_WIDTH * (LANE_PERCENTAGE/100),
                (WORLD_HEIGHT / 2) - (2 / PIXELS_PER_METER)
            ),
            Point(LANE_MARKER_WIDTH, WORLD_HEIGHT),
            color = 'Gray'
        )
        self.world.add(self.rightlane) 

        # add road boundaries
        self.left = RectangleBuilding(
            Point(
                GRASS_WIDTH / 2,
                (WORLD_HEIGHT / 2) - (2 / PIXELS_PER_METER)
            ),
            Point(GRASS_WIDTH, WORLD_HEIGHT),
            color = 'LawnGreen'
        )
        self.world.add(self.left) 
        
        self.right = RectangleBuilding(
            Point(
                WORLD_WIDTH - (GRASS_WIDTH / 2) + (2 / PIXELS_PER_METER),
                (WORLD_HEIGHT / 2) - (2 / PIXELS_PER_METER)
            ),
            Point(GRASS_WIDTH, WORLD_HEIGHT),
            color = 'LawnGreen'
        )
        self.world.add(self.right) 

        # add lane markers
        for lane_num in range(NUM_LANES - 1):
            for row_no in range(NUM_ROWS):
                center_x = GRASS_WIDTH + ROAD_WIDTH * (lane_num + 1)
                center_y = (
                    LANE_BOTTOM_OFFSET 
                    + LANE_MARKER_LENGTH / 2 
                    + row_no * (LANE_MARKER_SPACING + LANE_MARKER_LENGTH)
                )
                self.world.add(
                    Painting( # car cannot crash with lane markings
                        Point(center_x, center_y),
                        Point(LANE_MARKER_WIDTH, LANE_MARKER_LENGTH),
                        color = 'white'
                    )
                )

        # add finish line
        self.goal = Painting(
            Point(
                (WORLD_WIDTH) / 2 + (1 / PIXELS_PER_METER),
                WORLD_HEIGHT - (LANE_BOTTOM_OFFSET / 2) 
            ),
            Point(ROAD_WIDTH * NUM_LANES, GOAL_HEIGHT),
            color = 'DarkGreen'
        )
        self.world.add(self.goal)

        # add start line
        self.start = Painting(
            Point(
                (WORLD_WIDTH / 2) + (1 / PIXELS_PER_METER),
                1 / PIXELS_PER_METER
            ),
            Point(ROAD_WIDTH * NUM_LANES, 2 / PIXELS_PER_METER),
            color = 'black'
        )
        self.world.add(self.start)

    def _init_car(self):
        """
        Initializes the car in the world.
        """
        car_init_x = GRASS_WIDTH + (NUM_LANES // 2 ) * ROAD_WIDTH + 0.5 * ROAD_WIDTH
        car_init_y = LANE_BOTTOM_OFFSET + LANE_MARKER_LENGTH / 2
        self.car = Car(
            Point(car_init_x, car_init_y), # center of car
            (np.pi / 2) # heading it was (np.pi / 2) + np.radians(3) 
        )
        self.car.velocity = Point(0, CAR_VEL)
        self.car.friction = 0
        self.world.add(self.car)

    def render(self):
        """
        Renders the world into a graphic.
        """
        self.world.render()

    def tick(self):
        """
        Advances the world by one time step of size self.dt.
        """
        self.world.tick()
    
    def set_control(self, steering, acceleration):
        """
        Sets the control for the car at the current state of the world.

        Parameters:
            @param steering
                This control affects the car's angular velocity and heading.
            @param acceleration
                This control affects the car's speed.
        """
        self.car.set_control(steering, acceleration)


    def end_sim(self):
        """
        Checks to see if collision has occured at the left boundary or right boundary or car has reached its goal 
        """
        if (
            self.car.collidesWith(self.goal) or self.car.collidesWith(self.left) or 
            self.car.collidesWith(self.right) or self.car.collidesWith(self.start)
        ):
            return True
        else:
            return False