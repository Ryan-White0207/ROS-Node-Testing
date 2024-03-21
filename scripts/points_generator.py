#!/usr/bin/env python3
import random
import rospy
from ar_week8_test.msg import cubic_traj_params

def points_generator():
    # Initialize ROS node and publisher
    pub = rospy.Publisher('Params', cubic_traj_params, queue_size=10)
    rospy.init_node('Generator', anonymous=False)
    rate = rospy.Rate(0.05) # 20 seconds
    # Define maximum values for position and velocity
    P_MAX = 10
    V_MAX = 10
    # Generate random parameters and publish them
    while not rospy.is_shutdown():
        p0 = random.uniform(-P_MAX, P_MAX)
        pf = random.uniform(-P_MAX, P_MAX)
        v0 = random.uniform(-V_MAX, V_MAX)
        vf = random.uniform(-V_MAX, V_MAX)
        t0 = 0
        tf = t0 + random.uniform(5, 10)
        hello_str = cubic_traj_params(p0=p0, pf=pf, v0=v0, vf=vf, t0=t0, tf=tf)
        # Log the generated parameters
        rospy.loginfo("p0: %f, pf: %f, v0: %f, vf: %f, t0: %f, tf: %f", hello_str.p0, hello_str.pf, hello_str.v0, hello_str.vf, hello_str.t0, hello_str.tf)
        params = cubic_traj_params(p0, pf, v0, vf, t0, tf)
        pub.publish(params)
        # Sleep according to the defined rate
        rate.sleep()

if __name__ == '__main__':
    try:
        points_generator()
    except rospy.ROSInterruptException:
        pass
