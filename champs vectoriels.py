import matplotlib.pyplot as plt
import numpy as np

X = np.arange(-20, 20.1, 10)
Y = np.arange(-20, 20.1, 10)
U, V = np.meshgrid(-X, -Y)


fig, ax = plt.subplots()
ax.axis([0, 640, 0, 480])

q = ax.quiver(X+160, Y+240, U, V)
q = ax.quiver(X+430, Y+240, U, V)
crane_center = plt.Circle((315, 245, 40))
crane_sweeping_range = plt.Circle((315, 245), 200, fill=False)
ax.add_artist(crane_center)
ax.add_artist(crane_sweeping_range)

plt.show()
