import pygame
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
#hypothese : choc elastique , modele SEIR
ball_radius=5 #ballsize ca signifie la diffusion plus large plus diffuse
quantity=200 #number of balls ca signfie la densité de population dans un certaine region
initial_infect=100 #number of initial infected number 

dr =  0.1 # the rate of death
ht_mean = 500*10 # the mean time of the healing
ht_var = 100   # the ecart type  of the healing time
cr = 0.8     #the rate of contagion
ip_mean = 500*10  # the mean time of incubation period 
ip_var = 100    #the ecart type of the incubation period 
ir = 0.6*0.1   #the rate of infection
cra = 0 # the rate of confinement

def death():#taux de mortalité, mais retourner 0 ou 1 ca signifie mort ou pas 
    if (random.random()< 1 - math.pow(1-dr,1/ht_mean)): return 1 # pendant le temps de guésion , taux de mortalite a chaque instant t0 
    else : return 0
def confinement():#taux de confinement, mais retourner 0 ou 1 ca signifie confine ou pas 
    # pendant le temps de guésion , taux de confinement a chaque instant t0 

    if (random.random()< cra): return 1
    else : return 0

def healing_time():#temps de guérison qui suis loi de gausiennne
    return round (ht_mean + ht_var*(math.sqrt(-2*math.log(random.random()))*math.cos(2*math.pi*random.random())))

def incubation_period():#période de incubation qui suis loi de gausiennne
    return round (ip_mean + ip_var*(math.sqrt(-2*math.log(random.random()))*math.cos(2*math.pi*random.random())))
def contagion():# La probabilité qu'une personne infectée devienne une personne sont contagieuse , taux de incubation a chaque instant
      
    if (random.random()< 1 - math.pow(1-cr,1/ip_mean)): return 1
    else : return 0
def infection():#La probabilité qu'une personne en bonne santé soit infectée,mais retourner 0 ou 1 signifie infecte ou pas, taux de transmision
    if (random.random()< 1-math.pow(1-ir,1/((8*ball_radius)/(speed*math.pi)+1))): return 1
    else : return 0


def dist(pos1,pos2): #distance between two balls
    result = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] -pos2[1])**2)
    return result

def module(pos1):# distance of the ball from (0,0)
    result = math.sqrt(pos1[0]**2 + pos1[1]**2)
    return result
def partition(arr, low, high):
    i = low
    j = high         # index of smaller element
    pivot = module(arr[high])     # pivot
    
    while i <=j :
        while module(arr[i]) < pivot and i<= high :
            i += 1
        while module(arr[j]) >= pivot and j>= low:
            j -= 1 
        if i<j :
            arr[i], arr[j] = arr[j], arr[i]
            i = i+1
            j= j-1
      
    tem =arr[i]
    arr[i]=arr[high] 
    arr[high]= tem
    return i
def quick_sort(arr, low, high):
    if low  >= high:
        return arr
    if low < high:
 
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)
 
        # Separately sort elements before
        # partition and after partition
        quick_sort(arr, low, pi-1)
        quick_sort(arr, pi+1, high)
        return arr
def elastic_collision(liste):#liste is already sorted and we will take the elastic collision in count
      
    for i in range(quantity):
        if liste[i][4] != status[4]  and liste[i][0] < width - ball_radius and liste[i][0] > ball_radius and liste[i][1] < height-ball_radius and liste[i][1] > ball_radius :# don't collide with dead one :when the ball bumps into the wall don't collide with other ball

                j=1
                while (i+j<len(liste) and (liste[i][4] == status[4] or dist(liste[i], liste[i+j]) > ball_radius*2) ) :
                    j=j+1
            
                if i+j < len(liste):
                     #cut off the repeat area ,rectify the position
                    while i+j < len(liste) and dist(liste[i], liste[i+j]) <= ball_radius*2:
                        liste[i+j][0] -= liste[i+j][2]      #move the ball
                        liste[i+j][1] -= liste[i+j][3]

                    liste[i][2] ,liste[i+j][2] = liste[i+j][2] , liste[i][2]#swap speed with nearest ball
                    liste[i][3] ,liste[i+j][3] = liste[i+j][3] , liste[i][3]
                    #cut off the repeat area ,rectify the position
                    while i+j < len(liste):
                        while  dist(liste[i], liste[i+j]) <= ball_radius*2:
                            liste[i+j][0] -= liste[i+j][2]      #move the ball
                            liste[i+j][1] -= liste[i+j][3]
                        j+=1

    return liste

