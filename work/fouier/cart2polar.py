import numpy as np
# import matplotlib.pyplot as plt


def radius(x,y,center):
    r = np.sqrt((x-center[0])**2+(y-center[1])**2)
    return r
def theta(x,y,center):
    t = np.arctan2((x-center[0]),(y-center[1]))+np.pi
    return t


def cart2polar(pic):
    # setup
    rmax = 50
    dr = 1  # dr >= 1
    rs = np.arange(0,rmax,dr)
    nannuli = len(rs)

    ntheta_index = 7
    ntheta = 2**ntheta_index
    dtheta = 2*np.pi/ntheta

    r_theta = np.zeros((nannuli,ntheta))
    count = np.zeros((nannuli,ntheta))

    adaptive_flag = 1

    # ------------
    center = [(pic.shape[0]-1)/2,(pic.shape[1]-1)/2]

    # go through the picture
    for xi in range(pic.shape[0]):
        for yi in range(pic.shape[1]):
            if radius(xi,yi,center) < rmax:
                rn = int(np.floor(radius(xi,yi,center)/dr))
                thetan = int(np.floor(theta(xi,yi,center)/dtheta))
                r_theta[rn,thetan] += pic[xi,yi]
                count[rn,thetan] += 1

    if adaptive_flag:
    # adaptive dtheta
        index = ntheta_index
        while np.all(count) == False and index >= 0:
            max_0 = np.max(np.arange(nannuli)[~np.all(count,axis=1)])+1 # max r that has a count 0
            r_theta[0:max_0,:] = 0
            count[0:max_0,:] = 0
            index -= 1
            ntheta_adaptive = 2**index
            dtheta_adaptive = 2*np.pi/ntheta_adaptive
            rate = 2**(ntheta_index-index)
            # print(ntheta_adaptive,max_0)
            for xi in range(pic.shape[0]):
                for yi in range(pic.shape[1]):
                    if radius(xi,yi,center) < max_0*dr: 
                        rn = int(np.floor(radius(xi,yi,center)/dr))
                        thetan_adaptive = int(np.floor(theta(xi,yi,center)/dtheta_adaptive))
                        r_theta[rn,thetan_adaptive*rate:(thetan_adaptive+1)*rate] += pic[xi,yi]
                        count[rn,thetan_adaptive*rate:(thetan_adaptive+1)*rate] += 1
            # move to the left
            # r_theta[0:max_0,:] = np.roll(r_theta[0:max_0,:],-int(rate/2),axis=1)
            # count[0:max_0,:] = np.roll(count[0:max_0,:],-int(rate/2),axis=1)
            # don't need to move

    count[np.where(count==0)] = np.inf
    pic_polar = r_theta/count
    pic_polar = pic_polar/ntheta
    # pic_polar = pic_polar/3*np.size(pic_polar)**2/np.size(pic)*dr  # a coefficient which i haven't finish
    pic_polar = pic_polar/np.max(pic_polar)
    return pic_polar


# # test picture
# pic = np.ones((200,200))
# pic[90:110,:]+=1
# # pic[50:,40:60]+=1
# pic[95:105,:]+=1
# # pic[50:,45:55]+=1


# polar = cart2polar(pic)
# plt.imshow(polar)
# plt.show()