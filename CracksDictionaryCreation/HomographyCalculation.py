

import cv2
import numpy as np

from skimage.measure import ransac
from skimage.transform import AffineTransform
import math


def getSIFTkeypoints(im1, im2, siftPoints=5000, lowesRatio=0.75, returnRawPts=False, ):
    try:
        sift = cv2.SIFT_create(siftPoints)
        # sift = cv2.SIFT_create()

        # detect and compute the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(im1, None)
        kp2, des2 = sift.detectAndCompute(im2, None)

        # create BFMatcher object
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        anglesKp = []
        good = []
        deltaXKp = []
        for m, n in matches:
            if m.distance < lowesRatio * n.distance:
                angle = math.degrees(math.atan2(kp2[m.trainIdx].pt[1] - kp1[m.queryIdx].pt[1],
                                                kp2[m.trainIdx].pt[0] + im1.shape[1] - kp1[m.queryIdx].pt[0]))
                deltaX = kp2[m.trainIdx].pt[0] - kp1[m.queryIdx].pt[0]
                # anglesKp.append(angle)
                # deltaXKp.append(deltaX)
                good.append([m])

        impts1 = np.float32([kp1[m[0].queryIdx].pt for m in good]).reshape(-1, 2)
        impts2 = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(-1, 2)


    except:
        print('Faliure in SIFT keypoint generation')
        return None

    imgBefore = cv2.drawMatchesKnn(im1, kp1, im2, kp2, good, None, flags=0)
    # # cv2.imshow('imgBefore before keypt filtering', imgBefore)
    # # cv2.waitKey(0)

    impts1 = np.float32([kp1[m[0].queryIdx].pt for m in good]).reshape(-1, 2)
    impts2 = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(-1, 2)

    if len(impts1) < 4:
        print('not enough kpt matches SIFT', len(impts1))
        return None

    if returnRawPts:
        return impts1, impts2, None, None

    # Ransac
    model, inliers = ransac(
        (impts1, impts2),
        AffineTransform, min_samples=4,
        residual_threshold=1.1, max_trials=1000  # residual_threshold=10
    )

    if inliers is None:
        print('no inliers in SIFT for distance shift')
        return None

    validKp1 = [[np.float32(point[0]), np.float32(point[1])] for point in impts1[inliers]]
    validKp2 = [[np.float32(point[0]), np.float32(point[1])] for point in impts2[inliers]]

    # validKp1 = cv2.KeyPoint_convert(validKp1)
    # validKp2 = cv2.KeyPoint_convert(validKp2)

    # validKp1 = np.float32(validKp1)
    # validKp2 = np.float32(validKp2)
    print(' Matches in SIFT with RANSAC', len(validKp1), len(validKp2))

    if len(validKp1) == 0 or len(validKp1) < 8:
        print('not enough keypoints detected between images SIFT')
        return None

    validKp1 = np.array(validKp1)
    validKp2 = np.array(validKp2)
    print(' Matches in SIFT', len(validKp1), len(validKp2))

    Homography, mask = cv2.findHomography(validKp1, validKp2, cv2.RANSAC, 3.0)


    # Homography, mask = cv2.findHomography(keyPoints1, keyPoints2, cv2.RANSAC, 3.0)

    return Homography
