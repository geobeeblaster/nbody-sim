import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class body:
    def __init__(self, name, p, v, mass, radius, color):
        self.name = name
        self.p = p
        self.v = v
        self.mass = mass
        self.radius = radius
        self.color = color

def magnitude(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def unit(vector):
    return vector/magnitude(vector)

def vc(v1,v2,v3):
    return np.array([float(v1),float(v2),float(v3)])

bta = []

bta.append(["Sun", vc(0,0,0), vc(0,0,0), 1.99*10**30, 7.8*10**8,None,'gold'])
bta.append(["Earth", vc(1.5*10**11,0,0), vc(0,30000,0), 5.972*10**24,6.371*10**6,None,'blue'])
bta.append(['Venus', vc(1.08*10**11,0,0),vc(0,35000,0), 4.87*10**24, 6.052*10**6, 'Sun', 'yellow'])
#bta.append(["Moon", vc(405500*1000,0,0), vc(0,1000,0), 7.34*10**22, 1.73*10**6, "Earth", 'lightgrey'])
bta.append(['Mars', vc(2.06*10**11, 0, 0), vc(0,26000,0), 6.42*10**23, 3.38*10**6, "Sun", 'maroon'])
bta.append(['Mercury', vc(4.6*10**10,0,0), vc(0,59000,0), 3.3*10**23, 2.44*10**6,'Sun', 'dimgrey'])
#bta.append(['Jupiter', vc(7.78*10**11,0,0), vc(0,13070,0), 1.90*10**27, 6.69*10**7, 'Sun', 'lightcoral'])
# bta.append(['Io', vc(4.20*10**8,0,0), vc(0,17334,0), 8.931*10**22, 1.82*10**6, 'Jupiter', 'goldenrod'])
# bta.append(['Europa', vc(6.70*10**8,0,0), vc(0,13742,0), 4.8*10**22, 1.56*10**6, 'Jupiter', 'mistyrose'])
# bta.append(['Ganymede', vc(1.07*10**9,0,0), vc(0,10880,0), 1.48*10**23, 2.634*10**6, 'Jupiter', 'lightgrey'])
# bta.append(['Callisto', vc(1.869*10**9,0,0), vc(0,8204,0), 1.075*10**23, 2.410*10**6, 'Jupiter', 'darkgrey'])
# bta.append(['Kore', vc(2.45*10**10,0,0), vc(0,350,0), 3*10**12, 2*10**3, 'Jupiter',0])
# bta.append(['Phobos', vc(9.38*10**6,0,0), vc(0,0, 2138), 1.07*10**16, 1.226*10**4, 'Mars', 'lightgrey'])
# bta.append(['Deimos', vc(2.35*10**7,0,0), vc(0,0, 1351), 1.48*10**15, 6.2*10**3, 'Mars', 'darkgrey'])
#bta.append(['Saturn', vc(1.433*10**12,0,0), vc(0,9680,0), 5.68*10**26, 5.82*10**4, 'Sun', 'navajowhite'])
bodies = []
def parentnumber(index):
    if(bta[index][5]) == None:
        return 0
    else: 
        for bta_index in range(len(bta)):
            if(bta[bta_index][0] == bta[index][5]):
                return(parentnumber(bta_index))+1
    
pnmax = 0                    
for bta_index2 in range(len(bta)):
    pn = parentnumber(bta_index2)
    bta[bta_index2].append(pn)
    if(pn > pnmax):
        pnmax = pn

print(bta)
print(pnmax)
parentindex = 0
for pnum in range(0,pnmax+1):
    for bta_index3 in range(len(bta)):
        if(bta[bta_index3][7]) == pnum:
            for bta_index4 in range(len(bta)):
                if(bta[bta_index4][0] == bta[bta_index3][5]):
                    parentindex = bta_index4
            bodies.append(body(bta[bta_index3][0],bta[bta_index3][1]+bta[parentindex][1],bta[bta_index3][2]+bta[parentindex][2],bta[bta_index3][3],bta[bta_index3][4],bta[bta_index3][6]))
print(len(bodies))
def find_index_of_body_by_name(name):
    for bindex in range(len(bodies)):
        if(bodies[bindex].name == name):
            return bindex
saves = []
timestep = 20000
time = 0
maxtime = 1000000000
collision = False
G = 6.67*10**-11
while collision == False and time<maxtime:
    saves.append(bodies)
    new_state = []
    for b in bodies:
        acceleration = np.array([0,0,0])        
        velocity = b.v.copy()
        position = b.p.copy()
        for b2 in bodies:
            gravfield = np.array([0,0,0])
            if(b2.name != b.name):
                r = magnitude(b.p-b2.p)
                gravfield = G*b2.mass/r**2*unit(b2.p-b.p)
                acceleration = acceleration+gravfield
                if(r < b.radius+b2.radius):
                    print(r)
                    print('There has been a collision between ' + b.name + ' and ' + b2.name + ' at t = ' + str(time))
                    collision = True
        velocity += acceleration*timestep
        position += velocity*timestep

        new_state.append(body(b.name, position, velocity, b.mass, b.radius, b.color))
    bodies = new_state
    time += timestep
#graphs
legend = []
reference = find_index_of_body_by_name("Mercury")
for b3_index in range(len(bodies)):
    color = 0
    body_name = bodies[b3_index].name
    x = []
    y = []
    for save in saves:
        reference_position = save[reference].p
        x.append(save[b3_index].p[0]-reference_position[0])
        y.append(save[b3_index].p[1]-reference_position[1])
    color = bodies[b3_index].color
    if color == 0:
        plt.plot(x,y)
    else:
        plt.plot(x,y,color)
    legend.append(body_name + ' position')
plt.legend(legend)
plt.axis('square')
def limit(b1,b2, scale=1.2):
    return magnitude(bodies[find_index_of_body_by_name(b1)].p-bodies[find_index_of_body_by_name(b2)].p)*scale
lim = limit('Sun', 'Mars', 1.4)
plt.xlim(-lim,lim)
plt.ylim(-lim,lim)
plt.title('X and Y positions of the Objects')
plt.xlabel('X position of objects')
plt.ylabel('Y position of objects')
plt.show()