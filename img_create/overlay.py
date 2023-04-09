from PIL import Image, ImageDraw, ImageOps
import numpy as np
import cv2
import os
import sys
from local_settings import path_to_save_overlayed_image, path_to_image_frame, \
    temp_pictures_path


# use for frame that does need to be cut
def overlay_image_under(path_image, path_frame, desired_size, pts1, pts2,
                        file_name):
    img = cv2.imread(path_image)
    blue_channel, green_channel, red_channel = cv2.split(img)
    # creating a dummy alpha channel max 255
    alpha_channel = np.ones(blue_channel.shape, dtype=blue_channel.dtype) * 255
    img_bgra = cv2.merge((blue_channel, green_channel, red_channel,
                          alpha_channel))
    img_resize = cv2.resize(img_bgra, dsize=desired_size)
    rows, cols, ch = img_resize.shape
    # get the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # transform the image using perspective transform matrix
    changed_picture = cv2.warpPerspective(img_resize, matrix, (cols, rows))
    # temporary save img for PIL
    cv2.imwrite(f"{temp_pictures_path}/temp_foreground_img.png",
                changed_picture)
    with Image.open(f"{temp_pictures_path}/temp_foreground_img.png"
                    ).convert("RGBA") as img:
        with Image.open(path_frame).convert("RGBA") as img_frame:
            img.paste(img_frame, (0, 0), img_frame)
            # save picture
            img.save(f"{path_to_save_overlayed_image}/{file_name}.png", "PNG")
    os.remove(f"{temp_pictures_path}/temp_foreground_img.png")


# use for frame that doesn't need to be cut
def overlay_image_over(path_image, path_frame, desired_size, pts1, pts2,
                       file_name):
    img = cv2.imread(path_image)
    blue_channel, green_channel, red_channel = cv2.split(img)
    # creating a dummy alpha channel max 255
    alpha_channel = np.ones(blue_channel.shape, dtype=blue_channel.dtype) * 255
    img_bgra = cv2.merge((blue_channel, green_channel, red_channel,
                          alpha_channel))
    img_resize = cv2.resize(img_bgra, dsize=desired_size)
    rows, cols, ch = img_resize.shape
    # get the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # transform the image using perspective transform matrix
    changed_picture = cv2.warpPerspective(img_resize, matrix, (cols, rows))
    # temporary save img for PIL
    cv2.imwrite(f"{temp_pictures_path}/temp_foreground_img.png",
                changed_picture)
    with Image.open(path_frame).convert("RGBA") as img_back:
        with Image.open(f"{temp_pictures_path}/temp_foreground_img.png"
                        ).convert("RGBA") as img:
            img_back.paste(img, (0, 0), img)
            img_back.save(f"{path_to_save_overlayed_image}/{file_name}.png",
                          "PNG")
    os.remove(f"{temp_pictures_path}/temp_foreground_img.png")


# use for two images which don't need to have cut corners
def overlay_two_images(path_image, path_frame, desired_size, pts1, pts2, pts3,
                       pts4, file_name):
    img = cv2.imread(path_image)
    blue_channel, green_channel, red_channel = cv2.split(img)
    # creating a dummy alpha channel max 255
    alpha_channel = np.ones(blue_channel.shape, dtype=blue_channel.dtype) * 255
    img_bgra = cv2.merge((blue_channel, green_channel, red_channel,
                          alpha_channel))
    img_resize = cv2.resize(img_bgra, dsize=desired_size)
    rows, cols, ch = img_resize.shape
    # get the perspective transform matrix
    matrix_1 = cv2.getPerspectiveTransform(pts1, pts2)
    # transform the image using perspective transform matrix for first img
    changed_picture_1 = cv2.warpPerspective(img_resize, matrix_1, (cols, rows))
    # get the perspective transform matrix
    matrix_2 = cv2.getPerspectiveTransform(pts3, pts4)
    # transform the image using perspective transform matrix for second img
    changed_picture_2 = cv2.warpPerspective(img_resize, matrix_2, (cols, rows))
    # temporary save img for PIL
    cv2.imwrite(f"{temp_pictures_path}/temp_foreground_img_1.png",
                changed_picture_1)
    cv2.imwrite(f"{temp_pictures_path}/temp_foreground_img_2.png",
                changed_picture_2)
    with Image.open(f"{temp_pictures_path}/temp_foreground_img_1.png"
                    ).convert("RGBA") as img_1:
        with Image.open(f"{temp_pictures_path}/temp_foreground_img_2.png"
                        ).convert("RGBA") as img_2:
            with Image.open(path_frame).convert("RGBA") as img_frame:
                # img 1 under img 2
                img_1.paste(img_2, (0, 0), img_2)
                img_1.paste(img_frame, (0, 0), img_frame)
                img_1.save(f"{path_to_save_overlayed_image}"
                           f"/{file_name}.png", "PNG")
    os.remove(f"{temp_pictures_path}/temp_foreground_img_1.png")
    os.remove(f"{temp_pictures_path}/temp_foreground_img_2.png")


