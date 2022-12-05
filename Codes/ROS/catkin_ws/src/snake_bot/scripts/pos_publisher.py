#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Float32MultiArray
from std_msgs.msg import Int64, Int16,Int16MultiArray,MultiArrayLayout,MultiArrayDimension
import numpy as np
import pickle
import sys, select, termios, tty
from threading import Thread
from time import sleep

#from pos_publisher_functions import initialize, encoder_sub_cb, control,pos_publish, getKey

pre_rec_poses=[]
#pos_cmd_pub = rospy.Publisher('pos_cmd', Int16MultiArray, queue_size=10)
pos_cmd_pub = rospy.Publisher('pos_cmd', Int16, queue_size=10)
move_pub=rospy.Publisher('move_cmd', Int16, queue_size=10)

global SERVO_MAX
SERVO_MAX= 498
settings = termios.tcgetattr(sys.stdin)
global base_loc
base_loc=0
global base_locs
base_loc=-915
global speed
speed=150
#pre recorded base loacations

def initialize():
    global pre_rec_poses
    global base_locs
    rospy.init_node('pos_publisher', anonymous=True)

    with open('/home/mohamadi/snake_bot_files/pre_rec_poses.pkl', 'rb') as infile:
        pre_rec_poses =pickle.load(infile)
        pre_rec_poses =pre_rec_poses[0]
        base_locs=np.zeros(len(pre_rec_poses))

    poses=np.zeros((len(pre_rec_poses),6))
    for i in range(len(pre_rec_poses)):
        base_locs[i]=pre_rec_poses[i][0]
        for j in range(6):
            poses[i,j]=np.rad2deg(pre_rec_poses[i][1][j])
    poses=np.rint(fmap(poses,-180,180, -SERVO_MAX, SERVO_MAX))
    pos_cmd_msg=Int16MultiArray()

    """
    pos_cmd_msg.layout.dim=[MultiArrayDimension(), MultiArrayDimension()]
    pos_cmd_msg.layout.dim[0].size=len(pre_rec_poses)
    pos_cmd_msg.layout.dim[0].stride=len(pre_rec_poses)
    pos_cmd_msg.layout.dim[1].size=6
    pos_cmd_msg.layout.dim[0].stride=6

    pos_cmd_msg.data=poses.reshape([len(pre_rec_poses)*6])
    pos_cmd_pub.publish(pos_cmd_msg)
    """
    rospy.loginfo("length %i lkdjf" % len(pre_rec_poses))
    rospy.loginfo(poses)
    rospy.loginfo(pre_rec_poses[0][0])
    rospy.loginfo(pre_rec_poses[0][1])
    rospy.loginfo(pre_rec_poses[0][1][5])

def encoder_sub_cb(data):
    global base_loc
    tmp=data.data*1.1875-915
    base_loc=np.clip(tmp,np.min(base_locs), np.max(base_locs))

def control():
    global base_loc
    global speed
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "\n Time: %s \n Base Location: %.2f mm \n \
        Move Speed: %i \n" % (rospy.get_time(), base_loc, speed)
        rospy.loginfo(hello_str)
        key=getKey()

        if key=='w':
            move_pub.publish(+11)
        elif key=="s":
            move_pub.publish(-11)

        elif (key=="q"):
            speed=min(speed+10,500)
            move_pub.publish(speed)
        elif (key=="a") & (speed > 0):
            speed=speed-10
            move_pub.publish(speed)
        elif key=="\x03":
            rospy.signal_shutdown('Bye Bye')
        else:
            move_pub.publish(0)

        rate.sleep()

def pos_publish():
    global SERVO_MAX
    global base_locs
    global base_loc

    rate = rospy.Rate(5)
    #pos_cmd=Int16MultiArray()
    pos_cmd=Int16()
    while not rospy.is_shutdown():
        int_base_loc=np.int(np.rint(base_loc)+915)
        #k,=np.where(base_locs==int_base_loc)
        pos_deg=np.rad2deg(pre_rec_poses[int_base_loc][1])
        pos_servo=fmap(pos_deg,-180,180, -SERVO_MAX, SERVO_MAX)
        pos_servo=np.rint(pos_servo)
        pos_cmd.data =500
        pos_cmd_pub.publish(pos_cmd)
        pos_cmd_pub.publish(pos_cmd)
        for i in range(6):
            sleep(0.01)
            pos_cmd.data=pos_servo[i]
            pos_cmd_pub.publish(pos_cmd)
        rate.sleep()

def fmap(x, x1, x2, y1, y2):
    return((x-x1)*(y2-y1)/(x2-x1)+y1)

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key



rospy.Subscriber('encoder_pos', Int16, encoder_sub_cb)

if __name__ == '__main__':
    initialize()
    Thread(target=pos_publish).start()
    try:
        control()
    except rospy.ROSInterruptException:
        pass
