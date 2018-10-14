import pygame
import getopt
import sys

pygame.init()

colors = {
           'BLACK'        : (  0,  0,  0,255),
           'BLACK_2'      : (  0,  0,  0,255),
           'BLACK_3'      : (  0,  0,  0,255),
           'BLACK_4'      : (  0,  0,  0,255),
           'BLACK_5'      : (  0,  0,  0,255),
           'BLACK_6'      : (  0,  0,  0,255),
           'BLACK_7'      : (  0,  0,  0,255),
           'BLACK_8'      : (  0,  0,  0,255),
           'BLACK_9'      : (  0,  0,  0,255),
           'BLACK_10'     : (  0,  0,  0,255),
      'DARK_GRAY'         : ( 84, 84, 84,255),
      'DARK_GRAY_2'       : ( 60, 60, 60,255),
           'GRAY'         : (152,150,152,255),
           'GRAY_2'       : (160,162,160,255),
     'LIGHT_GRAY'         : (255,255,255,255),
           'WHITE'        : (255,255,255,255),
      'DARK_GRAY_BLUE'    : (  0, 30,116,255),
           'GRAY_BLUE'    : (  8, 76,196,255),
     'LIGHT_GRAY_BLUE'    : ( 76,154,236,255),
'VERY_LIGHT_GRAY_BLUE'    : (168,204,236,255),
      'DARK_BLUE'         : (  8, 16,144,255),
           'BLUE'         : ( 48, 50,236,255),
     'LIGHT_BLUE'         : (120,124,236,255),
'VERY_LIGHT_BLUE'         : (188,188,236,255),
      'DARK_PURPLE'       : ( 48,  0,136,255),
           'PURPLE'       : ( 92, 30,228,255),
     'LIGHT_PURPLE'       : (176, 98,236,255),
'VERY_LIGHT_PURPLE'       : (212,178,236,255),
      'DARK_PINK'         : ( 68,  0,100,255),
           'PINK'         : (136, 20,176,255),
     'LIGHT_PINK'         : (228, 84,236,255),
'VERY_LIGHT_PINK'         : (236,174,236,255),
      'DARK_FUCHSIA'      : ( 92,  0, 48,255),
           'FUCHSIA'      : (160, 20,100,255),
     'LIGHT_FUCHSIA'      : (236, 88,180,255),
'VERY_LIGHT_FUCHSIA'      : (236,174,212,255),
      'DARK_RED'          : ( 84,  4,  0,255),
           'RED'          : (152, 34, 32,255),
     'LIGHT_RED'          : (236,106,100,255),
'VERY_LIGHT_RED'          : (236,180,176,255),
      'DARK_ORANGE'       : ( 60, 24,  0,255),
           'ORANGE'       : (120, 60,  0,255),
     'LIGHT_ORANGE'       : (212,136, 32,255),
'VERY_LIGHT_ORANGE'       : (228,196,144,255),
      'DARK_TAN'          : ( 32, 42,  0,255),
           'TAN'          : ( 84, 90,  0,255),
     'LIGHT_TAN'          : (160,170,  0,255),
'VERY_LIGHT_TAN'          : (204,210,120,255),
      'DARK_GREEN'        : (  8, 58,  0,255),
           'GREEN'        : ( 40,114,  0,255),
     'LIGHT_GREEN'        : (116,196,  0,255),
'VERY_LIGHT_GREEN'        : (180,222,120,255),
      'DARK_LIME_GREEN'   : (  0, 64,  0,255),
           'LIME_GREEN'   : (  8,124,  0,255),
     'LIGHT_LIME_GREEN'   : ( 76,208, 32,255),
'VERY_LIGHT_LIME_GREEN'   : (168,226,144,255),
      'DARK_SEAFOAM_GREEN': (  0, 60,  0,255),
           'SEAFOAM_GREEN': (  0,118, 40,255),
     'LIGHT_SEAFOAM_GREEN': ( 56,204,108,255),
'VERY_LIGHT_SEAFOAM_GREEN': (152,226,180,255),
      'DARK_CYAN'         : (  0, 50, 60,255),
           'CYAN'         : (  0,102,120,255),
     'LIGHT_CYAN'         : ( 56,180,204,255),
'VERY_LIGHT_CYAN'         : (160,214,228,255),
}
color_list = {}

