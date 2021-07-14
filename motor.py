import threading
from ctypes import *
import RPi.GPIO as GPIO

timing = CDLL("./timing.so")

speed = 1800
duty = 10

servo = 17
servo_y = 18
loop_search = 0
cur_millis = 0
cur_micros = 0
pre_millis = 0
pre_micros = 0
move_state = 0
degree = 90
cycle = 0
cycle_y = 0
check_cnt_reset = 0
check_cnt = 0
check_cnt_y = 0
pre_millis_y = 0
pre_micros_y = 0
move_state_y = 0
degree_y = 90

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(servo_y, GPIO.OUT)

def check_degree():
  global degree
  if degree < 0:
    degree = 0
  elif degree > 180:
    degree = 180

def check_degree_y():
  global degree_y
  if degree_y < 80:
    degree_y = 80
  elif degree_y > 100:
    degree_y = 100

def set_loop_search(value):
  global loop_search
  loop_search = value
def search():
  state = 0
  explore_flag = 0
  global loop_search, cur_micros, cur_millis, cycle, degree, duty, pre_micros, pre_millis
  while (loop_search):
    cur_millis = timing.millis1()
    cur_micros = timing.micros1()
    check_degree()
    cycle = degree * duty
    if cur_micros > pre_micros + cycle + 600 and state == 0:
    
      pre_micros = cur_micros
      pre_millis = cur_millis
      GPIO.output(servo, GPIO.LOW)
      state = 1
    
    if cur_millis > pre_millis + 17 and state:
      pre_micros = cur_micros
      pre_millis = cur_millis
      state = 2

    
    if cur_micros > pre_micros + 2400 - cycle and state == 2:
    
      pre_micros = cur_micros
      pre_millis = cur_millis
      GPIO.output(servo, GPIO.HIGH)
      state = 0

      if explore_flag == 0:
        degree+=1
        if degree == 180:
          explore_flag = 1
      if explore_flag:
        degree-=1
        if degree == 0:
          explore_flag = 0
def reseting():
  state_reset = 0
  global degree, cycle, duty, cur_micros, cur_millis, pre_micros, pre_millis, check_cnt
  degree = 90
  cycle = degree * duty
  while check_cnt < 30:
    cur_millis = timing.millis1()
    cur_micros = timing.micros1()
    if cur_micros > pre_micros + 600 + cycle and state_reset == 0:
    
      pre_micros = cur_micros
      pre_millis = cur_millis
      GPIO.output(servo, GPIO.LOW)
      state_reset = 1
    
    if cur_millis > pre_millis + 17 and state_reset:
      pre_micros = cur_micros
      pre_millis = cur_millis
      state_reset = 2

    
    if cur_micros > pre_micros + 2400 - cycle and state_reset == 2:
    
      pre_micros = cur_micros
      pre_millis = cur_millis
      GPIO.output(servo, GPIO.HIGH)
      check_cnt+=1
      state_reset = 0

    
  
  check_cnt = 0



def position(x, y):
  x_dir = True
  y_dir = True

  if (x > 0) :
    x_dir = True

  
  elif (x < 0): 
    x_dir = False

  
  if (y > 0):
  
    y_dir = True

  
  elif (y < 0):
    y_dir = False

  x = abs(x)
  y = abs(y)
  moving (x, y, x_dir, y_dir)

def moving(x, y, x_dir, y_dir):

  motor(x, x_dir)
  motor_y(y, y_dir)

def motor(x, x_dir):
  state = 0
  global degree, cycle, duty, cur_micros, cur_millis, pre_micros, pre_millis, check_cnt
  if (x == 0):
    GPIO.output(servo, GPIO.LOW)
  else :
    if (x_dir == True):
      degree = degree + x / 10
    
    elif (x_dir == False):
      degree = degree - x / 10
    check_degree()
    cycle = degree * duty
    while check_cnt < 30:
      cur_millis = timing.millis1()
      cur_micros = timing.micros1()
      if (cur_micros > pre_micros + 600 + cycle and state == 0):
      
        pre_micros = cur_micros
        pre_millis = cur_millis
        GPIO.output(servo, GPIO.LOW)
        state = 1
      
      if (cur_millis > pre_millis + 17 and state) :
        pre_micros = cur_micros
        pre_millis = cur_millis
        state = 2
      if (cur_micros > pre_micros + 2400 - cycle and state == 2):
        pre_micros = cur_micros
        pre_millis = cur_millis
        GPIO.output(servo, GPIO.HIGH)
        check_cnt+=1
        state = 0
    check_cnt = 0

def motor_y(y, y_dir):
  state_y = 0
  global degree_y, cycle_y, duty, cur_micros, cur_millis, pre_micros_y, pre_millis_y, check_cnt_y
  if y == 0:
  
    GPIO.output(servo_y, GPIO.LOW)
  
  else:
    if y_dir == True:
    
      degree_y = degree_y + y / 10
    
    elif y_dir == False:
    
      degree_y = degree_y - y / 10
    
    check_degree_y()
    cycle_y = degree_y * duty
    while check_cnt_y < 30:
      cur_millis = timing.millis1()
      cur_micros = timing.micros1()
      if cur_micros > pre_micros_y + cycle_y + 600 and state_y == 0:
      
        pre_micros_y = cur_micros
        pre_millis_y = cur_millis
        GPIO.output(servo_y, GPIO.LOW)
        state_y = 1
      
      if cur_millis > pre_millis_y + 17 and state_y:
        pre_micros_y = cur_micros
        pre_millis_y = cur_millis
        state_y = 2

      
      if cur_micros > pre_micros_y + 2400 - cycle_y and state_y == 2:
      
        pre_micros_y = cur_micros
        pre_millis_y = cur_millis
        GPIO.output(servo_y, GPIO.HIGH)
        check_cnt_y+=1
        state_y = 0
      
    
    check_cnt_y = 0