import Doll
import socket
import math
d = Doll.doll()
d.set()
address = ('192.168.31.56',6000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)


def doll_set_by_big_console(d_num):
    l_eye_x=0
    l_eye_y=1
    r_eye_x=2
    r_eye_y=3
    l_ear_angle=4
    r_ear_angle=5
    l_bow_angle=6
    l_bow_y =7
    r_bow_angle=8
    r_bow_y=9
    c_mouth_angle = 10
    l_mouth_angle=11
    r_mouth_angle=12


    d.l_ear.angle = (d_num[l_ear_angle]-512)/1024*68 - 5
    d.r_ear.angle = (d_num[r_ear_angle]-512)/1024*68 - 24

    d.l_bow.y=(d_num[l_bow_y]-512)/512*11-10
    d.r_bow.y=(d_num[r_bow_y]-512)/512*11-9
    d.l_bow.angle=(d_num[l_bow_angle]-512)/512*30
    d.r_bow.angle=(d_num[r_bow_angle]-512)/512*30

    eye_x=(d_num[l_eye_x]-511)/1.2
    eye_y=(d_num[l_eye_y]-511)/1.2
    eye_r = math.sqrt(pow(eye_x,2) + pow(eye_y,2) )
    eye_angle=math.degrees(math.atan2(eye_y,eye_x))
    d.l_eye.r = eye_r
    d.l_eye.angle= eye_angle

    eye_x=(d_num[r_eye_x]-511)/1.2
    eye_y=(d_num[r_eye_y]-511)/1.2
    eye_r = math.sqrt(pow(eye_x,2) + pow(eye_y,2) )
    eye_angle=math.degrees(math.atan2(eye_y,eye_x))
    d.r_eye.r = eye_r
    d.r_eye.angle= eye_angle

    d.l_mouth.angle=(d_num[l_mouth_angle])*50/1024
    d.r_mouth.angle=(d_num[r_mouth_angle])*50/1024
    if d_num[c_mouth_angle]== 1:
        d.c_mouth.angle=0
    else:
        d.c_mouth.angle =65

    d.set()


while 1:
    print("waiting the data come")
    data, addr = s.recvfrom(2048)
    if not data:
        print "client has exist"
        break
    print "received:", data, "from", addr
    num = data.split(",")
    num = map(float,num)
    if len(num) == 13:
        doll_set_by_big_console(num)

s.close()