def print_usage():
    print("sprite_pattern_mapper.py a python script to map images down to a specified palette, and optionally to dump pattern data for the NES.")
    print("Usage:")
    print(" -h --help this help message")
    print(" --in= input image")
    print(" --out= output image")
    print(" --c= .c file to output pattern and nametable")
    print(" --offset= a static offset to add to all nametable values. This allows you to reserve sprite space at the beginning of the pattern table")
    print(" --RLE dump the nametable in an RLE format")
    print(" --hex dump the nametable and pattern table in hex")
    print(" --attribute gnerate attribute tables")

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
    return (map[index][0], map[index][1], map[index][2], map[index][3])

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
    if pixel.r != color[0]:
        return False
    if pixel.g != color[1]:
        return False
    if pixel.b != color[2]:
        return False
    if pixel.a != color[3]:
        return False
    return True

def create_pattern(image, map, attribute_map):
    #print(image.get_height())
    #print(image.get_width())
    bytes = [0] * int((image.get_height() * image.get_width()) / 4)
    for i in range(image.get_height()):
        for j in range(int(image.get_width()/8)):
            for k in range(8):
                pixel = image.get_at((j*8+k,i))
                attribute_offset = 0
                if attribute_map != None:
                    if i < 240:
                        attribute_offset = 3*attribute_map[16*(int(i/16)) + int(j/2)]
                    else:
                        attribute_offset = 3*attribute_map[256 + 16*(int((i-240)/16)) + int(j/2)]


                #print("x=%x y=%x byte=%x" % (j*8+k,i,(i/8)*(image.get_width()*2)+i%8+j*16))
                if pixel_compare(pixel, map[attribute_offset+1]):
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16]   |= (1<<(7-k))
                if pixel_compare(pixel, map[attribute_offset+2]):
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16+8] |= (1<<(7-k))
                if pixel_compare(pixel, map[attribute_offset+3]):
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16]   |= (1<<(7-k))
                    bytes[(int(i/8))*(image.get_width()*2)+i%8+j*16+8] |= (1<<(7-k))
    return bytes

def create_attributes(image, map):
    #print(image.get_height())
    #print(image.get_width())
    screens = int((image.get_height() + 239)/240)
    attributes = [-1] * (256 * screens)
    #print(attributes)
    for i in range(0,screens):
        for j in range(0,240):
            for k in range(0,image.get_width()):
                pixel = image.get_at((k, 240*i + j))
                if not pixel_compare(pixel, map[0]):
                    for l in range(0,int((len(map)-1)/3)):
                        if pixel_compare(pixel, map[1 + 3*l]) or pixel_compare(pixel, map[2 + 3*l]) or pixel_compare(pixel, map[3 + 3*l]):
                            #print(256*i + 16*int(j/16) + int(k/16))
                            if attributes[256*i + 16*int(j/16) + int(k/16)] == -1:
                                #print("assign %d %d %d as %d=%d" % (i,int(j/16),int(k/16),256*i + 16*int(j/16) + int(k/16),l))
                                attributes[256*i + 16*int(j/16) + int(k/16)] = l
                            else:
                                if attributes[256*i + 16*int(j/16) + int(k/16)] != l:
                                    print("screen %d 16x16 tile %d has too many colors!" % (screens, 16*int(j/16) + int(k/16)))
                                    sys.exit(2)

    for i in range(0,len(attributes)):
        if attributes[i] == -1:
            attributes[i] = 0

    table = [0] * (64*screens)
    for i in range(0,screens):
        for j in range(0,256):
            #print(j)
            if (int(j/16) & 1) == 0:
                #print(" %d"%(64*i + int(j/32)*8 + int((j%16)/2)))
                if (j & 1) == 0:
                    table[64*i + int(j/32)*8 + int((j%16)/2)] += attributes[256*i + j]
                else:
                    table[64*i + int(j/32)*8 + int((j%16)/2)] += (attributes[256*i + j]<<2)
            else:
                #print(" %d"%(64*i + int(j/32)*8 + int((j%16)/2)))
                if (j & 1) == 0:
                    table[64*i + int(j/32)*8 + int((j%16)/2)] += (attributes[256*i + j]<<4)
                else:
                    table[64*i + int(j/32)*8 + int((j%16)/2)] += (attributes[256*i + j]<<6)

    #for i in range(0,int(len(attributes)/16)):
    #    print("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d"%(            attributes[i*16+0],            attributes[i*16+1],            attributes[i*16+2],            attributes[i*16+3],            attributes[i*16+4],            attributes[i*16+5],            attributes[i*16+6],            attributes[i*16+7],            attributes[i*16+8],            attributes[i*16+9],            attributes[i*16+10],            attributes[i*16+11],            attributes[i*16+12],            attributes[i*16+13],            attributes[i*16+14],            attributes[i*16+15]))

    #print(attributes)
    #print(table)
    return table,attributes

