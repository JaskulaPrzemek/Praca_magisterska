import csv
import math
v_dem = 195
leght_robot = 319
x_start  = 0 
y_start = 0
theta_start = 0
last_time = 0
ticksPerRev=16570/2
diameter=205
intMax=32767
intMin=-32768
EncINIT = False
prevEncL = 0
prevEncR = 0

def get_data(file_name):
    global last_time
    with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
            for row in reader:        
                delta_t = float(stampToTime(row['#time'])) - last_time
                calculate_pose(float(row['velR']),float(row['velL']),delta_t)
                last_time= stampToTime(row['#time']) 
    

def get_data_encoder(file_name):
    global last_time
    global EncINIT
    global prevEncL
    global prevEncR
    with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
            for row in reader:        
                delta_t = float(stampToTime(row['#time'])) - last_time
                if EncINIT:
                        deltaL=deltaEnc(prevEncL,float(row["posL"]))
                        deltaR=deltaEnc(prevEncR,float(row["posR"]))
                        velocity = vel_wheel(deltaL,deltaR)
                        calculate_pose(velocity[1],velocity[0],delta_t)
                        prevEncL=float(row["posL"])
                        prevEncR=float(row["posR"])
                          
                else:
            
                    prevEncL=float(row["posL"])
                    prevEncR=float(row["posR"])
                    EncINIT=True
                last_time= stampToTime(row['#time']) 
    



def calculate_pose(vR,vL,delta_t):
    global x_start 
    global y_start
    global theta_start
    
    v = (vR+vL)*0.5
    omega = (vR - vL)/ leght_robot
    theta_start = theta_start + omega*delta_t
    
    x_start = x_start + v*math.cos(theta_start)*delta_t
    y_start = y_start + v*math.sin(theta_start)*delta_t
    print("X pose = ", x_start)
    print("Y pose = ", y_start)
    print("theta_start", theta_start)


def vel_wheel(deltaL,deltaR):
    velL=deltaL/ticksPerRev*math.pi*diameter
    velR=deltaR/ticksPerRev*math.pi*diameter
    return [velL,velR]

    
    
def deltaEnc(Prev,Current):
    if Current>15000 and Prev<0:
        #z - na +
        deltaL=abs(Prev-intMin)
        deltaL=-deltaL-abs(Current-intMax)
    elif Current<-15000 and Prev>0:
        #z + na -
        deltaL=abs(Prev-intMax)
        deltaL=deltaL+abs(Current-intMin)
    else:
        deltaL=Current-Prev
    return deltaL


def stampToTime(stamp):
    x = stamp.split(":")
    return float(x[2])
    

if __name__ == '__main__':
    f1 = 'forward.csv'
    f6 = 'backward.csv'
    f2 = 'left_full_turn.csv'	
    f3 = 'right_full_turn.csv'
    f4 = 'square_left.csv'
    f5 = 'square_right.csv'
   # get_data(f5)
    get_data_encoder(f5)
