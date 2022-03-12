# Epitrochoid, epicycloid
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import matplotlib.patches as patches


def update_circle1_arm():
    global p1, p_arm, x_arm, y_arm, line_arm
    p1[0] = (r0 + r1) * np.cos(theta1)
    p1[1] = (r0 + r1) * np.sin(theta1)
    x_arm = p1[0] + r_arm * np.cos(theta_arm)
    y_arm = p1[1] + r_arm * np.sin(theta_arm)
    line_arm.set_data([p1[0], x_arm], [p1[1], y_arm])
    p_arm[0] = x_arm
    p_arm[1] = y_arm


def change_arm(value):
    global r_arm
    r_arm = float(value)
    update_circle1_arm()


def change_r1(value):
    global r1, circle1
    r1 = float(value)
    circle1.remove()
    circle1 = patches.Circle(xy=p1, radius=r1, fill=False, color='green')
    ax1.add_patch(circle1)
    update_circle1_arm()


def change_r0(value):
    global r0, circle0
    r0 = float(value)
    circle0.remove()
    circle0 = patches.Circle(xy=p0, radius=r0, fill=False, color='red')
    ax1.add_patch(circle0)
    update_circle1_arm()


def clear_curve():
    global cnt, x_curve, y_curve, curve, p1, circle1, theta1, theta_arm
    cnt = 0
    x_curve.clear()
    y_curve.clear()
    curve.set_data(x_curve, y_curve)
    p1[0] = r0 + r1
    p1[1] = 0.
    theta1 = theta1_init
    theta_arm = theta_arm_init
    circle1.set_center(p1)
    update_circle1_arm()


def switch():
    global is_running
    if is_running:
        is_running = False
    else:
        is_running = True


def update(f):
    global cnt, theta1, theta_arm, p1, x_arm, y_arm, line_arm, x_curve, y_curve, curve
    if is_running:
        tx_step.set_text(' Step=' + str(cnt))
        th = cnt / 10.
        theta_arm = theta_arm_init + th % (2 * np.pi)
        theta1 = theta1_init + (th * r1 / (r0 + r1)) % (2 * np.pi)
        update_circle1_arm()
        x_curve.append(x_arm)
        y_curve.append(y_arm)
        curve.set_data(x_curve, y_curve)
        cnt += 1
        if th > 10000:
            cnt = 0
            x_curve.clear()
            y_curve.clear()


# Global variables
is_running = False

x_min = -8.
x_max = 8.
y_min = -8.
y_max = 8.

cnt = 0

num_of_points = 500

r0 = 1.
r1 = 1.
r_arm = r1
p0 = np.array([0., 0.])
p1 = np.array([r0 + r1, 0.])
p_arm = np.array([p1[0] - r_arm, 0.])

theta1_init = 0.
theta1 = theta1_init
theta_arm_init = - np.pi
theta_arm = theta_arm_init

x_curve = []
y_curve = []

# Generate figure and axes
fig = Figure()
ax1 = fig.add_subplot(111)
ax1.grid()
ax1.set_title('Epitrochoid, epicycloid')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
ax1.set_aspect("equal")

# Generate items
tx_step = ax1.text(x_min, y_max * 0.9, " Step=" + str(0))
circle0 = patches.Circle(xy=p0, radius=r0, fill=False, color='red')
ax1.add_patch(circle0)
circle1 = patches.Circle(xy=p1, radius=r1, fill=False, color='green')
ax1.add_patch(circle1)

x_arm = p1[0] + np.cos(theta_arm)
y_arm = p1[1] + np.sin(theta_arm)
line_arm, = ax1.plot([p1[0], x_arm], [p1[1], y_arm], color='green')
p_arm[0] = x_arm
p_arm[1] = y_arm
circle_arm = patches.Circle(xy=p_arm, radius=r1*0.1, color='green')
ax1.add_patch(circle_arm)

curve, = ax1.plot(x_curve, y_curve)

# Embed in Tkinter
root = tk.Tk()
root.title("Trochoid, cycloid")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

label_r0 = tk.Label(root, text="Radius 0")
label_r0.pack(side='left')
var_r0 = tk.StringVar(root)  # variable for spinbox-value
var_r0.set(r0)  # Initial value
s_r0 = tk.Spinbox(
    root, textvariable=var_r0, format="%.1f", from_=0.1, to=4, increment=0.1,
    command=lambda: change_r0(var_r0.get()), width=5
    )
s_r0.pack(side='left')

label_r1 = tk.Label(root, text=", Radius 1")
label_r1.pack(side='left')
var_r1 = tk.StringVar(root)  # variable for spinbox-value
var_r1.set(r1)  # Initial value
s_r1 = tk.Spinbox(
    root, textvariable=var_r1, format="%.1f", from_=0.1, to=4, increment=0.1,
    command=lambda: change_r1(var_r1.get()), width=5
    )
s_r1.pack(side='left')

label_arm = tk.Label(root, text=", Length of arm")
label_arm.pack(side='left')
var_arm = tk.StringVar(root)  # variable for spinbox-value
var_arm.set(r_arm)  # Initial value
s_arm = tk.Spinbox(
    root, textvariable=var_arm, format="%.1f", from_=0.1, to=4, increment=0.1,
    command=lambda: change_arm(var_arm.get()), width=5
    )
s_arm.pack(side='left')

btn = tk.Button(root, text="Play/Pause", command=switch)
btn.pack(side='left')

btn = tk.Button(root, text="Clear", command=clear_curve)
btn.pack(side='left')


# main loop
anim = animation.FuncAnimation(fig, update, interval=50)
root.mainloop()