def create_nametable(pattern, offset):
    nametable = [-1] * int(len(pattern)/16)
    reduced_pattern = [0] * len(pattern)
    nametable_index = 0

    for i in range(0,len(nametable)):
        if nametable[i] == -1:
            nametable[i] = nametable_index + offset
            for j in range(0,16):
                reduced_pattern[nametable_index*16 + j] = pattern[i*16 + j]

            for j in range(i+1,len(nametable)):
                same = 1
                for k in range(0,16):
                    if reduced_pattern[nametable_index*16 + k] != pattern[j*16 + k]:
                        same = 0
                if same == 1:
                    nametable[j] = nametable_index + offset
            nametable_index += 1

    #k = 0
    #for i in range(int(image.get_height()/8)):
    #    for j in range(int(image.get_width()/8)):
    #        bytes[i*int(image.get_width()/8) + j] = k
    #        k += 1
    return reduced_pattern[0:nametable_index*16], nametable

def create_nametable_horizontal_screens(pattern):
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

def create_rle( nametable ):
    histo = [0]*256
    key = -1
    rle = []
    count = 1
    pre = -1

    for data in nametable:
        histo[data] += 1

    for i in range(1,len(histo)):
        if histo[i] == 0:
            key = i
            break

    if key == -1:
        return -1

    rle.append(key)
    pre = nametable[0]

    for i in range(1,len(nametable)):
        if nametable[i] != pre or count == 256 or i == len(nametable)-1:
            if count == 1:
                rle.append(pre)
                pre = nametable[i]
                if i == len(nametable)-1:
                    rle.append(nametable[i])
            elif count == 2:
                rle.append(pre)
                rle.append(pre)
                pre = nametable[i]
                if i == len(nametable)-1:
                    rle.append(nametable[i])
            else:
                rle.append(pre)
                rle.append(key)
                if i == len(nametable)-1:
                    rle.append(count)
                else:
                    rle.append(count-1)
            pre = nametable[i]
            count = 1
        else:
            count += 1

    rle.append(key)
    rle.append(0)

    return rle

def main():
    in_file = None
    out_file = None
    image = None
    out_image = None
    map = None
    c_file = None
    offset = 0
    rle = False
    hex_option = False
    attribute_option = False

    short_options = ":h"
    long_options = ["help", "in=", "out=", "map=", "c=", "offset=", "RLE", "hex", "attribute"]
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
                if tmp_color != '':
                    tmp2 = tmp_color.split(",")
                    map.append((int(tmp2[0]),int(tmp2[1]),int(tmp2[2]),int(tmp2[3])))
        if option == "--c":
            c_file = argument
        if option == "--offset":
            offset = int(argument)
        if option == "--RLE":
            rle = True
        if option == "--hex":
            hex_option = True
        if option == "--attribute":
            attribute_option = True

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
        attribute_map = None
        c_attribute_table = None
        if attribute_option == True:
            c_attribute_table, attribute_map = create_attributes(out_image, map)
        c_pattern_table = create_pattern(out_image, map, attribute_map)
        c_reduced_pattern, c_name_table = create_nametable(c_pattern_table, offset)
        if rle == True:
            c_rle_name_table = create_rle(c_name_table)

        c_handle = open(c_file, 'w')
        c_handle.write("unsigned char pattern[%d] = {" % (len(c_reduced_pattern)))
        for i in range(len(c_reduced_pattern)):
            if hex_option == True:
                c_handle.write("0x%02X," % (c_reduced_pattern[i]))
            else:
                c_handle.write("%d," % (c_reduced_pattern[i]))
        c_handle.write("};\n")
        if rle == True:
            c_handle.write("unsigned char rle_nametable[%d] = {" % (len(c_rle_name_table)))
            for i in range(len(c_rle_name_table)):
                if hex_option == True:
                    c_handle.write("0x%02X," % (c_rle_name_table[i]))
                else:
                    c_handle.write("%d," % (c_rle_name_table[i]))
            c_handle.write("};\n")
        else:
            c_handle.write("unsigned char nametable[%d] = {" % (len(c_name_table)))
            for i in range(len(c_name_table)):
                if hex_option == True:
                    c_handle.write("0x%02X," % (c_name_table[i]))
                else:
                    c_handle.write("%d," % (c_name_table[i]))
            c_handle.write("};\n")
        if attribute_option == True:
            c_handle.write("unsigned char attributes[%d] = {" % (len(c_attribute_table)))
            for i in range(len(c_attribute_table)):
                if hex_option == True:
                    c_handle.write("0x%02X," % (c_attribute_table[i]))
                else:
                    c_handle.write("%d," % (c_attribute_table[i]))
            c_handle.write("};\n")

        c_handle.close()
        #print(len(c_pattern_table))

    try:
        pygame.image.save(out_image, out_file)
    except pygame.error as error:
        print(error)
        sys.exit(2)

if __name__ == '__main__':
    main()
