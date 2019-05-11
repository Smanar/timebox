#!/usr/bin/python
# -*- coding: latin-1 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import os
import sys
from timeboximage import TimeBoxImage

"""
Color are encoded in 12 bits, 4bits for each color.
That is not standard for bmp, so when loading an image it is converted to 
24 bits bitmap (8/color), then the 4 LSB bits for each colors are dropped.
"""

# bmp 16bit palette to divoom palett ...
# bmp pallett
BMP_BLACK = 0
BMP_DARK_RED = 1
BMP_DARK_GREEN = 2
BMP_YELLOW_OCHRE = 3
BMP_GREEN = 6
BMP_PINK = 7
BMP_LIGHT_PINK = 8
BMP_RED = 9
BMP_ANOTHER_GREEN = 10
BMP_YELLOW = 11
BMP_BLUE = 12
BMP_LIGHT_BLUE = 14
BMP_WHITE = 15
	
# way:
# 1 horizontal from left to right
# 2 vertical from upper to lower
# 3 horizontal from right to left
# 4 vertical from lower to upper
def _slices(image, way=1, slice_size=11):
	'''Create 10x10 images from a bigger image e.g. 10x40.'''
	width, height = image.size
	# calculate slice size:
	slices = 1
	if (way == 1) or (way == 3):
		slices = width - slice_size
	elif (way == 2)  or (way == 4):
		slices = height - slice_size
	
	result_images = []
	
	if (way == 1):
		for slice in range(slices):
			new_box = (slice, 0, slice+slice_size, height)
			new_img = image.crop(new_box)
			result_images.append(new_img)
	elif (way == 2):
		for slice in range(slices):
			new_box = (0, slice, width, slice+slice_size)
			new_img = image.crop(new_box)
			result_images.append(new_img)
	elif (way == 3):
		for slice in range(slices,-1,-1):
			new_box = (slice, 0, slice+slice_size, height)
			new_img = image.crop(new_box)
			result_images.append(new_img)
	elif (way == 4):
		for slice in range(slices,-1,-1):
			new_box = (0, slice, width, slice+slice_size)
			new_img = image.crop(new_box)
			result_images.append(new_img)
		
	return result_images
	
# ways
# 1 horizontal from left to right
# 2 vertical from upper to lower
# 3 horizontal from right to left
# 4 vertical from lower to upper
def scroll_between(old_img, new_img, way=1):
	'''Does a scroll between the old and the new image and returns all images in between.'''
	img = None
	if (way == 1):
		img = concatenate(old_img, new_img, 1)
	elif (way == 2):
		img = concatenate(old_img, new_img, 2)
	elif (way == 3):
		img = concatenate(new_img, old_img, 1)
	elif (way == 4):
		img = concatenate(new_img, old_img, 2)	
	sliced_images = _slices(img, way)
	sliced_images.append(new_img)
	return sliced_images
	
def concatenate(image1, image2, way=1):
    '''Concatenates the sencond image to the first'''
    if (way == 1):
        width = image1.width + image2.width
        height = max(image1.height, image2.height)
        result_img = create_default_image((width, 11))
        result_img.paste(image1, (0, 0))
        result_img.paste(image2, (image1.width, 0))
    if (way == 2):
        result_img = create_default_image((11, 22))
        result_img.paste(image1, (0, 0))
        result_img.paste(image2, (0, 11))
    return result_img
	

	
def horizontal_slices(image, slice_size=11):
	'''Create 10x10 images from a bigger image e.g. 10x40.'''
	return _slices(image=image, way=1, slice_size=slice_size)
	
def image_horizontal_slices(image_path, slice_size=11):
	'''Create 10x10 images from a bigger image given as path.'''
	img = Image.open(image_path)
	return horizontal_slices(img, slice_size)
	
def create_default_image(size=(11,11)):
	'''Create an image with the correct palette'''
	# make use of the black image to copy the palette over
	# proto = Image.open(os.path.join(os.path.dirname(__file__), "images/black.bmp"))
	# im = Image.new("P", size)
	# im.putpalette(proto.palette.getdata()[1])
	im = Image.new("RGB", size)
	return im

def draw_text_to_image(text, color="red", size=(0,11), empty_start=True, empty_end=True, font = None):
    '''Draws the string in given color to an image and returns this iamge'''
    #fn = ImageFont.load(os.path.join(os.path.dirname(__file__),'fonts/slkscr.pil'))
    #fn = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'fonts/11x7 Matrix.ttf'),13)
    #fn = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'fonts/tallround.ttf'),13)
    if not font:
        fn = ImageFont.truetype(os.path.join(os.path.dirname(__file__),'fonts/Electronic scale.ttf'),11)
    else:
        fn = font
    draw_txt = ImageDraw.Draw(create_default_image())
    width, height = draw_txt.textsize(text, font=fn)
    del draw_txt
    if empty_start:
        width += size[1]
    if empty_end:
        width += size[1]
    im = create_default_image((width, size[1]))
    draw = ImageDraw.Draw(im)

    if empty_start:
        offset_x = size[1]
    else:
        offset_x = 0
        
    offset_y = (11 - height) / 2
    
    draw.text((offset_x,offset_y), text, font=fn, fill=color)
    del draw
    return im

def draw_multiple_to_image(texts, font=None):
    img_result = create_default_image((0,0))
    empty_start = True
    for txt, color in texts:
        im = draw_text_to_image(txt, color, empty_start=empty_start, empty_end=False, font=font)
        empty_start = False
        img_result = concatenate(img_result, im)
    img_result = concatenate(img_result, create_default_image((11,11)))
    return img_result


def build_img(img, size=(11,11)):
    tb_img = TimeBoxImage()
    rgb_im = img.convert('RGB')
    rgb_im = rgb_im.resize((size[0], size[1]))
    for x in range(rgb_im.width):
        for y in range(rgb_im.height):
            r,g,b=rgb_im.getpixel((x,y))
            tb_img.put_pixel(x,y,r>>4,g>>4,b>>4)
    return tb_img


def load_image(file, sz=(11,11)):
    with Image.open(file).convert("RGBA") as imagedata:
        return build_img(imagedata,sz)

def analyseImage(im):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    im.seek(0)
    return results

def getFrames(im):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(im)['mode']

    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0,0), im.convert('RGBA'))
            yield new_frame

            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    
def load_gif_frames(file,sz=(11,11)):
    data = []
    with Image.open(file) as imagedata:
        for f in getFrames(imagedata):
            data.append(build_img(f,sz))
    return data  
          
if __name__ == "__main__":
  pass