def overlay_two_rounded_images(path_image, path_frame, desired_size, pts1,
                               pts2, pts3, pts4, cut_corner_back,
                               cut_corner_front, size_cut_back,
                               size_cut_front, file_name):
    img = Image.open(path_image)
    img_resized = img.resize(desired_size)
    if cut_corner_back:
        img_cut_back = img_resized
        add_corners(img_cut_back, size_cut_back)
        # cv2 doesn't read alpha mask properly from "PNG" format
        img_cut_back.save(f"{temp_pictures_path}/temp_cut_picture_back.tiff",
                          "TIFF")
    else:
        img_cut_back = img_resized
        img_cut_back.save(f"{temp_pictures_path}/temp_cut_picture_back.tiff",
                          "TIFF")
    if cut_corner_front:
        img_cut_front = img_resized
        add_corners(img_cut_front, size_cut_front)
        # cv2 doesn't read alpha mask properly from "PNG" format
        img_cut_front.save(f"{temp_pictures_path}/temp_cut_picture_front.tiff",
                           "TIFF")
    else:
        img_cut_front = img_resized
        img_cut_front.save(f"{temp_pictures_path}/temp_cut_picture_front.tiff",
                           "TIFF")

    img_frame = cv2.imread(f"{temp_pictures_path}/temp_cut_picture_back.tiff",
                           cv2.IMREAD_UNCHANGED)
    img_front = cv2.imread(f"{temp_pictures_path}/temp_cut_picture_front.tiff",
                           cv2.IMREAD_UNCHANGED)

    blue_channel_back, green_channel_back, red_channel_back, \
        alpha_channel_back = cv2.split(img_frame)
    blue_channel_front, green_channel_front, red_channel_front, \
        alpha_channel_front = cv2.split(img_front)
    img_bgra_back = cv2.merge((blue_channel_back, green_channel_back,
                               red_channel_back, alpha_channel_back))
    img_bgra_front = cv2.merge((blue_channel_front, green_channel_front,
                                red_channel_front, alpha_channel_front))

    rows_back, cols_back, channel_back = img_bgra_back.shape
    rows_front, cols_front, channel_front = img_bgra_front.shape
    # get the perspective transform matrix
    matrix_1 = cv2.getPerspectiveTransform(pts1, pts2)
    # transform the image using perspective transform matrix for first img
    changed_picture_1 = cv2.warpPerspective(img_bgra_back, matrix_1,
                                            (cols_back, rows_back))
    # get the perspective transform matrix
    matrix_2 = cv2.getPerspectiveTransform(pts3, pts4)
    # transform the image using perspective transform matrix for second img
    changed_picture_2 = cv2.warpPerspective(img_bgra_front, matrix_2,
                                            (cols_front, rows_front))
    # temporary save img for PIL
    cv2.imwrite(f"{temp_pictures_path}/temp_foreground_img_1.png",
                changed_picture_1)
    cv2.imwrite(f"{temp_pictures_path}/temp_foreground_img_2.png",
                changed_picture_2)

    with Image.open(f"{temp_pictures_path}/temp_foreground_img_1.png"
                    ).convert("RGBA") as img_1:
        with Image.open(f"{temp_pictures_path}/temp_foreground_img_2.png"
                        ).convert("RGBA") as img_2:
            with Image.open(path_frame).convert("RGBA") as img_frame:
                img_1.paste(img_2, (0, 0), img_2)  # img 1 under img 2
                img_1.paste(img_frame, (0, 0), img_frame)
                img_1.save(f"{path_to_save_overlayed_image}/"
                           f"{file_name}.png", "PNG")
    os.remove(f"{temp_pictures_path}/temp_cut_picture_back.tiff")
    os.remove(f"{temp_pictures_path}/temp_cut_picture_front.tiff")
    os.remove(f"{temp_pictures_path}/temp_foreground_img_1.png")
    os.remove(f"{temp_pictures_path}/temp_foreground_img_2.png")


