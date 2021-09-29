from PIL import Image


def get_max_size(iw, ih, mw, mh):
    rw = mw/iw
    rh = mh/ih

    final_ratio = rw if rw < rh else rh
    return int(final_ratio*iw), int(final_ratio*ih)


def get_top_left(iw, ih, mw, mh, halign, valign):
    top = 0
    left = 0

    if(halign == "right"):
        left = mw - iw
    elif(halign == "center"):
        left = int((mw-iw)/2)

    if(valign == "bottom"):
        top = mh-ih
    elif(valign == "center"):
        top = int((mh-ih)/2)

    return top, left


def resize(imgfile, mwidth, mheight, halign="center", valign="center"):
    img = Image.open(imgfile)

    iw, ih = img.size

    print("Image Size: {},{}".format(iw, ih))
    print("Required Size: {},{}".format(mwidth, mheight))

    size = get_max_size(iw, ih, mwidth, mheight)
    print("Resized Size: {},{}".format(size[0], size[1]))

    resized_img = img.resize((size[0], size[1]), Image.ANTIALIAS)

    top, left = get_top_left(
        resized_img.size[0], resized_img.size[1], mwidth, mheight, halign, valign)
    print("Top, Left: {},{}".format(top, left))

    out_img = Image.new(resized_img.mode, (mwidth, mheight), (255,))
    out_img.paste(resized_img, (left, top))
    return out_img


def paste_logo(doc, logo, count):
    out = Image.open("docs/{}".format(doc["path"])).convert('RGBA')
    temp = Image.new("RGBA", out.size, (255,))
    temp.paste(logo, (doc["left"], doc["top"]))
    out.alpha_composite(temp)
    out.save("out/final_{}_{}.png".format(count, doc["path"]))
