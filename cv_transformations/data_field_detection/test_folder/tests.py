from ..data_field_detection import *
import cv2
from .paths import get_data_field_detection_path


# test_file = cv2.imread(get_data_field_detection_path('img_1.png'))
# passport_ocr_img, passport_data = get_passport_data('img_1.png')
# print(passport_data)
# cv2.imshow('',passport_ocr_img)
#
cv2.imshow('',get_us_driving_license_data('img_1.png'))
cv2.waitKey(0)
cv2.destroyAllWindows()

# for i in get_invoice_details_using_aws('img_3.png'):
#     #TODO:- Figure some good way to output data maybe creating csv's as required according to need
#     print(i)