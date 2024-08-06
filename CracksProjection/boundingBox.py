

def is_bbox_inside_image(bbox_coords, image_size):
    image_width, image_height = image_size
    print("Running is_bbox_inside_image.......................")

    for coord in bbox_coords:
        print("coord is: ", coord)
        c = coord[0]
        print("c is: ", c)
        x, y = c[0], c[1]

        print("x,y is: ", x, y)
        print("Values Finished.........................................................")
        # print("x, y ", x , y)
        if y < 0:#x < 0 or y < 0: # or x >= image_width or y >= image_height:
            # print("Box is not inside")
            return False
    # print("Box is inside")
    return True

def is_bbox_inside_image_backward(bbox_coords, image_size):
    image_width, image_height = image_size

    for coord in bbox_coords:
        c = coord[0]
        x, y = c[0], c[1]
        # print("x, y ", x , y)
        #if x < 0 or y < 0 or x >= image_width or y >= image_height:
        if  y < 0  or y >= image_height:
            # print("Box is not inside")
            return False
    # print("Box is inside")
    return True


def convert_bbox(box):
    tlx, tly, brx, bry = box
    x = tlx
    y = tly
    w = brx - tlx
    h = bry - tly
    box1 = [x,y,w,h]
    return box1
