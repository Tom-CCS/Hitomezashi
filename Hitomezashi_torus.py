import numpy as np
import matplotlib.pyplot as plt

# ================================================
#
#      Main Function to draw Graph_{M, N}(x, y)
#         You can modify paramaters below
#
# ================================================

def one_instance(x, y = None,
                 visual = False,
                 homologous_only = False,
                 planar = False,
                 starting_points = False,
                 starting_list = True,
                 decompose=-1,
                 excursion = False):
    plt.figure(figsize=(10,10))
    if y is None:
        y = x
    n = x.shape[0]
    m = y.shape[0]
    A=np.ones((m,n),dtype=np.int32)

    count=0
    # first loop starts from (0, 0)
    sta=np.array([0,0],dtype=np.int32)
    cur=np.array([0,0],dtype=np.int32)
    A[0,0]=0
    limit = num_cycles if visual else n**3 # limit on how many cycles to draw
    draw_count = 0 # limit on on how many cycles to draw
    length = 0 # length of the cycle
    while draw_count < limit:
        S_dx = 0   # total movement in x direction
        S_dy = 0   # total movement in y direction
        length = 0
        step_start = [[],[]]
        step_dir = [[],[]]
        boundary_passage = False #whether the walk crosses the boundary
        while True:
            cc= [cur[0], cur[1]]

            # imagine all walk outside the square to be defined as follows.
            walk1 = 0
            if cur[1] < 0:
                boundary_passage = True
                walk1 = 0
            elif cur[1] >= n:
                boundary_passage = True
                walk1 = 1
            else:
                walk1 = x[cur[1]]
            cur[0]=cur[0]+2*walk1-1
            if not planar:
                #toroidal walk, mod n
                cur[0] %= m
            
                
            walk2 = 0
            if cur[0] < 0:
                boundary_passage = True
                walk2 = 1 
            elif cur[0] >= m:
                boundary_passage = True
                walk2 = 0
            else:
                walk2 = y[cur[0]]
            
            cur[1]=cur[1]+2*walk2-1
            if not planar:
                #toroidal walk, mod n
                cur[1] %= n
                
            try:  
                A[cur[0],cur[1]]=0
            except:
                # ignore out of boundary walk
                pass
            # the algorithm is walking two steps at a time
            length += 2

            def add_arrow(x, y, dx, dy):
                step_start[0].append(x)
                step_start[1].append(y)
                step_dir[0].append(dx)
                step_dir[1].append(dy)
                #special treatment for border crossings
                if not planar and ((x + dx >= m) or (x + dx < 0)):
                   step_start[0].append((x + dx) % m - dx)
                   step_start[1].append(y)
                   step_dir[0].append(dx)
                   step_dir[1].append(dy)
                if not planar and ((y + dy >= n) or (y + dy < 0)):
                   step_start[0].append(x)
                   step_start[1].append((y + dy) % n - dy)
                   step_dir[0].append(dx)
                   step_dir[1].append(dy)
            add_arrow(cc[0], cc[1], 2*walk1-1, 0)
            add_arrow(cur[0], cc[1], 0, 2*walk2-1)
            S_dx += 2*walk1-1
            S_dy += 2*walk2-1
                

            if np.array_equal(cur, sta):
                count+=1
                break
        ## draw the current loop
        if visual:
            if ((not homologous_only or planar or S_dx != 0 or S_dy != 0)
                and (not planar or boundary_passage)):
                print(draw_count)
                draw_count += 1
                lam = S_dx // m
                mu = S_dy // n
                # attributes of the arrows
                hw, hl, hal, cr = 3,3,3, colors[draw_count-1]
                # when decomposing
                if decompose >= 0:
                    hw, hl, hal= 0,0,0
                    
                if decompose < 0 or (cur[0] + cur[1] - decompose) % 2 == 1:
                    plt.quiver(step_start[0], step_start[1],
                               step_dir[0], step_dir[1], color= cr,
                               headwidth=hw, headlength=hl, headaxislength=hal,
                               scale = 1, scale_units='x',
                               label="length is {}, ({}, {})".format(str(length), str(lam), str(mu)))
                if (S_dx != 0 or S_dy != 0):
                    predicted_length_mod_8 = 2 * (n * mu + m * lam - mu * (2 * sum(x) - n))
                    print("predicted length modulo 8: ", predicted_length_mod_8 % 8)
                    print("actual length modulo 8: ", length % 8)
        ## prepare for next loop
        f_one=np.where(A==1)    ## first 1 in A[][] 
        if len(f_one[0])==0:    ## if no 1 in A[][], we found all loops
            break
        sta=np.array([f_one[0][0],f_one[1][0]],dtype=np.int32)     ##starting state
        A[sta[0],sta[1]]=0    ##set starting state to 0
        cur=np.copy(sta)
            
    if visual and decompose < 0:
        # plot x an y on the boundary of the graph
        for i in range(0, n):
            plt.text(-1, i+0.2, '+' if x[i] > 0 else '−', ha='center', va='center', color='black', fontsize=12)
        for i in range(0, m):
            plt.text(i+0.2, -1, '+' if y[i] > 0 else '−', ha='center', va='center', color='black', fontsize=12)
        # draw boundary of region
        plt.plot([0,0],[0,n],[0,m],[n,n],[m,m],[n,0],[m,0],[0,0], color="black", linestyle = 'dashed')
        #plt.legend()
        plt.xticks([])
        plt.yticks([])
        plt.show()
    
    if visual and decompose >= 0:
        # draw boundary of region
        plt.plot([0,0],[0,n],[0,m],[n,n],[m,m],[n,0],[m,0],[0,0], color="black", linestyle = 'dashed')
        #plt.legend()
        plt.xticks([])
        plt.yticks([])
        plt.show()
        
    return count

# ================================================
#
#      Parameters of the Hitomezashi pattern
#
# ================================================
# The dimension of the Hitomezashi pattern
m = 6 
n = 8

# The orientation of the horizontal edges
i = 0b0001_1111

# The orientation of the vertical edges
j = 0b0001_11

# Maximum number of cycles to draw
num_cycles = 8

# The color of each cycle to draw
colors = ["blue", "cyan", "green", "orange",
          "red", "lightgreen", "pink", "darkred"]

# You must provide enough colors
assert len(colors) >= num_cycles

# ================================================
#
#                End of Parameters
#
# ================================================


# Convert the binary string to a NumPy array of integers
all_count=np.zeros((100,))
binary_str = np.binary_repr(i, width=n)
# Convert the binary string to a NumPy array of integers
row = np.array([int(d) for d in binary_str],dtype=np.int32)
binary_str = np.binary_repr(j, width=m)

column = np.array([int(d) for d in binary_str],dtype=np.int32)
print("k(x): ", 2 * sum(row) - n)
print("k(y): ", 2 * sum(column) - m)
print(one_instance(row, y = column, decompose = -1,
                 visual = True, homologous_only = False, planar = False)) 
