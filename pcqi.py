import cv2
import numpy as np
import scipy.signal
def PCQI(img1, img2):


    window = np.multiply(cv2.getGaussianKernel(11, 1.5), (cv2.getGaussianKernel(11, 1.5)).T)


    L = 256


    window = window / np.sum(np.sum(window))

    mu1 = scipy.signal.correlate2d(img1, window, 'valid')
    mu2 = scipy.signal.correlate2d(img2, window, 'valid')
    mu1_sq = mu1 * mu1

    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2


    sigma1_sq = scipy.signal.correlate2d(img1 * img1, window, 'valid')- mu1_sq
    sigma2_sq = scipy.signal.correlate2d(img2 * img2, window, 'valid') - mu2_sq
    sigma12 = scipy.signal.correlate2d(img1 * img2, window, 'valid') - mu1_mu2

    sigma1_sq[sigma1_sq<0]=0
    sigma2_sq[sigma2_sq<0]=0


    C = 3

    pcqi_map = (4 / np.pi) * np.arctan((sigma12 + C) / (sigma1_sq + C))
    pcqi_map = pcqi_map * ((sigma12 + C) / (np.sqrt(sigma1_sq) * np.sqrt(sigma2_sq) + C))
    pcqi_map = pcqi_map * np.exp(-abs(mu1 - mu2) / L)

    mpcqi = np.mean(pcqi_map)

    return mpcqi, pcqi_map

if __name__ == '__main__':

    ref = np.array(cv2.imread(r'img\ref.png',0).tolist())
    raw = np.array(cv2.imread(r'img\contrast_changed.png',0).tolist())

    mpcqi, pcqi_map=PCQI(ref,raw)
    print(mpcqi)
