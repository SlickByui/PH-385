####################################################################
# Solar System Class
#  - Tracks a list of given celestial objects and simulates their
#    interactions and time evolved states
#
# Author: Nick Ball       Contact: bal16004@byui.edu
# Date: 2/10/2025
####################################################################

#Import Libraries
from numpy import array, arange, pi, linalg
from matplotlib import pyplot as plt
from celestial_object import celestial_object

class solar_system:

    def __init__(self,planets):
        """ Initialization function of the class
        Input: planets -> list of celestial_object objects

        Return: None
        """
        self.planet_list = planets   #list of celestial_object objects
        self.G = 4*pi**2
        self.M = self.calc_M()        #calculate the central mass
        self.R = self.calc_COM_pos()  #calculate the center of mass position
        self.V = self.calc_COM_vel()  #calculate the center of mass velocity

        #Automatically apply offset of COM and COV
        self.apply_offset()
        return

    def calc_M(self):
        """ Calculates the central mass of all the planetary masses
        Input: None
        Return: M : mass (AU)  -> float
        """
        M = 0.0   #Center of mass's mass

        #Loop through our planet list and sum the masses
        for planet in self.planet_list:
            M += planet.get_mass()
        return M

    def calc_COM_pos(self):
        """ Calculates the position R relative to the COM
        Input: None
        Return: R -> np.ndarray
        """
        R = array([0.0,0.0,0.0]) #initialize our R array

        #Loop through planets and add to center of mass
        for planet in self.planet_list:
            R = R + planet.get_mass() * planet.get_position()

        #Divide COM by M
        R = R/self.M

        return R
    
    def calc_COM_vel(self):
        """ Calculates the velocity V relative to the COM
        Input: None

        Return: V -> np.ndarray
        """
        V = array([0.0,0.0,0.0])

        for planet in self.planet_list:
            V = V + planet.get_mass() * planet.get_velocity()

        V = V/self.M

        return V

    def apply_offset(self):
        """ Applies the offset of R to the list of 'planets' to shift
            our reference frame to the center of mass frame
        Input: None

        Return: none
        """
        #Applies positional offset
        for planet in self.planet_list:
            planet.r = planet.r - self.R
            planet.pos[0] = planet.r   #reset the first instance of list (could do later)

        #Applies velocity offset
        for planet in self.planet_list:
            planet.v = planet.v - self.V

        return
    
    def a(self,planet1:celestial_object):
        """ Calculates  and returns the acceleration on the inputted planet
        from the other planets provided
        Input: Planet -> celestial_object

        Return: accel: acceleration -> np.ndarray
        """
        a = array([0,0,0])   #initialize our accel array
        G = 4*pi**2          #Gravitational constant

        for planet2 in self.planet_list:
            #Calculate the acceleration between two planets only if 
            # it is not planet1 (ie itself)
            if planet1.name != planet2.name:
                r12 = planet2.get_position() - planet1.get_position()
                mag = linalg.norm(r12)
                a = a + r12 * (planet2.get_mass()/(mag**3))
        return G*a

    def first_verlet(self,planet:celestial_object,dt:float):
        """ Calculates the first verlet calculation 
        Input: planet -> celestial_object
        Output: pos_vec: position vector -> nd.array
        """
        pos_vec = planet.r + planet.v*dt + 0.5*self.a(planet)*dt**2
        return pos_vec

    def verlet(self,planet:celestial_object,dt:float):
        """ Calculates the n+1 verlet step for the position of the given 
            planet.WILL NOT WORK FOR FIRST STEP.
        Input: Planet Position list -> list
               dt: time step -> float
        Return: pos_vec: updated change in position -> np.ndarray
        """
        pos_vec = 2*planet.r - planet.pos[-2] + self.a(planet)*dt**2

        return pos_vec

    def evolve(self, t_max:float, dt:float):
        """ Time evolves the system 
        Input: time: total time the system runs for (in years) -> float
                 dt: time increment (in years) -> float
        Return: None
        """
        #Create our time range to loop over
        t_range = arange(dt,t_max,dt)  #might not affect, but we want to start after a single iteration
        new_positions = []   #list of new positions

        #"Manually" run through our first verlet method
        for planet in self.planet_list:
            new_positions.append(self.first_verlet(planet,dt))

        #Update all of our planet positions (and their lists) at the same time
        for i,pos in enumerate(new_positions):
            self.planet_list[i].r = pos
            self.planet_list[i].pos.append(pos)

        new_positions.clear()  #Clear list for next use

        #Run the actual verlet loop 
        for t in t_range:
            for planet in self.planet_list:
                new_positions.append(self.verlet(planet,dt))

            for i,pos in enumerate(new_positions):
                self.planet_list[i].r = pos
                self.planet_list[i].pos.append(pos)
            
            new_positions.clear() #Clear list for next run
        return
    
    def plot_data(self,file_name:str):
        """ Plots and saves plot of our data to a file of the given file_name 
        Input: file_name -> str
        Return: None
        """
        ax = plt.figure().add_subplot(projection='3d')
        #Loop through planets and graph their trajectories
        for planet in self.planet_list:
            ax.plot([el[0] for el in planet.pos],[el[1] for el in planet.pos],[el[2] for el in planet.pos] ,label=planet.name + " trajectory")
        
        #Set up our graph details
        plt.title("Three Body Simulation")
        ax.set_xlabel("x (AU)")
        ax.set_ylabel("y (AU)")
        ax.set_zlabel("z (AU)")
        ax.set(xlim = [-3,3],ylim = [-3,3], zlim = [-3,3])
        plt.legend()
        plt.savefig(file_name)
        plt.show()

        return