#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published
## to the 'chatter' topic

import rospy
import rosbag
from tf_bag import BagTfTransformer
from std_msgs.msg import String
import numpy as np


def record():

    rospy.init_node('listener', anonymous=True)

    bag_transformer = BagTfTransformer('/home/mohamadi/snake_bot_files/Testbag.bag')

    times=bag_transformer.getTransformUpdateTimes('world', 'turtle2')
    t=np.array([])
    translations=[]
    while True:
        try:
            tmp_time=next(times)
            t=np.append(t,tmp_time.to_sec())
            rospy.loginfo(t[-1])
            translation=[]

            for i in range(2):
                target_frame='turtle'+str(i+1)
                translation_i, quaternion = bag_transformer.lookupTransform('turtle1', target_frame ,tmp_time )
                translation.append(translation_i)

            translations.append(translation)
        except StopIteration:
            break

    t=t-t[0]
    rospy.loginfo('last time is %.3f',t[-1])
    rospy.loginfo('lenght of time is: %i ' , len(t))

    #translations=np.array(translations)
    for tt in translations[::10]:
        #rospy.loginfo(bag_transformer.getTransformFrameTuples())
        rospy.loginfo(tt)
        #rospy.loginfo(translation)

    np.save('/home/mohamadi/snake_bot_files/recorded_poses.npy', [t, [translations]], allow_pickle=True)

    rospy.loginfo('The data is saved.')


if __name__ == '__main__':
    record()


























#
