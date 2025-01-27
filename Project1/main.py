from pingpoing import PingPong
import numpy as np

#Define our data
x0 = np.array([0,0,10])
v0 = np.array([10,0,10])
w0 = np.array([0,5,5])

ping_pong = PingPong(x0,v0,w0)


#Debugging
print("Drag return type: ", type(ping_pong.Drag(v0)))
print("Drag return size: ", np.size(ping_pong.Drag(v0)))
print("Magnus Force return type: ", type(ping_pong.MagnusAccel(v0)))
print("Mag Force return size: ", np.size(ping_pong.Drag(v0)))
print("Derivs return type: ", type(ping_pong.derivs(v0)))

print(ping_pong.MagnusAccel(v0))
ping_pong.RK2()
print("r[0] data type: ", type(ping_pong.r[0]))
print("Final Position: ", ping_pong.r[-1])

ping_pong.save_data("test_output")
ping_pong.plot_data()

