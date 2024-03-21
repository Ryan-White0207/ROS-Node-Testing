#!/usr/bin/env python3

import rospy
import numpy as np
from ar_week8_test.srv import compute_cubic_traj, compute_cubic_trajResponse

def handle_compute_cubic_traj(req):
    # Construct the coefficient matrix M
    tim = np.array([[1, req.t0, req.t0**2, req.t0**3],
                    [0, 1, 2*req.t0, 3*req.t0**2],
                    [1, req.tf, req.tf**2, req.tf**3],
                    [0, 1, 2*req.tf, 3*req.tf**2]])
    pos = np.array([[req.p0],
                    [req.pf],
                    [req.v0],
                    [req.vf]])

    # Solve for the coefficients
    weights = np.linalg.inv(tim) @ pos
    
    # Extract coefficients a0, a1, a2, a3 from the solution
    a0, a1, a2, a3 = weights.flatten()
    
    # Return the response with the computed coefficients
    return compute_cubic_trajResponse(a0, a1, a2, a3)
# Initialize the ROS node and create a service to compute cubic trajectory coefficients
def compute_cubic_coeffs_server():
    rospy.init_node('Computer')
    s = rospy.Service('compute_cubic_traj', compute_cubic_traj, handle_compute_cubic_traj)
    print("Ready to compute cubic trajectory coefficients.")
    rospy.spin()
# Start the server for computing cubic trajectory coefficient
if __name__ == "__main__":
    compute_cubic_coeffs_server()