# makes circular corners for picture
def add_corners(im, rad):
    # creates black image with space for ellipse to do alpha masking
    circle_right_bottom = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle_right_bottom)
    # draws an ellipse in circle_right_bottom image with values that make ~1/4
    # of ellipse to make rounded cut
    draw.ellipse((-rad * 2, -4 * rad, rad * 2.755, rad * 2.1), fill=255)
    alpha = Image.new('L', im.size, 255)
    width, height = im.size
    # mirror (vertical flip) circle_right_bottom to make circle_left_bottom
    circle_left_bottom = ImageOps.mirror(circle_right_bottom)
    # flips (horizontal flip) circle_right_bottom to make circle_right_top
    circle_right_top = ImageOps.flip(circle_right_bottom)
    # flips (horizontal flip) circle_right_bottom to make circle_right_top
    circle_left_top = ImageOps.flip(circle_left_bottom)
    # adds masking to corners with images created above in specified position
    alpha.paste(circle_left_top.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle_left_bottom.crop((0, rad, rad, rad * 2)),
                (0, height - rad))
    alpha.paste(circle_right_top.crop((rad, 0, rad * 2, rad)),
                (width - rad, 0))
    alpha.paste(circle_right_bottom.crop((rad, rad, rad * 2, rad * 2)),
                (width - rad, height - rad))
    im.putalpha(alpha)
    return im


if __name__ == "__main__":
    try:
        # path to image
        path_image = str(sys.argv[1])
        # display type
        display = str(sys.argv[2]).upper()
        if display == "TABLET_01":
            # background
            path_frame = f"{path_to_image_frame}/tablet01_frame.png"
            # of img to get same size as background
            desired_size = (2918, 3001)
            # points in old plane
            points_old_1 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane
            points_new_1 = np.float32([[727, 447], [2175, 447], [727, 2489],
                                       [2175, 2489]])
            overlay_image_under(path_image, path_frame, desired_size,
                                points_old_1, points_new_1, "TABLET_01")
        # tablet frame img which is pasted on image
        elif display == "TABLET_02":
            # background
            path_frame = f"{path_to_image_frame}/tablet02_frame.png"
            # size of image to get same size as background
            desired_size = (1200, 1200)
            # points in old plane
            points_old_1 = np.float32([[0, 0], [1200, 0], [0, 1200],
                                       [1200, 1200]])
            # points in new plane
            points_new_1 = np.float32([[298, 86], [719, 220], [707, 866],
                                       [1125, 907]])
            overlay_image_under(path_image, path_frame, desired_size,
                                points_old_1, points_new_1, "TABLET_02")
        elif display == "PHONE_01":
            # background
            path_frame = f"{path_to_image_frame}/phone01_frame.png"
            # size of image to get same size as background
            desired_size = (2918, 3001)
            # points in old plane
            points_old_1 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane
            points_new_1 = np.float32([[981, 398], [1969, 398], [981, 2498],
                                       [1969, 2498]])
            overlay_image_under(path_image, path_frame, desired_size,
                                points_old_1, points_new_1, "PHONE_01")
        elif display == "AUDIOBOOK_TABLET_01":
            # background
            path_frame = f"{path_to_image_frame}/audiobook+tablet_frame.png"
            # of img to get same size as background
            desired_size = (2918, 3001)
            # points in old plane
            points_old_1 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane
            points_new_1 = np.float32([[426, 429], [1874, 429], [426, 2470],
                                       [1874, 2470]])
            overlay_image_under(path_image, path_frame, desired_size,
                                points_old_1, points_new_1,
                                "AUDIOBOOK_TABLET_01")
        elif display == "PHONE_TABLET_01":
            # background
            path_frame = f"{path_to_image_frame}/phone+tablet_frame.png"
            # of img to get same size as background
            desired_size = (2918, 3001)
            # points in old plane first pic
            points_old_1 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane first pic
            points_new_1 = np.float32([[1041, 321], [2489, 321], [1041, 2362],
                                       [2489, 2362]])
            # points in old plane second pic
            points_old_2 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane second pic
            points_new_2 = np.float32([[455, 928], [1265, 928], [455, 2650],
                                       [1265, 2650]])
            overlay_two_images(path_image, path_frame, desired_size,
                               points_old_1, points_new_1, points_old_2,
                               points_new_2, "PHONE_TABLET_01")
        elif display == "AUDIOBOOK_PHONE_TABLET_01":
            # background
            path_frame = f"{path_to_image_frame}/audiobook+phone+" \
                         f"tablet_frame.png"
            # of img to get same size as background
            desired_size = (2918, 3001)
            # points in old plane first pic
            points_old_1 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane first pic
            points_new_1 = np.float32([[774, 487], [2009, 487], [774, 2210],
                                       [2009, 2210]])
            # points in old plane second pic
            points_old_2 = np.float32([[0, 0], [2918, 0], [0, 3001],
                                       [2918, 3001]])
            # points in new plane second pic
            points_new_2 = np.float32([[289, 982], [1008, 982], [289, 2453],
                                       [1008, 2453]])
            overlay_two_rounded_images(path_image, path_frame, desired_size,
                                       points_old_1, points_new_1,
                                       points_old_2, points_new_2, True, True,
                                       60, 210, "AUDIOBOOK_PHONE_TABLET_01")
        else:
            print("Invalid display")
    except IndexError:
        print("insert two arguments <path_to_image> <display>")