def change_status(liste):

    quick_sort(liste,0,len(liste)-1)#sorting
    elastic_collision(liste)

    for i in range(quantity):

        if liste[i][4] == status[1] :# case infect mais non contagious 
            if contagion()==1 :

                liste[i][4] = status[2]
                liste[i][5] = healing_time()

                if confinement() == 1: 
                    liste[i][4] = status[5]
                    liste[i][2] = 0
                    liste[i][3] = 0
                                   
                    
            else : 
                liste[i][5] -= 1
                if liste[i][5] <= 0 : liste[i][4] = status[3]
                   
        if liste[i][4] == status[5] :# case confinement contagious

            if death() == 1:
                liste[i][4] = status[4]
                liste[i][5] = 0 
            else:
                liste[i][5] -=1
                if liste[i][5] <= 0 : liste[i][4] = status[3] 
            
        if liste[i][4] == status[2] : #case contagious

            if death() ==1:
                liste[i][4] = status[4] #case death
                liste[i][2] = 0
                liste[i][3] = 0
                liste[i][5] = 0 
            else:
                liste[i][5] -=1
                if liste[i][5] <= 0 : liste[i][4] = status[3]     #case heal 
                else:
                    j=0
                    for j in range (quantity):
                        if i!=j and dist(liste[i], liste[j]) < ball_radius and liste[j][4] == status[0] and  infection() == 1:# infect other balls
                            liste[j][4] = status[1]
                            liste[j][5] = incubation_period()

        
        if liste[i][0] >= width - ball_radius or liste[i][0] <= ball_radius :    #boundary condition

            #cut off the repeat area ,rectify the position while choc elastique
            #if  liste[i][0] >= width - ball_radius or liste[i][0] <= ball_radius:
            #    liste[i][0] -= liste[i][2] 
            #    liste[i][1] -= liste[i][3] 



            liste[i][2] = -liste[i][2]

        if liste[i][1] >= height-ball_radius or liste[i][1] <= ball_radius :
            #cut off the repeat area ,rectify the position while choc elastique
            #if  liste[i][1] >= height-ball_radius or liste[i][1] <= ball_radius:
            #   liste[i][1] -= liste[i][3]
            #   liste[i][0] -= liste[i][2]   
        

            liste[i][3] = -liste[i][3]
         
        liste[i][0]+=liste[i][2]      #move the ball
        liste[i][1]+=liste[i][3] 
                

    
    
    return liste

def statistic(liste,data):#registry the data to scatter
    i1,i2,i3,i4,i5=0,0,0,0,0
    for i in range (quantity):
        if liste[i][4] == status[0]: i1+=1
        elif liste[i][4] == status[1]:i2+=1
        elif liste[i][4] == status[2]:i3+=1
        elif liste[i][4] == status[3]:i4+=1
        elif liste[i][4] == status[4]:i5+=1
        elif liste[i][4] == status[5]:i3+=1
    
    data[0].append(i1)
    data[1].append(i2)
    data[2].append(i3)
    data[3].append(i4)
    data[4].append(i5)


    return data

pygame.init()
size = width,height= 800,600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("multiballsbouncing")

speed = 2 #ball speed magnitude
bg=(255,255,255) #whiteboard
ball_color_red=(255,0,0) #redball
ball_color_reddark=(100,0,0)
ball_color_black=(0,0,0)
ball_color_blue=(0,0,255)
ball_color_green=(0,255,0)
ball_color_grey=(150,150,150)
status = (ball_color_grey,ball_color_blue,ball_color_red,ball_color_green,ball_color_black,ball_color_reddark)

temps =0
balls=[] 
time_list= [0]

data=[]
#initial position
for i in range(quantity):

    while True :#two ball don't have same initial position
        pos_x = random.randint(0+ball_radius, width-ball_radius)
        pos_y = random.randint(0+ball_radius, height-ball_radius)#initialize position
        j =1 
        while i-j>=0 and dist( balls[i-j],[pos_x,pos_y]) > ball_radius*2 :
            j=j+1
        if i-j == -1 and pos_x != ball_radius and pos_x != 1200-ball_radius and pos_y != ball_radius and pos_y != 900-ball_radius : 
            t = random.random()#set initial speed direction(random)
            m = speed *random.random()#set initial speed magnitude
            if ( i< initial_infect):
                balls.append([pos_x , pos_y , math.cos(2*math.pi*t)*m,math.sin(2*math.pi*t)*m, status[1],incubation_period() ]) 
            else :
                balls.append([pos_x , pos_y , math.cos(2*math.pi*t)*m,math.sin(2*math.pi*t)*m, status[0],temps ]) 
            break
#initial data
data.append([quantity-initial_infect])
data.append([initial_infect])
data.append([0])
data.append([0])
data.append([0])



clock=pygame.time.Clock()
a=0
det =True
t=0
# draw picture and pass next step
while det :
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
       
    screen.fill(bg)
    for i in range(quantity):
        pygame.draw.circle(screen , balls[i][4] , [balls[i][0],balls[i][1]] ,ball_radius)#draw balls in the screen

    pygame.display.flip()   #update 
    pygame.time.delay(1)
    t+=1

    if (t//500 == a): #registry the time and data
        time_list.append(a) 
        statistic(balls,data)
        a=a+1
    
    
    change_status(balls)


    det =False
    for i in range(quantity):
        if balls[i][5] > 0 : 
            det =True
            break
#registry the last data

time_list.append(a) 
statistic(balls,data)
print(a)
#plot the data 
fig=plt.figure(figsize=(12,8))
plt.title('statistical trend chart', fontsize = 16)

plt.plot(time_list , data[2], 'r-' ,label = 'Contagious')
plt.plot(time_list , data[2], 'rs' )

plt.plot(time_list , data[1], 'b-' ,label = 'Infecté non Contagious')
plt.plot(time_list , data[1], 'bs' )
   
plt.plot(time_list , data[3], 'g-' ,label = 'Remise')
plt.plot(time_list , data[3], 'gs' )

plt.plot(time_list , data[4], 'k-' ,label = 'Mort')
plt.plot(time_list , data[4], 'ks' )

plt.plot(time_list , data[0], 'y-' ,label = 'Sain')
plt.plot(time_list , data[0], 'ys' )

plt.legend();
fig.savefig("fig/" +"CCC"+repr(size) + "quantity"+repr(quantity)+"  ball_size"+repr(ball_radius) +" confine_rate"+repr(cra)+ " death_rate"+ repr(dr)+" heal_time"+ repr(ht_mean/500)+" "+repr(ht_var/500)+" contagious_rate"+repr(cr)+ " incubation_Period"+repr(ip_mean/500)+" " +repr(ip_var/500) +" infect_rate"+repr(ir)  +".png")

plt.show()


