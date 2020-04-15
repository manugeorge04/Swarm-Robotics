#Libraries
import RPi.GPIO as GPIO
import time
import pigpio
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Ultrasonic
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 3
ECHO = 4
maxTime = 0.04
minDistance = 27

#Servo
pi = pigpio.pi()
pi.set_mode(2, pigpio.OUTPUT)
pi.get_mode(2)

#Motors
#MotorA
in1 = 9
in2 = 10
enA = 11

#MotorB
in3 = 22
in4 = 27
enB = 17

#MotorC
in5 = 24
in6 = 23
enC = 25

#MotorD
in7 = 18
in8 = 15
enD = 14

#Motors
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.setup(in5,GPIO.OUT)
GPIO.setup(in6,GPIO.OUT)
GPIO.setup(enC,GPIO.OUT)
GPIO.setup(in7,GPIO.OUT)
GPIO.setup(in8,GPIO.OUT)
GPIO.setup(enD,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(in5,GPIO.LOW)
GPIO.output(in6,GPIO.LOW)
GPIO.output(in7,GPIO.LOW)
GPIO.output(in8,GPIO.LOW)

pA=GPIO.PWM(enA,100)
pB=GPIO.PWM(enB,100)
pC=GPIO.PWM(enC,100)
pD=GPIO.PWM(enD,100)

pA.start(100)
pB.start(100)
pC.start(100)
pD.start(100)


def goForward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.HIGH)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.HIGH)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)


def goBack():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.HIGH)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.LOW)
    GPIO.output(in8,GPIO.HIGH)
    GPIO.output(enD,GPIO.HIGH)

def goLeft():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.HIGH)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)

def goRight():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.HIGH)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.LOW)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)



def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.LOW)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)

def getDistance():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG,False)

    time.sleep(0.01)

    GPIO.output(TRIG,True)

    time.sleep(0.00001)

    GPIO.output(TRIG,False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(ECHO) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)

    return distance


if __name__ == '__main__':

    pi.set_servo_pulsewidth(2, 1500)  #mid
    pi.get_servo_pulsewidth(2)
    time.sleep(2)
   
    while True:
        distance = getDistance()
        #print("distance = ",distance)
        if( distance <= minDistance):
            stop()
            print("stop")
            goBack()
            time.sleep(0.5)
            stop()
            time.sleep(0.5)
            maxDistLeft = 0
            maxDistRight = 0

            time.sleep(0.5)           

            pi.set_servo_pulsewidth(2, 500)  #right
            pi.get_servo_pulsewidth(2)
            time.sleep(2)

            maxDistRight = getDistance()
            print("Right = ",maxDistRight)

            pi.set_servo_pulsewidth(2, 1500)  #mid
            pi.get_servo_pulsewidth(2)
            time.sleep(2)
   
            pi.set_servo_pulsewidth(2, 2500) #left
            pi.get_servo_pulsewidth(2)
            time.sleep(2)

            pi.set_servo_pulsewidth(2, 1500)  #mid
            pi.get_servo_pulsewidth(2)
            time.sleep(2)


            maxDistLeft = getDistance()
            print("left = ",maxDistLeft)
            
            if (maxDistLeft <=20 and maxDistRight <= 20):
                goBack()
                time.sleep(0.5)


            elif(maxDistLeft <= maxDistRight):
                goRight()
                time.sleep(1.4)

            else:
                goLeft()
                time.sleep(1.4)
        
        else:
            print("moving Forward")
            goForward()