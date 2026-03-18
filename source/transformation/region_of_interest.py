import numpy as np
from plantcv import plantcv as pcv, plantcv


def region_of_interest(image: np.ndarray) -> np.ndarray:
    # hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    #
    # lower = np.array([25, 40, 40])
    # upper = np.array([90, 255, 255])
    #
    # mask = cv2.inRange(hsv, lower, upper)
    #
    # result = np.zeros_like(image)
    # result[mask == 255] = image[mask == 255]

    # result[(mask != 255) & (image.sum(axis=2) > 0)] = (0, 255, 0)
    # l_gray = pcv.rgb2gray_lab(rgb_img=image, channel="l")
    # bin_mask = pcv.threshold.otsu(gray_img=l_gray, object_type="light")
    # cleaner_mask = pcv.fill(bin_img=bin_mask, size=50)
    # clean_mask = pcv.fill_holes(cleaner_mask)

    # h, w = image.shape[:2]
    # roi1 = pcv.roi.custom(img=image, vertices=[
    #     (0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1)
    # ])

    # kept_mask = pcv.roi.filter(mask=cleaner_mask, roi=roi1, roi_type='partial')
    # labeled_objects, n_obj = pcv.create_labels(mask=kept_mask)
    # shape_img = pcv.analyze.size(img=image, labeled_mask=labeled_objects,
    #                              n_labels=n_obj)

    # roi_start_x = 0
    # roi_start_y = 0
    # roi_w = image.shape[0]
    # roi_h = image.shape[1]
    # roi_line_w = 5

    # roi = pcv.roi.rectangle(
    #     img=image,
    #     x=roi_start_x,
    #     y=roi_start_y,
    #     w=roi_w,
    #     h=roi_h
    # )

    # Create a mask based on the ROI
    # kept_mask = pcv.roi.filter(mask=image, roi=roi, roi_type='partial')

    a_gray = pcv.rgb2gray_lab(rgb_img=image, channel="a")
    bin_mask = pcv.threshold.otsu(gray_img=a_gray, object_type="dark")
    cleaned_mask = pcv.fill(bin_img=bin_mask, size=1000)
    return cleaned_mask
