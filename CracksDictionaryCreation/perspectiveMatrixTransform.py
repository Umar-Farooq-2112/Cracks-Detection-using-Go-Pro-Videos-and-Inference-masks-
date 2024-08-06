import cv2
import numpy as np


def find_features(image_0, image_1):
    '''
    Feature detection using the sift algorithm and KNN
    return keypoints(features) of image1 and image2
    '''
    sift = cv2.SIFT_create(15000)  # 10000
    key_points_0, desc_0 = sift.detectAndCompute(cv2.cvtColor(image_0, cv2.COLOR_BGR2GRAY), None)
    key_points_1, desc_1 = sift.detectAndCompute(cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY), None)

    length = False
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(desc_0, desc_1, k=2)
    feature = []
    for m, n in matches:
        if m.distance < 0.85 * n.distance:
            feature.append(m)
    # print("Length be4 geometric filtering: ", len(feature))
    threshold = 0.29
    good_matches = []
    # print("Entering Loop")
    while (length == False):
        good_matches = []
        # lowes ratio test
        for m, n in matches:
            if m.distance < threshold * n.distance:
                # print(m.queryIdx, m.trainIdx)
                good_matches.append(m)
        # print(len(good_matches))
        if len(good_matches) < 99 and len(good_matches) >= 5:
            length = True
            # print(len(good_matches))
        elif len(good_matches) < 7:
            threshold = threshold + 0.02
        else:
            threshold = threshold - 0.02

    # Geometric filtering
    # print("Exiting loop")
    num_iterations = 200
    # inlier_threshold = 0.7  # Adjust this based on your problem
    best_model = None
    # print("Inlier Threshold Is : ", inlier_threshold)
    best_inliers = []
    inlier_threshold = 3
    best_perspective_matrix = np.eye(3)

    for _ in range(num_iterations):

        # Randomly sample a minimal set of points
        sample_indices = np.random.choice(len(good_matches), 4, replace=False)
        src_points = np.float32([key_points_0[good_matches[i].queryIdx].pt for i in sample_indices])
        dst_points = np.float32([key_points_1[good_matches[i].trainIdx].pt for i in sample_indices])
        perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        query_indices = [match.queryIdx for match_pair in matches for match in match_pair]
        src_points_all = np.float32([key_points_0[m.queryIdx].pt for m in feature])
        dst_points_all = np.float32([key_points_1[m.trainIdx].pt for m in feature])

        distances = np.linalg.norm(
            dst_points_all - cv2.perspectiveTransform(src_points_all.reshape(-1, 1, 2), perspective_matrix).reshape(
                -1, 2), axis=1)
        inliers = np.where(distances < inlier_threshold)[0]

        if len(inliers) > len(best_inliers):
            best_model = perspective_matrix
            best_inliers = inliers
            best_perspective_matrix = perspective_matrix
        good_match_indices = [feature[i] for i in best_inliers]

        #print("Total inliers")
    # new_image = cv2.drawMatches(image_0, key_points_0, image_1, key_points_1, good_match_indices, None,None, cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    # new_image = cv2.resize(new_image, (900, 600))
    # cv2.imshow("image", new_image)
    # cv2.waitKey(0)
    # print("Image SHOWN BY NOW")
    return best_perspective_matrix
