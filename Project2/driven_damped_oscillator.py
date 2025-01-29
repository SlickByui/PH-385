########################################
#
#
#
########################################

#Import Libraries
import numpy as np
from matplotlib import pyplot as plt

class driven_damped_oscillator:
    def __init__(self,theta0, omega0,Fd,offset,run_poincare = False):
        #Define initial conditions
        self.q = 0.5
        self.g = 9.8
        self.l = 9.8
        self.Fd = Fd
        self.Od = 2.0/3.0

        self.theta0 = theta0
        self.omega0 = omega0
        self.theta = [] #Redefine these later
        self.omega = []
        
        self.dt = 0.04
        self.poincare_run = run_poincare
        self.offset = offset

        #Set up our time
        if run_poincare:
            t_max = 10000
        else:
            t_max = 1000

        self.time = np.arange(0,t_max,self.dt) 
        

    def derivs(self,vars,t):
        theta = vars[0]
        omega  = vars[1]

        dTheta = omega
        dOmega = -(self.g/self.l)*np.sin(theta) -self.q*omega + self.Fd * np.sin(self.Od * t)
        return np.array([dTheta,dOmega])
    
    def poincare(self,vars,t,plot_list1,plot_list2):
        phase = self.Od*t % (2*np.pi)
        if (abs(phase - self.offset) < self.dt):
            plot_list1.append(vars[0])
            plot_list2.append(vars[1])
        return

    def RK4(self, vars,t):
        k1 = self.dt * self.derivs(vars,t)
        k2 = self.dt * self.derivs(vars + 1/2 * k1,t)
        k3 = self.dt * self.derivs(vars + 1/2 * k2,t)
        k4 = self.dt * self.derivs(vars + k3,t)

        vars += 1/6. * (k1 + 2 * k2 + 2 * k3 + k4)
        return vars
    
    def wrap_around(self,upper_bound,lower_bound, vars):
        #Wrap around conditions
        if vars[0] > upper_bound:
            while vars[0] > upper_bound:
                vars[0] -= 2*np.pi
        
        if vars[0] < lower_bound:
            while vars[0] < lower_bound:
                vars[0] += 2*np.pi

        return vars
    
    def run(self):
        vars = np.array([self.theta0,self.omega0])
        for t in self.time:

            self.theta.append(vars[0])
            self.omega.append(vars[1])

            #RK4 function
            vars = self.RK4(vars,t)

            #Wrap around conditions
            vars = self.wrap_around(np.pi,-np.pi,vars)

    def plot_data(self):
        #Take our data and do poincare slicing for different offset values
        off_sets = [0,np.pi/2,np.pi/4]
        for offset in off_sets:
            theta_list = []
            omega_list = []
            self.offset = offset
            for iter,t in enumerate(self.time):
                vars = np.array([self.theta[iter],self.omega[iter]])
                self.poincare(vars,t,theta_list,omega_list)

            plt.plot(theta_list,omega_list,'.',markersize = 2)

        #Plot Visual constuctions
        plt.title("Omega vs Theta")
        plt.xlabel("Theta (rads)")
        plt.ylabel("Omega (rads/s)")
        plt.show()