import pygame
import getopt
import sys

pygame.init()

color_list = {}

def print_usage():
    print("sprite_pattern_mapper.py a python script to map images down to a specified palette, and optionally to dump pattern data for the NES.")
    print("Usage:")
    print(" -h --help this help message")
    print(" --in= input image")
    print(" --out= output image")
    print(" --c= .c file to output pattern and nametable")

def palette_map(pixel, map):
    index = 0
    diff = None
    for i in range(len(map)):
        tmp_diff = 0
        if map[i][0] >= pixel.r:
            tmp_diff += map[i][0] - pixel.r
        else:
            tmp_diff += pixel.r - map[i][0]
        if map[i][1] >= pixel.g:
            tmp_diff += map[i][1] - pixel.g
        else:
            tmp_diff += pixel.g - map[i][1]
        if map[i][2] >= pixel.b:
            tmp_diff += map[i][2] - pixel.b
        else:
            tmp_diff += pixel.b - map[i][2]
        if diff == None or tmp_diff < diff:
            index = i
            diff = tmp_diff
    return (map[index][2], map[index][1], map[index][0], map[index][3])

def sort_value(key):
    global color_list
    return color_list[key]

def get_most_used_colors(image, count):
    global color_list
    color_list = {}
    #print(image.get_height())
    #print(image.get_width())
    for i in range(image.get_height()):
        for j in range(image.get_width()):
            #print("%d,%d" % (i, j))
            color = image.get_at((j,i))
            if (color.r, color.g, color.b, color.a) not in color_list:
                color_list[(color.r, color.g, color.b, color.a)] = 1
            else:
                color_list[(color.r, color.g, color.b, color.a)] += 1
    print("raw list")
    print(color_list)
    color_list = sorted(color_list, key = sort_value, reverse = True)
    print("sorted list")
    print(color_list)
    print("final list")
    print(color_list[:count])
    return color_list[:count]

def pixel_compare(pixel, color):
    #print("%X %X %X %X" % (pixel.r, pixel.g, pixel.b, pixel.a))
    if pixel.r != color[2]:
        return False
    if pixel.g != color[1]:
        return False
    if pixel.b != color[0]:
        return False
    if pixel.a != color[3]:
        return False
    return True

def create_pattern(image, map):
    #print(image.get_height())
    #print(image.get_width())
    bytes = [0] * int((image.get_height() * image.get_width()) / 4)
    for i in range(image.get_height()):
        for j in range(int(image.get_width()/8)):
            for k in range(8):
                pixel = image.get_at((j*8+k,i))
                #print("x=%x y=%x byte=%x" % (j*8+k,i,(i/8)*(image.get_width()*2)+i%8+j*16))
                if pixel_compare(pixel, map[1]):
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16]   |= (1<<(7-k))
                if pixel_compare(pixel, map[2]):
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16+8] |= (1<<(7-k))
                if pixel_compare(pixel, map[3]):
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16]   |= (1<<(7-k))
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16+8] |= (1<<(7-k))
    return bytes

def create_nametable(pattern):
    nametable = [-1] * int(len(pattern)/16)
    reduced_pattern = [0] * len(pattern)
    nametable_index = 0
    screens = int((len(nametable)+959)/960)
    
    for m in range(0,screens):
        for i in range(0,960):
            if nametable[m*960+i] == -1:
                nametable[m*960+i] = nametable_index
                for j in range(0,16):
                    reduced_pattern[nametable_index*16 + j] = pattern[((i%30) * 32*screens + m * 32 + int(i/30))*16 + j]
                    
                for n in range(m, screens):
                    start = 0
                    if n == m:
                        start = (n*960+i)+1
                    else:
                        start = 0
                    for j in range(start,960):
                        same = 1
                        for k in range(0,16):
                            #print("j=%d screens=%d n=%d k=%d length=%d index=%d" % (j, screens, n, k, len(pattern), int((int(j/32) * 32*screens + n * 32 + j%32)*16) + k))
                            if reduced_pattern[nametable_index*16 + k] != pattern[((j%30) * 32*screens + n * 32 + int(j/30))*16 + k]:
                                same = 0
                        if same == 1:
                            nametable[n*960+j] = nametable_index
                nametable_index += 1
    
    #k = 0
    #for i in range(int(image.get_height()/8)):
    #    for j in range(int(image.get_width()/8)):
    #        bytes[i*int(image.get_width()/8) + j] = k
    #        k += 1
    return reduced_pattern[0:nametable_index*16], nametable

def main():
    in_file = None
    out_file = None
    image = None
    out_image = None
    map = None
    c_file = None

    short_options = ":h"
    long_options = ["help", "in=", "out=", "map=", "c="]
    try:
        options, arguments = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as error:
        print(error)
        print_usage()
        sys.exit(2)

    for option, argument in options:
        if option == "-h" or option == "--help":
            print_usage()
            sys.exit()
        if option == "--i" or option == "--in":
            in_file = argument
        if option == "--o" or option == "--out":
            out_file = argument
        if option == "--map":
            map = []
            tmp = argument.split(":")
            for tmp_color in tmp:
                tmp2 = tmp_color.split(",")
                map.append((int(tmp2[0]),int(tmp2[1]),int(tmp2[2]),int(tmp2[3])))
        if option == "--c":
            c_file = argument

    if in_file == None:
        print("input file required")
        print_usage()
        sys.exit(2)
    if out_file == None:
        print("output file required")
        print_usage()
        sys.exit(2)

    try:
        image = pygame.image.load(in_file)
    except pygame.error as error:
        print(error)
        sys.exit(2)

    out_image = image.copy()

    #print(image.get_height())
    #print(image.get_width())
    
    if map == None:
        map = get_most_used_colors(image, 4)

    for i in range(out_image.get_height()):
        for j in range(out_image.get_width()):
            pixel = out_image.get_at((j,i))
            #out_image.set_at((j,i), palette_map(pixel, [[89,37,43],[0,0,0],[31,31,31],[63,63,63],[95,95,95],[127,127,127],[159,159,159],[191,191,191],[223,223,223],[255,255,255]]))
            out_image.set_at((j,i), palette_map(pixel, map))
            #if pixel.r == 0 and pixel.g == 0 and pixel.b == 0:
            #    out_image.set_at((j,i), (pixel.r, pixel.g, pixel.b, 0))

    if c_file != None:
        c_pattern_table = create_pattern(out_image, map)
        c_reduced_pattern, c_name_table = create_nametable(c_pattern_table)
        c_handle = open(c_file, 'w')
        c_handle.write("unsigned char pattern[%d] = {" % (len(c_reduced_pattern)))
        for i in range(len(c_reduced_pattern)):
            c_handle.write("0x%02X," % (c_reduced_pattern[i]))
        c_handle.write("};\n")
        c_handle.write("unsigned char nametable[%d] = {" % (len(c_name_table)))
        for i in range(len(c_name_table)):
            c_handle.write("0x%02X," % (c_name_table[i]))
        c_handle.write("};\n")
        c_handle.close()
        #print(len(c_pattern_table))

    try:
        pygame.image.save(out_image, out_file)
    except pygame.error as error:
        print(error)
        sys.exit(2)
    
main()
