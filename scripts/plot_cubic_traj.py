#!/usr/bin/env python3
import rospy
import numpy as np
from ar_week8_test.msg import cubic_traj_coeffs
from std_msgs.msg import Float32
# Initialize ROS node and subscribe to the cubic trajectory coefficients topic
def plot_cubic_traj():
    rospy.init_node('Plotter', anonymous=False)
    rospy.Subscriber("Coeffs", cubic_traj_coeffs, callback)
    rospy.spin()

def callback(data):
    # Generate time array
    t = np.linspace(data.t0, data.tf, 100)
    
    # Compute trajectories
    p_traj = data.a0 + data.a1 * t + data.a2 * t**2 + data.a3 * t**3
    v_traj = data.a1 + 2 * data.a2 * t + 3 * data.a3 * t**2
    a_traj = 2 * data.a2 + 6 * data.a3 * t

    # Publish trajectories and converts to float
    for p in p_traj:
        pos_pub.publish(Float32(p))
    
    for v in v_traj:
        vel_pub.publish(Float32(v))
    
    for a in a_traj:
        acc_pub.publish(Float32(a))
# Initialize publishers for position, velocity, and acceleration trajectories
if __name__ == '__main__':
    pos_pub = rospy.Publisher('position_trajectory', Float32, queue_size=10)
    vel_pub = rospy.Publisher('velocity_trajectory', Float32, queue_size=10)
    acc_pub = rospy.Publisher('acceleration_trajectory', Float32, queue_size=10)
    # Start plotting cubic trajectories
    try:
        plot_cubic_traj()
    except rospy.ROSInterruptException:
        pass
