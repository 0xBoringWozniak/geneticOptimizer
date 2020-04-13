import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.animation as animation
from matplotlib.ticker import LinearLocator, FormatStrFormatter





import sys, os
sys.path.append(os.path.abspath('../'))

from function import Func


pathdrct = os.path.abspath('./')
data = pd.concat([pd.read_csv(pathdrct + '/chromosomes_{}.csv'.format(i + 1), index_col=0) for i in range(20)], ignore_index=True)
data['time'] = [i for i in range(160)]




def update_graph(num):
    df=data[data['time'] <= num]
    graph.set_data (np.array(df['x']), np.array(df['y']))
    graph.set_3d_properties(np.array(df['f(x, y)']))
    title.set_text('3D Test, time={}'.format(num))
    return title, graph, 


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# Make data.
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)
f_x_y = '(x ** 1/2 - 5 * y ) / (x ** 2 + y ** 2  - 2 * x + 10)'
f = Func(f_x_y)
Z = f(X, Y)


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
# ax.scatter(data['x'], data['y'], data['f(x, y)'], marker='^', c=np.arange(160))


title = ax.set_title('3D GA optimizer')

df = data[data['time'] == 0]
graph, = ax.plot(np.array(df['x']), np.array(df['y']), np.array(df['f(x, y)']), linestyle="", marker="X", c='black')

ani = animation.FuncAnimation(fig, update_graph, 159, interval=8,  save_count=True)


# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.8, aspect=3)


plt.show()