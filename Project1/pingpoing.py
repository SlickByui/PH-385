############################################################
# Ping Pong Object Class
#   
#
############################################################

#To Do
# - Cleanup code
# - Make more class variables
# - Better components
# - Save Graphs
# - Save table data

#Import Libraries
import numpy as np
from matplotlib import pyplot as plt
import csv

class PingPong:

    #Initialize Class
    def __init__(self, x0, v0, w0):
        #Maybe adjust to intake python native data?
        self.r=[]
        self.r.append(x0)
        self.x = np.copy(x0)

        self.v = np.copy(v0)
        self.w = np.copy(w0)
        self.t = [0]
    
    #Calculate the drag of vector v
    def Drag(self,v):
        #Define constants needed here
        C = 0.5      
        m = 0.0027   #mass in kg
        rho = 1.27   #kg/m^3
        r = 0.02     # radius in m

        A = np.pi * (0.02)**2    #Surface area of our ping pong ball in m^2  #Does this recalc every time?
        v_mag = np.linalg.norm(v)
        drag = 0.5*rho*A*C*v*v_mag
        return drag/m
    
    #Calculates the magnus force on the spinning object given its spin and velocity
    def MagnusAccel(self,v):
        S0_m = 0.040    #S0/m in si units
        wv = np.cross(self.w,v)
        return S0_m * wv
    
    #Come back to later
    def derivs(self,v):
        #Define Constants
        g = np.array([0,0,-9.8])   #could add later?

        #Set derivatives equal to old values
        dx = v
        dv = g - self.Drag(v) + self.MagnusAccel(v)

        return np.array([dx, dv])
    
    def RK2(self):
        #Define constants
        dt = 0.01
        z_is_positive = True
        n = 0   #this is an iterator for debugging

        while z_is_positive:
            k1 = dt*self.derivs(self.v)
            k2 = dt*self.derivs(self.v + k1[1]/2)

            #Update our positions and velocities
            self.x = self.x + k2[0]
            self.v = self.v + k2[1]

            #Append our new position to the list
            self.r.append(self.x)
            n += 1

            #Check if our Z is still positive (above ground)
            if self.x[2] <= 0:
                print("z = ", self.x[2])
                z_is_positive = False

        print("Runs = ", n)
        return
    
    def Euler(self):
        #Define constants
        dt = 0.01
        z_is_positive = True
        n = 0   #this is an iterator for debugging

        while z_is_positive:
            dx,dv = self.derivs(self.v)
            self.v = self.v + dv*dt
            self.x = self.x + dx*dt

            self.r.append(self.x)

            if self.x[2] <= 0:
                print("z = ", self.x[2])
                z_is_positive = False

        return

    #Saves positions of ping pong ball to CSV file
    def save_data(self, file_name):
        with open(file_name + ".csv", "w", newline="") as file:
            writer = csv.writer(file)
            for item in self.r:
                writer.writerow([item])
        return
    
    def plot_data(self):
        ax = plt.figure().add_subplot(projection='3d')
        ax.plot([el[0] for el in self.r],[el[1] for el in self.r],[el[2] for el in self.r],label="trajectory")
        plt.show()
        return
    