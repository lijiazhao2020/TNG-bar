import numpy as np

def fouier_a2(pic_polar):
    a2=[]
    angle=[]
    for ri in pic_polar:
        fft_r = np.fft.fft(ri)
        a0i = np.abs(np.real(fft_r[0]))
        a2i = np.abs(np.real(fft_r[2]))
        anglei = np.angle(fft_r[2])
        a2.append(a2i/a0i)
        angle.append(anglei)
    a2 = np.array(a2)
    angle = np.array(angle)
    return a2,angle
