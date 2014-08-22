#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8
import shlex,subprocess,os
import simplejson
cmd1='sox -r 16000 -t alsa default recording.flac silence 1 0.1 1% 1 1.5 1%'
cmd2='wget -q -U "Mozilla/5.0" --post-file recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyA4j0NkPDfPMNKjHSD6vk7h93Gne1t9lfQ"'


def speech():
    print "Initializing node 'itf_listen'"
    rospy.init_node('itf_listen')
    pubs = rospy.Publisher('itf_listen', String)
    pubc = rospy.Publisher('confidence', Int8)

    args2 = shlex.split(cmd2)

    print "Start recording"
    os.system('sox -r 16000 -t alsa default recording.flac silence 1 0.1 1% 1 1.5 1%')

    print "Posting file to Google..."
    output,error = subprocess.Popen(args2,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()

    output = output.replace('{"result":[]}', '')

    if not error and len(output)>39:
        jsonobj = simplejson.loads(output)

        print "New output is " + output + ": end"

        alternatives = jsonobj['result'][0]['alternative']

        indexer = 0

        for lol in alternatives:
            confidence = -1
            try:
                confidence = alternatives[indexer]['confidence']
            except:
                pass

            if (confidence >= 0):
                print "Number " + str(indexer) + " is " + alternatives[indexer]['transcript'] + ", confidence is " + str(confidence)
                pubs.publish(alternatives[indexer]['transcript'])
                pubc.publish(confidence)
            else:
                print "Number " + str(indexer) + " is " + alternatives[indexer]['transcript']

            indexer += 1
    else:
        print "*** Recognition failed ***"
        pubs.publish("BADINPUT")

    print ""
    print "---------------------------------------------"
    print ""

    speech()


if __name__ == '__main__':
    try:
        speech()
    except rospy.ROSInterruptException: pass
    except KeyboardInterrupt:
        sys.exit(1)
   
