#On PC
#python mavlink_Test.py --console --map --out=<ipRaspberryPi>:14550
#On Pi
#sudo mavproxy.py --master=udpin:0.0.0.0:14550
#this starts Mavproxy and sending of UDP packets

#fot this run: python mavlink_test.py

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import time

# Connect to the Vehicle (in this case a UDP endpoint)
vehicle = connect('127.0.0.1:14550', wait_ready=True)

#for RaspPi:
#vehicle = connect('/dev/ttyAMA0', wait_ready = True, baud = 57600)
#SITL connected to the vehicle via UDP as target address

#start SITL if no connection string is given
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

#pymavlink with DroneKit API. simple arming test for 5 seconds

print "Arming motors:"
vehicle.mode  = VehicleMode("GUIDED")
vehicle.armed = True
while not vehicle.mode.name=='GUIDED' and not vehicle.armed:
        print " Getting ready for takeoff.."
        time.sleep(1)
print "Keeping motors armed for 5s"
time.sleep(5)
print "Disarming"
vehicle.armed = False #disarm vehicle
time.sleep(1)

vehicle.armed = True #re-armed
#simple take-off
if vehicle.armed == False:
    print "wait until armed"

print "--Ready for flight--"
vehicle.simple_takeoff(15)
vehicle.airspeed = 10 #m/s
vehicle.simple_goto(LocationGlobal(-32.8,152.1))
time.sleep(10)
vehicle.mode = VehicleMode("LOITER")

#control servo test
#sending MAVLINK commands to simulated drone
msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target_system, target_component (target_component is set to 0)
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    1,         # param 1, servo number
    1100,          # param 2, PWM (1000-2000)
    0, 0, 0, 0, 0) # param 3 ~ 7 not used
#send command to vehicle
vehicle.send_mavlink(msg)
time.sleep(2)

msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    2,         # param 1, servo number
    1500,          # param 2, PWM (1000-2000)
    0, 0, 0, 0, 0) # param 3 ~ 7 not used
#send command to vehicle
vehicle.send_mavlink(msg)
time.sleep(2)

msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    3,         # param 1, servo number
    1750,          # param 2, PWM (1000-2000)
    0, 0, 0, 0, 0) # param 3 ~ 7 not used
#send command to vehicle
vehicle.send_mavlink(msg)
time.sleep(2)

#Raspberry Pi Camera = (import dronekit, opencv etc into script)
#connect Pixhawk to RaspberryPi (usb to usb not by serial)
#verified by Mavlink (sudo -s mavproxy.py) then not needed
#run script with openCV in IDLE 2.0

'''
msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE, #command
    0, # confirmation
    0, # param 1, reserved
    1, # param 2, duration between consecutive pictures
    5, # param 3, number of images to capture
    0)
vehicle.send_mavlink(msg)

msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target_system, target_component
    mavutil.mavlink.MAV_CMD_IMAGE_STOP_CAPTURE, #command
    0, # confirmation
    0, # param 1, reserved
    0)
vehicle.send_mavlink(msg)
'''

#Create a message listener
#self = current vehicle
#name = name of message that was intercepted
#message = actual message

#@vehicle.n_message('ATTITUDE')
#def listener(self, name, message):
#    print 'pitch: %s' % message.pitch
#    print 'yaw: %s' % message.yaw
#    print 'roll: %s' %message.roll

#listener for battery
@vehicle.on_message('BATTERY')
def listener(self,name,message):
    print 'voltage: %s' %message.voltage
    print 'current: %s' %message.current

@vehicle.on_message('RAW_IMU')
def listener(self,name,message):
    print message #all 9 DOF

vehicle.mode = VehicleModel("LAND")
vehicle.armed = False

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

