from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import os

class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline(x = x[0],color='k', alpha=0.2)  # the vert line
        self.marker, = ax.plot(x[0],0,marker="o", color="crimson", zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = event.xdata, event.ydata
        indx = np.searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        self.ly.set_xdata(x)
        self.marker.set_data([x],[y])
        self.txt.set_text('y=%1.5fmm' % (y))
        self.txt.set_position((x,y))
        self.ax.figure.canvas.draw_idle()

time = list()
horizontalEncoder = list()
verticalEncoder = list()
diff = list()

file = open(f'{os.path.dirname(__file__)}/data.csv','r')

screwPitch = 2.0
displacementPerRev   = 0.230

verticalEncoderRes   = 0.000023
horizontalEncoderResRaw = 0.000368

# screwPitch / horizontal resolution = counts per jack screw rev (230um)
horizontalEncoderRes = displacementPerRev/(screwPitch/horizontalEncoderResRaw)

print(f'{horizontalEncoderRes:.6f}')

for line in file.readlines():
    time.append(float(line.split(',')[0]))
    horizontalEncoder.append(float(line.split(',')[1])*horizontalEncoderRes)
    verticalEncoder.append((float(line.split(',')[2])*-1.0)*verticalEncoderRes)
    diff.append(horizontalEncoder[-1]-verticalEncoder[-1])


fig, ax = plt.subplots()
ax2 = ax.twinx()

c1 = SnaptoCursor(ax, time, horizontalEncoder)
c2 = SnaptoCursor(ax, time, verticalEncoder)
c3 = SnaptoCursor(ax2, time, diff)
cid =  plt.connect('motion_notify_event', c1.mouse_move)
cid =  plt.connect('motion_notify_event', c2.mouse_move)
cid =  plt.connect('motion_notify_event', c3.mouse_move)

ax.plot(time,horizontalEncoder,color="blue",label='AT3018 (Horizontal) mm')
ax.plot(time,verticalEncoder,color="red",label='AT1218 (Vertical) mm')
ax.set_ylabel("Encoders (mm)")
ax.legend(loc = "upper left")

plt.xlabel("Time")

ax2.plot(time,diff,color="green",label='Difference')
ax2.set_ylabel("Difference (mm)")
ax2.legend(loc = "upper right")
#plt.legend()
plt.show()