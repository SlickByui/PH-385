###################################################################################
# Base String Class
# - Contains information about the string alongside methods to analyze, plot
#   and animate the data.
#
###################################################################################

#Import Libs
from matplotlib import pyplot as plt
import numpy as np

class string:
    def __init__(self, length, dx, wave_speed, t_max, r):
        #Initialize our values
        self.L = length
        self.dx = dx
        self.c = wave_speed
        self.r = r
        self.dt = dx*r/self.c
        self.t_max = t_max
        self.fft = []   #create our FFT list
        self.M = self.L/self.dx

        #Make i array from 0 to L given steps of dx
        self.i = np.arange(0,self.M + 1,1)

        #Create our x_array for plotting
        self.x_array = np.arange(0,self.L + self.dx,self.dx)

        #Set up time array
        self.time = np.arange(0,t_max + self.dt, self.dt)

        #Make our y_array
        self.y_array = np.zeros((len(self.x_array),len(self.time)),float)      #End points should be fixed

        #Create array of bool values about point fixedness
        self.fixed_point = np.full_like(self.x_array,False)

    #Function sets explicit points corresponding to y_array vals that are fixed
    def set_fixed_points(self,x_point:float):
        """ Function sets explicit points corresponding to y_array vals that are fixed
        (or clamped).
        """
        #Find closest point to input point
        i = np.argmin(np.abs(self.x_array-x_point))

        self.fixed_point[i] = True #Set fixed point to true
        return
    
    def spectral_analysis(self):
        """Function performs spectral analysis of our y values"""
        self.frequency = np.fft.fftfreq(len(self.time),self.dt)
        for i in range(0,len(self.x_array)):
            self.fft.append(np.fft.fft(self.y_array[i]))

        self.position_avg_fft = np.mean(np.abs(self.fft), axis=0)  # Average across the spatial dimension (x)
        pass

    def plot_fourier(self,x):
        """ Plots Fourier transform at a given position."""
        if len(self.fft) == 0: self.spectral_analysis()
            # find the maximum value in the fft array so we can set
            # appropiate limits for the plot. The FFT functions in 
            # numpy return values for positive and negative 
            # frequencies. We only want to show the positive 
            # frequencies
        fftmax = 0.0
        for fftstep in self.fft:
            for fft in fftstep:
                if abs(fft) > fftmax: fftmax = abs(fft)
        # find the index of the position we want to plot
        i = np.argmin(np.abs(self.x_array-x))
        # bulid the plot
        fig = plt.figure().add_subplot()
        fig.set_xlabel("Frequency (Hz)")
        fig.set_ylabel("Magnitude")
        fig.set_title(f"FFT at x = {x: .4f}")
        plt.gca().set_ylim(0.,fftmax)
        plt.gca().set_xlim(0.,1000)#max(self.frequency))
        fig.plot(self.frequency, abs(self.fft[i]))
        plt.show()

    def plot_average_fourier(self):
        """Plot the position-averaged power spectrum of the string."""
        power_spectrum_avg = np.abs(self.position_avg_fft) ** 2  # Power spectrum is the squared magnitude of the FFT
        plt.plot(self.frequency[:len(power_spectrum_avg)], power_spectrum_avg, label="Position-Averaged Power Spectrum")
        plt.gca().set_xlim(0.,1000)#max(self.frequency))
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Power")
        plt.title("Position-Averaged Power Spectrum")
        plt.grid()
        plt.legend()
        plt.show()

    def save_average_fourier(self, filename):
        """Save the Fourier power spectrum to a file."""
        power_spectrum = np.abs(self.position_avg_fft) ** 2  # Power spectrum
        with open(filename, "w") as file:
            for freq, power in zip(self.frequency, power_spectrum):
                file.write(f"{freq:.5f}\t{power:.5f}\n")
        pass
    
    def wave_animation(self):
        """Creates animation of the y_array values as the change through time"""
        #Loop through our time function to graph each segment of dt
        for t in range(0,len(self.time)):
            #Set our plot features
            plt.title("Basic Wave Eq.")
            plt.ylim([-2.0,2.0])
            plt.plot(self.x_array,self.y_array[:,t])
            plt.draw()
            plt.pause(0.01)
            plt.clf()

        plt.close()

        return

    
