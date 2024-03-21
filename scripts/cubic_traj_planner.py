#!/usr/bin/env python3
import rospy
from ar_week8_test.msg import cubic_traj_params, cubic_traj_coeffs
from ar_week8_test.srv import compute_cubic_traj
    #initialize the ros node and subscripe to the params topic
def cubic_traj_planner():
    rospy.init_node('Planner', anonymous=False)
    rospy.Subscriber("Params", cubic_traj_params, callback)
    rospy.spin()

def callback(data):
    # Call the service to compute coefficients

    rospy.wait_for_service('compute_cubic_traj')
    try:
        compute_cubic_traj_service = rospy.ServiceProxy('compute_cubic_traj', compute_cubic_traj)
        
        # Create a request message
        request = compute_cubic_traj_service(data.p0, data.pf, data.v0, data.vf, data.t0, data.tf)

        rospy.loginfo("Coefficients: a0=%f, a1=%f, a2=%f, a3=%f, t0=%f, tf=%f", request.a0, request.a1, request.a2, request.a3, data.t0, data.tf)

        # Publish coefficients
        coeffs_msg = cubic_traj_coeffs()
        coeffs_msg.a0, coeffs_msg.a1, coeffs_msg.a2, coeffs_msg.a3 = request.a0, request.a1, request.a2, request.a3
        coeffs_msg.t0 = data.t0
        coeffs_msg.tf = data.tf
        coeffs_pub.publish(coeffs_msg)
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)


#initialize the publisher for Coeffs topic
if __name__ == '__main__':
    coeffs_pub = rospy.Publisher('Coeffs', cubic_traj_coeffs, queue_size=10)
    cubic_traj_planner()
