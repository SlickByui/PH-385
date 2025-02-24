###################################################################################
# Test Routine Class
# - Custom testing function for testing code from Project 5
#
###################################################################################
# Things to check:
#   - var types and returns of our init vars and arrays
#   - Check why propogating wave twice works (maybe the first few time steps?)
#   - Make sure our array is working the way it needs to

#Import libs
from basic_wave import basic_wave
from matplotlib import pyplot as plt
import csv

class test:
    #Not sure if init needs anything for now
    def __init__(self):
        pass

    #Run function will run through the set parameters we define inside it.
    #Nothing needs to be passed through main
    def run(self):
        #Initialize here so we dont run it instantly in main
        #Define our init values
        length = 1    #m
        dx = 0.01     #m
        wave_speed = 200
        t_max = 0.1

        #Initialize our basic wave
        self.test_wave = basic_wave(length,dx,wave_speed,t_max)

        #Walk through animation to see if problems arise
        self.animation_walkthrough()
        
        return
    

    def check_first_frames(self):
        """ Function checks the types and lengths of 
        
        """    
        #Check to see if the first "frame" corresponds to the correct values of our Gauss pluck
        self.plot_frame(0,title="Frame 0 before displace")
        self.test_wave.displace(0.3)
        self.plot_frame(0,title="Frame 0 after displace")

        #Propogate the wave to see how it affects the second frame
        self.plot_frame(1,title="Frame 1 before 1st propogate")
        self.test_wave.propogate()
        self.plot_frame(1,title="Frame 1 after 1st propogate")

        #Propogate again to see if it has changed
        self.plot_frame(1,title="Frame 1 before 2nd propogate")
        self.test_wave.propogate()
        self.plot_frame(1,title="Frame 1 after 2nd propogate")
        return


    def check_graphs():

        pass

    def animation_walkthrough(self):

        #Propogate once
        self.test_wave.displace(0.3)
        self.test_wave.propogate()

        #Loop through our time function to graph each segment of dt
        self.plot_frame(0)

        for t in range(0,len(self.test_wave.time)):
            plt.title("Animation walkthrough: frame: " + str(t))
            plt.ylim([-3.5,3.5])
            plt.plot(self.test_wave.x_array,self.test_wave.y_array[:,t])
            plt.draw()
            step = input("")
            plt.pause(0.01)
            plt.clf()

        plt.close()

    def plot_frame(self,frame:int, title:str = ""):
        plt.title(title)
        plt.plot(self.test_wave.x_array,self.test_wave.y_array[:,frame])
        plt.show()

    #Read writes input data to csv
    def log_output(self, file_name:str,data):
        with open(file_name + ".csv", "w", newline="") as file:
            for t in range(0,len(self.test_wave.time)):
                data = 1
                writer = csv.writer(file)
                for item in data:
                    writer.writerow([item])
        return