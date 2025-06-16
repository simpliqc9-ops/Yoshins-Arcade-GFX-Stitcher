#Used to navigate file directories
#from distutils.command.build_scripts import first_line_re
import os
import importlib
import sys
import time
#import math
#import cython as cy

#DANGEROUTS TO MUCK WITH STUFF UNDER THIS LINE, BE WARNED
var_prefix = "GFX_C"
inter_data = bytes()
#Generate folders if they don't already exist
rompath = r'roms'
if not os.path.exists(rompath):
    os.makedirs(rompath)
gfxpath = r'interleaved_data'
if not os.path.exists(gfxpath):
    os.makedirs(gfxpath)
respath = r'resources'
if not os.path.exists(respath):
    os.makedirs(respath)

gfx_ok = 0
prg_ok = 0


print("---------- YOSHINS ARCADE DATA STITCHER ----------")
game_name = input("Enter ROM name here: ")
#Invalid Input: No Resource file
while not os.path.exists(os.path.join(respath, game_name+".py")):
    print("GAME NOT SUPPORTED! Look in resources")
    game_name = input("Try something else: ")    

#Valid input
print("ROM_Name = ", str(game_name).lower())

#Invalid Input: No ROM Folder
while not os.path.exists(os.path.join(rompath, game_name)):
    print("Oy, there's no ROM folder!")
    os.makedirs(os.path.join(rompath, game_name))
    print("Lemme just fix that!")
#    game_name = input("Try something else: ")    

#Grab the needed resource file
sys.path.append(respath)
res_file = importlib.import_module(game_name.lower()) #Ensure lowercase for ease of input

#Generate folder if it doesn't already exist
out_path = os.path.join(gfxpath,game_name)
if not os.path.exists(out_path):
    os.makedirs(out_path)

#PRINT GFX STATUS
try:
    res_file.gfx_prefix
except:
    print("GFX: = NO")
else:
    gfx_ok = 1
    num_of_gfx_roms = len(res_file.gfx_prefix)
    inter_name = str(game_name).upper() + "_INTERLEAVED_GFX"
    print("GFX: = OK")

    gfx_file = ["{}{}" .format(var_prefix, i) for i in range(1, num_of_gfx_roms + 1)]
#Generate tables for storing data using a dict
    gfx_table = {}
    for i in range (0, num_of_gfx_roms, 1):
        gfx_table.update({i : []})
    #NEO-GEO
    if res_file.System == "Neo-Geo":

    #Fuck you Samsho 1
        try:
            res_file.prefix_override
        except: #Most games will return negative, only do prefix override stuff if the var exists
            filename = ["{}-c{}.c{}".format(res_file.gfx_prefix[i].lower(), i + 1,i + 1) for i in range(0, num_of_gfx_roms)]
    #In the case of games like Samsho 1, you need to be additionally explicit in order to handle the weird c51/c61 prefixes
        else:
            filename = ["{}-c{}.c{}".format(res_file.gfx_prefix[i].lower(), res_file.prefix_override[i], i + 1) for i in range(0, num_of_gfx_roms)]        

    #CPS2
    if res_file.System == "CPS2":
        filename = ["{}.{}m".format(res_file.gfx_prefix[i], res_file.file_writes[i],res_file.file_writes[i]) for i in range(0, num_of_gfx_roms)]
    #CPS1
    if res_file.System == "CPS1" :
        filename = ["{}".format(res_file.gfx_prefix[i]) for i in range(0, num_of_gfx_roms)]
    print("GRAPHICS DATA")
#    print(filename)

    #Validate ROMS
    print("----Graphics ROMS---- {}".format(os.path.join(rompath, game_name)))
    for i in range(0, len(res_file.gfx_prefix), 1):
        if os.path.exists(os.path.join(rompath, game_name, filename[i])):
            print(filename[i], " - OK")
        else:
            print(filename[i], " - DOES NOT EXIST")
    print("----Interleaved Data---- {}".format(out_path))
    if os.path.exists((os.path.join(out_path, inter_name))):
        status = "EXISTS"
    else:
        status = "DOES NOT EXIST"
    print("{} - {}".format(inter_name,status))

#PRINT PRG STATUS
try:
    len(res_file.prg_import)
except:
    inter_prg_name = str(game_name).upper() + "_INTERLEAVED_PRG.bin"
else:
    prg_ok = 1
    print("IMPORT PRG: = OK")
    #Validate ROMS
    print("----Import Program ROMS----")
    for i in range(0, len(res_file.prg_import), 2):
        if os.path.exists(os.path.join(rompath, game_name, res_file.prg_import[i])):
            print(res_file.prg_import[i], " - OK")
        else:
            print(res_file.prg_import[i], " - DOES NOT EXIST")
    ####Print status of 
    try:
        res_file.import_swapendian
    except:
        print("Import Endian - Default")
    else:
        print("Import Endian - Swapped")

try:
    res_file.prg_prefix
except:
    inter_prg_name = str(game_name).upper() + "_INTERLEAVED_PRG.bin"
else:
    prg_ok = 1
    inter_prg_name = str(game_name).upper() + "_INTERLEAVED_PRG.bin"
    print("INTERLEAVE PRG: = OK")
    #Validate ROMS
    print("----De-Interleaved Program ROMS----")
    for i in range(0, len(res_file.prg_prefix), 1):
        if os.path.exists(os.path.join(rompath, game_name, res_file.prg_prefix[i])):
            print(res_file.prg_prefix[i], " - OK")
        else:
            print(res_file.prg_prefix[i], " - DOES NOT EXIST")
        ####Print status of 
    try:
        res_file.swapendian
    except:
        print("Interleave Endian - Default")
    else:
        print("Interleave Endian - Swapped")

try:
    len(res_file.prg_append)
except:
    inter_prg_name = str(game_name).upper() + "_INTERLEAVED_PRG.bin"
else:
    prg_ok = 1
    print("APPEND PRG: = OK")
    #Validate ROMS
    print("----Append Program ROMS----")
    for i in range(0, len(res_file.prg_append), 2):
        if os.path.exists(os.path.join(rompath, game_name, res_file.prg_append[i])):
            print(res_file.prg_append[i], " - OK")
        else:
            print(res_file.prg_append[i], " - DOES NOT EXIST")
    ####Print status of 
    try:
        res_file.append_swapendian
    except:
        print("Append Endian - Default")
    else:
        print("Append Endian - Swapped")

if os.path.exists(os.path.join(out_path, inter_prg_name)):
    print(inter_prg_name, " - EXISTS")
else:
    print(inter_prg_name, " - DOES NOT EXIST")

#Make a folder for the game ROM is there isn't one already
gamepath = os.path.join(rompath, game_name)
if not os.path.exists(gamepath):
    os.makedirs(gamepath)

script_action = input("Great, now what? 1:Interleave 2: De-Interleave: ")

#Invalid Input
while script_action != "1" and script_action != "2":
    print("Why'd ya do that? Now ya just look silly")
    script_action = input("Try something else: ")  
if gfx_ok == 1:
    print(inter_name)
#Assign appropriate names/vars to be used later

#Valid Input 1
if script_action == "1":
    print("Interleaving, please wait...")
#Valid Input 2
if script_action == "2":
    print("De-Interleaving, please wait...")

#Allocate Filenames if PRG is prepped for interleaving
if prg_ok == 1:
    try:
        res_file.prg_prefix
    except:
        print("No interleave data")
    else:
        prg_filename = ["{}".format(res_file.prg_prefix[i]) for i in range(0, len(res_file.prg_prefix))]
        print("DE-INTERLEAVED PROGRAM DATA")
        print(prg_filename)



#Allocate Filenames if GFX is prepped for interleaving
#if gfx_ok == 1:


#Display some info, mostly aesthetic if i'm honest
print("System =", res_file.System)
#print(filename)

def Interleave_PRG():
#Go through every file based on it's group
    prg_table = []
    out_table = []
 #Append remainder of data if need be
    try:
        res_file.prg_import
    except:
        print("No initial data to import")
    else:
        print("Now importing data...")
        #Define the beginning of previous data to append the new data
        import_data = {}
        import_flipped_data = {}
        for x in range(0, len(res_file.prg_import), 2):
            import_data.update({x>>1 : []})
            print("Import X - ", x)
            print("Import Name - ", res_file.prg_import[x])
            print("Import Size - ", res_file.prg_import[x+1])
            with open((os.path.join(gamepath, res_file.prg_import[x])), "rb") as PRG1:
                import_data[x>>1] = PRG1.read(res_file.prg_import[x+1])
#####CHECK IF THE ENDIAN OF THE DATA SHOULD BE SWAPPED#####        
                try:
                    res_file.import_swapendian
                except:
                    print("writing appended data...")
                    out_table += import_data[x>>1]
                else: #Swap the Endian of the data before it's written
                    import_flipped_data.update({x>>1 : []})
                    for v in range(res_file.import_swapendian, (res_file.prg_import[x+1]) + res_file.import_swapendian, res_file.import_swapendian):
                        for b in range(-1, -res_file.import_swapendian-1, -1):
                            import_flipped_data[x>>1] += import_data[x>>1][v + b:  v + b + 1]
                    print("writing flipped appended data...")
                    out_table += import_flipped_data[x>>1]
 
    try:
        res_file.prg_prefix #Check if interleacving should be goin on
    except:
        print("-----")
    else:
        b = 0
        k = 0
        print("---Interleaving PRG---")
        for i in range(0,len(prg_filename), res_file.prg_groupsize[k]):
            if res_file.prg_groupsize[b] == 2:
                print("Group ", b+1)
                print("Interleaving - ", prg_filename[k], prg_filename[k+1])
    #            print(prg_filename[k+1])
                with open((os.path.join(gamepath, prg_filename[k])), "rb") as PRG1:
                    with open((os.path.join(gamepath, prg_filename[k+1])), "rb") as PRG2:
                            for j in range(0, res_file.prg_romsize[b], res_file.prg_grabsize[b]):
                                prg_table += PRG1.read(res_file.prg_grabsize[b])
                                prg_table += PRG2.read(res_file.prg_grabsize[b])
            if res_file.prg_groupsize[b] == 4:
                print("Group ", b+1)
                print("Interleaving - ", prg_filename[k], prg_filename[k+1], prg_filename[k+2], prg_filename[k+3])
                with open((os.path.join(gamepath, prg_filename[k])), "rb") as PRG1:
                    with open((os.path.join(gamepath, prg_filename[k+1])), "rb") as PRG2:
                        with open((os.path.join(gamepath, prg_filename[k+2])), "rb") as PRG3:
                            with open((os.path.join(gamepath, prg_filename[k+3])), "rb") as PRG4:
                                for j in range(0, res_file.prg_romsize[b], res_file.prg_grabsize[b]):
                                    prg_table += PRG1.read(res_file.prg_grabsize[b])
                                    prg_table += PRG2.read(res_file.prg_grabsize[b])
                                    prg_table += PRG3.read(res_file.prg_grabsize[b])
                                    prg_table += PRG4.read(res_file.prg_grabsize[b])
            k += res_file.prg_groupsize[b]
            b += 1
    #####CHECK IF THE ENDIAN OF THE DATA SHOULD BE SWAPPED#####        
        try:
            res_file.swapendian
        except:
            with open((os.path.join(gfxpath, inter_prg_name)), "wb") as Output:
                Output.write(bytes(prg_table))
                out_table += prg_table
        else: #Swap the Endian of the data before it's written
            print("Now swapping the Endian...")
            flipped_table = []
            for i in range(res_file.swapendian, sum(res_file.prg_romsize) * len(prg_filename) + res_file.swapendian, res_file.swapendian):
                for k in range(-1, -res_file.swapendian-1, -1):
                    flipped_table += prg_table[i + k:  i + k + 1]
    #Write the altered data
            out_table += flipped_table
#            with open((os.path.join(gfxpath, inter_prg_name)), "wb") as Output:
    #            print(sum(res_file.prg_romsize))
#                print(len(flipped_table))
#                Output.write(bytes(flipped_table))

#Append remainder of data if need be
    try:
        res_file.prg_append
    except:
        print("Finished reading PRG ROMs")
    else:
        print("Now appending data...")
        #Define the beginning of previous data to append the new data
#        try:
#            res_file.swapendian
#        except:
#            append_start = sum(res_file.prg_romsize) * len(prg_filename)
#        append_start = sum(res_file.prg_romsize) * len(prg_filename)
        append_data = {}
        append_flipped_data = {}
#        if not os.path.exists(((os.path.join(gfxpath, inter_prg_name)))):
#            with open((os.path.join(gfxpath, inter_prg_name)), "wb") as Output:
#                Output.write()
        for x in range(0, len(res_file.prg_append), 2):
            append_data.update({x>>1 : []})
            print("Append X - ", x)
            print("Append Name - ", res_file.prg_append[x])
            print("Append Size - ", res_file.prg_append[x+1])
            with open((os.path.join(gamepath, res_file.prg_append[x])), "rb") as PRG1:
                append_data[x>>1] = PRG1.read(res_file.prg_append[x+1])
#####CHECK IF THE ENDIAN OF THE DATA SHOULD BE SWAPPED#####        
                try:
                    res_file.append_swapendian
                except:
                    print("writing appended data...")
                    out_table += append_data[x>>1]
                else: #Swap the Endian of the data before it's written
                    append_flipped_data.update({x>>1 : []})
                    for v in range(res_file.append_swapendian, (res_file.prg_append[x+1]) + res_file.append_swapendian, res_file.append_swapendian):
                        for b in range(-1, -res_file.append_swapendian-1, -1):
                            append_flipped_data[x>>1] += append_data[x>>1][v + b:  v + b + 1]
                    print("writing flipped appended data...")
                    out_table += append_flipped_data[x>>1]

###WRITE THE FINAL INTERLEAVED DATA
#    with open((os.path.join(gfxpath, inter_prg_name)), "wb") as Output:
    with open((os.path.join(out_path, inter_prg_name)), "wb") as Output:
        Output.write(bytes(out_table))


def De_Interleave_PRG():
####IMPORT DATA FOR LATER
    h = 0
    try:
        res_file.prg_import
    except:
        pass
    else:
        import_prg_table = {}
        with open((os.path.join(out_path, inter_prg_name)), "rb") as Input:
#Offset when the data begins reading if there's interleaved data beforehand
            for h in range(0, len(res_file.prg_import), 2):
                import_prg_table.update({h>>1 : []})
                import_prg_table[h>>1] += Input.read(res_file.prg_import[h+1])
####CHECK TO SEE IF WE SHOULD CHANGE THE ENDIAN OF THE DATA
        try:
            res_file.import_swapendian
        except:
            for h in range(0, len(res_file.prg_append), 2):
                with open((os.path.join(gamepath, res_file.prg_import[h])), "wb") as Appendfile:
                    Appendfile.write(bytes(append_prg_table[h>>1]))
        else: #Swap the Endian of the data before it's written
            import_flipped_table = {}
            for r in range(0, len(res_file.prg_import), 2):
                import_flipped_table.update({r>>1 : []})
                for q in range(res_file.import_swapendian, res_file.prg_import[r+1] + res_file.import_swapendian, res_file.import_swapendian):
                    for k in range(-1, -res_file.import_swapendian-1, -1):
                        import_flipped_table[r>>1] += import_prg_table[r>>1][q + k:  q + k + 1]
#Write the flipped data back
            for h in range(0, len(res_file.prg_import), 2):
                with open((os.path.join(gamepath, res_file.prg_import[h])), "wb") as Appendfile:
                    Appendfile.write(bytes(import_flipped_table[h>>1]))

#Go through every file based on it's group
    prg_table = {}
####GRAB INTERLEAVED DATA FOR LATER
    h = 0
    try:
        res_file.prg_prefix
    except:
        pass
    else:
        with open((os.path.join(out_path, inter_prg_name)), "rb") as Input:
            try:
                res_file.prg_import
            except:
                while h < len(res_file.prg_groupsize):
                    prg_table.update({h : []})
                    prg_table[h] += Input.read((res_file.prg_romsize[h]) * (res_file.prg_groupsize[h]))
                    h += 1
            else:
                for q in range(0, len(res_file.prg_import),2):
                    Input.read(res_file.prg_import[q+1])

                while h < len(res_file.prg_groupsize):
                    prg_table.update({h : []})
                    prg_table[h] += Input.read((res_file.prg_romsize[h]) * (res_file.prg_groupsize[h]))
                    h += 1


        out_table = {}

        for i in range (0, len(res_file.prg_prefix), 1):
            out_table.update({i : []})
        b = 0
        k = 0
        print("---De-Interleaving PRG---")
        for i in range(0,len(prg_filename), res_file.prg_groupsize[k]):
            with open((os.path.join(out_path, inter_prg_name)), "rb") as Input:
                if res_file.prg_groupsize[b] == 2:
                    print("Group ", b+1)
                    print("De-Interleaving - ", prg_filename[k], prg_filename[k+1])
                    for j in range(0, res_file.prg_romsize[b] << 1, res_file.prg_grabsize[b] << 1):
                        out_table[k] += prg_table[b][j : j + res_file.prg_grabsize[b]]
                        out_table[k+1] += prg_table[b][j + res_file.prg_grabsize[b] : j + (res_file.prg_grabsize[b] * 2)]

                if res_file.prg_groupsize[b] == 4:
                    print("Group ", b+1)
                    print("De-Interleaving - ", prg_filename[k], prg_filename[k+1], prg_filename[k+2], prg_filename[k+3])
                    for j in range(0, res_file.prg_romsize[b] << 2, res_file.prg_grabsize[b] << 2):
                        out_table[k] += prg_table[b][j : j + res_file.prg_grabsize[b]]
                        out_table[k+1] += prg_table[b][j + res_file.prg_grabsize[b] : j + (res_file.prg_grabsize[b] * 2)]
                        out_table[k+2] += prg_table[b][j + (res_file.prg_grabsize[b] * 2) : j + (res_file.prg_grabsize[b] * 3)]
                        out_table[k+3] += prg_table[b][j + (res_file.prg_grabsize[b] * 3) : j + (res_file.prg_grabsize[b] * 4)]

                k += res_file.prg_groupsize[b]
                b += 1
        try:
            res_file.swapendian
        except:
    #Write the PRG Data back
            for l in range(0,len(prg_filename), 1):
                with open((os.path.join(gamepath, prg_filename[l])), "wb") as output:
                    output.write(bytes(out_table[l]))
        #            print(l)
        #            output.write(bytes(0))
        else: #Swap the Endian of the data before it's written
            print("Now swapping the Endian...")
    #Generate tables to push the data back in to, flipped back to it's original state
            flipped_table = {}
            for i in range(0, len(prg_filename), 1):
                flipped_table.update({i : []})
            for m in range(0, len(prg_filename), 1):
                for i in range(res_file.swapendian, sum(res_file.prg_romsize) + res_file.swapendian, res_file.swapendian):
                    for k in range(-1, -res_file.swapendian-1, -1):
                        flipped_table[m] += out_table[m][i + k:  i + k + 1]
    #Write the PRG Data back
            for l in range(0,len(prg_filename), 1):
                with open((os.path.join(gamepath, prg_filename[l])), "wb") as output:
                    output.write(bytes(flipped_table[l]))
                    print(len(flipped_table[l]))


####GRAB APPENDED DATA FOR LATER
    h = 0
    try:
        res_file.prg_append
    except:
        pass
    else:
        append_prg_table = {}
        with open((os.path.join(gfxpath, inter_prg_name)), "rb") as Input:
            ###Just to be safe, read data until the start of appended data
            try:
                res_file.prg_prefix
            except:
                for h in range(0, len(res_file.prg_append), 2):
                    append_prg_table.update({h>>1 : []})
                    append_prg_table[h>>1] += Input.read(res_file.prg_append[h+1])
            else:
#Offset when the data begins reading if there's interleaved data beforehand
                for s in range(0, len(res_file.prg_groupsize), 1):
                    Input.read((res_file.prg_romsize[s]) * (res_file.prg_groupsize[s]))
            try:
                res_file.prg_import
            except:
                for h in range(0, len(res_file.prg_append), 2):
                    append_prg_table.update({h>>1 : []})
                    append_prg_table[h>>1] += Input.read(res_file.prg_append[h+1])
            else:
#Offset when the data begins reading if there's interleaved data beforehand
                for q in range(0, len(res_file.prg_import),2):
                    Input.read(res_file.prg_import[q+1])

                for h in range(0, len(res_file.prg_append), 2):
                    append_prg_table.update({h>>1 : []})
                    append_prg_table[h>>1] += Input.read(res_file.prg_append[h+1])
#                h += 1
####CHECK TO SEE IF WE SHOULD CHANGE THE ENDIAN OF THE DATA
        try:
            res_file.append_swapendian
        except:
            for h in range(0, len(res_file.prg_append), 2):
                with open((os.path.join(gamepath, res_file.prg_append[h])), "wb") as Appendfile:
                    Appendfile.write(bytes(append_prg_table[h>>1]))
        else: #Swap the Endian of the data before it's written
            append_flipped_table = {}
            for r in range(0, len(res_file.prg_append), 2):
                append_flipped_table.update({r>>1 : []})
                for q in range(res_file.append_swapendian, res_file.prg_append[r+1] + res_file.append_swapendian, res_file.append_swapendian):
                    for k in range(-1, -res_file.append_swapendian-1, -1):
                        append_flipped_table[r>>1] += append_prg_table[r>>1][q + k:  q + k + 1]
#Write the flipped data back
            for h in range(0, len(res_file.prg_append), 2):
                with open((os.path.join(gamepath, res_file.prg_append[h])), "wb") as Appendfile:
                    Appendfile.write(bytes(append_flipped_table[h>>1]))


#Function used to write data to interleaved files
def grab_inter_data(i,in1,in2):
    temp = []
    for k in range (0, res_file.gfx_romsize[i>>1], 2):
        temp += in1[k:k+2]
        temp += in2[k:k+2]
    return temp
#        gfx_table[0] += bytes(gfx_file[i].read(2))
#        gfx_table[0] += bytes(gfx_file[i+1].read(2))

#Function used to write data to C files
def grab_Cx_data(x, inp):
    for i in range (0, res_file.gfx_romsize[x>>1] >> 1, 1):
#        print("interleave", i)
        gfx_table[x] += bytes(inp.read(2))
        gfx_table[x+1] += bytes(inp.read(2)) 

#//////////////////// START OF CASE NEO-GEO ////////////////////
def CASE_NEO_GEO():
#///// INTERLEAVE DATA ///////////////
    if script_action == "1":
   #Grab data from the interleaved GFX file
        for i in range (0, num_of_gfx_roms, 2):
#        if os.path.exists(os.path.join(gamepath, filename[i])):
            with open (os.path.join(gamepath, filename[i]), "rb") as in1:
                with open (os.path.join(gamepath, filename[i+1]), "rb") as in2:
                    temp1 = in1.read()
                    temp2 = in2.read()
                    print("Interleaving", filename[i], filename[i+1])
                    gfx_table[0] += grab_inter_data(i,temp1,temp2)

        #Write the final interleaved data
        with open (os.path.join(out_path, inter_name), "wb") as Interleaved_GFX:   
            Interleaved_GFX.write(bytes(gfx_table[0]))

#///// DE-INTERLEAVE DATA ////////////
    if script_action == "2":
    #Grab data from the interleaved GFX file
        with open (os.path.join(out_path, inter_name), "rb") as Interleaved_GFX:   
            for i in range (0, num_of_gfx_roms, 2):
                print("De-Interleaving", filename[i], filename[i+1])
                grab_Cx_data(i,Interleaved_GFX)

    #Write the final Cx data
        for k in range (0, num_of_gfx_roms, 1):
            with open (os.path.join(gamepath, filename[k]), "wb") as gfx_file[k]:
                gfx_file[k].write(bytes(gfx_table[k]))

#//////////////////// END OF CASE NEO-GEO ////////////////////


#1. Split each base ROM into its even and odd words.
#2. Interleave these on a word basis into eight files: The 13-15 evens, 
#the 13-15 odds, the 17-19 evens, the 17-19 odds, the 14-16 evens, 
#the 14-16 odds, the 18-20 evens, and the 18-20 odds.
#3. Interleave each half's evens together and each half's odds together, 
#both on a 64-byte basis. You should now have four files: the 13-15-17-19 
#evens, the 13-15-17-19 odds, the 14-16-18-20 evens, and the 14-16-18-20 odds.
#4. Interleave each half's odds and evens with each other on a 1,048,576-byte 
#basis: You should now have two files, the 13-15-17-19 and the 14-16-18-20.
#5. Append the latter to the former.

#Holds the EVEN and ODD Bytes in as many tables as there are GFX Roms
def grab_ROM_Data(v,gfx,gfx2,gfx3,gfx4):
    romsize = res_file.gfx_romsize
    temp = {}
    for b in range(4):
        temp.update({b : []})
#    temp[0],temp[1],temp[2],temp[3] = [],[],[],[]
    length = romsize[v>>2]
#    index1,index2,index3,index4 = v,v+1,v+2,v+3
    index1,index2,index3,index4 = 0,1,2,3
    print(hex(length))
    print(hex(romsize[v>>2]))
#    print(hex(len(gfx[v])))
#    print(hex(len(gfx[v+1])))
#    print(hex(len(gfx[v+2])))
#    print(hex(len(gfx[v+3])))
    for newk in range(0,length,4):
#        print(hex(newk))
#Within each of those chunks, words from two of the associated base 
#ROMs are interleaved for each 8x8 subtile (64 bytes). The ROMs read 
#from alternate between each subtile. Meaning the first subtile is 
#comprised of interleaved words form the first two of the four associate 
#ROMs, the next tile is comprised of interleaved words from the second 
#two of the four associate ROMs. So, for example, the very first subtile
#would be comprised of alternating words from ROMs 13 and 15, the second 
#would comprised of alternating words from ROMs 17 and 19, the third would 
#switch back to alternating words from ROMs 13 and 15... etc.
#            start1 = k
#            end1 = start1+2
#            start2 = end1
#            end2 = start2+2
        #Table 0 stores the EVEN Bytes for 13/15m
        temp[index1] += gfx[newk:newk+2] #13m #14m
        temp[index1] += gfx2[newk:newk+2] #15m #16m
        #Table 1 stores the ODD Bytes for 13/15m
        temp[index2] += gfx[newk+2:newk+4] #17m #18m
        temp[index2] += gfx2[newk+2:newk+4] #19m #20m
        #Table 2 stores the EVEN Bytes for 17/19m
        temp[index3] += gfx3[newk:newk+2] #13m #14m
        temp[index3] += gfx4[newk:newk+2] #15m #16m
        #Table 3 stores the ODD Bytes for 17/19m
        temp[index4] += gfx3[newk+2:newk+4] #17m #18m
        temp[index4] += gfx4[newk+2:newk+4] #19m #20m

#            tempfile[i] += gfx[i][start1:end1] #13m #14m
#            tempfile[i] += gfx[i+1][start1:end1] #15m #16m
        #Table 1 stores the ODD Bytes for 13/15m
#            tempfile[i+1] += gfx[i][start2:end2] #17m #18m
#            tempfile[i+1] += gfx[i+1][start2:end2] #19m #20m
        #Table 2 stores the EVEN Bytes for 17/19m
#            tempfile[i+2] += gfx[i+2][start1:end1] #13m #14m
#            tempfile[i+2] += gfx[i+3][start1:end1] #15m #16m
        #Table 3 stores the ODD Bytes for 17/19m
#            tempfile[i+3] += gfx[i+2][start2:end2] #17m #18m
#            tempfile[i+3] += gfx[i+3][start2:end2] #19m #20m
        #Table 0 stores the EVEN Bytes for 13/15m
#            tempfile[i] += gfx_file[i].read(2) #13m #14m
#            tempfile[i] += gfx_file[i+1].read(2) #15m #16m
        #Table 1 stores the ODD Bytes for 13/15m
#            tempfile[i+1] += gfx_file[i].read(2) #17m #18m
#            tempfile[i+1] += gfx_file[i+1].read(2) #19m #20m
        #Table 2 stores the EVEN Bytes for 17/19m
#            tempfile[i+2] += gfx_file[i+2].read(2) #13m #14m
#            tempfile[i+2] += gfx_file[i+3].read(2) #15m #16m
        #Table 3 stores the ODD Bytes for 17/19m
#            tempfile[i+3] += gfx_file[i+2].read(2) #17m #18m
#            tempfile[i+3] += gfx_file[i+3].read(2) #19m #20m
#        print("interleave", k)
#    for j in range (0, res_file.gfx_romsize[i>>2], 64):
    #    ["-------------- table 0 --------------"]
    print(filename[0],filename[1],"EVEN",hex(len(temp[0])))
#    ["-------------- table 1 --------------"]
    print(filename[0],filename[1],"ODD",hex(len(temp[1])))
#    ["-------------- table 2 --------------"]
    print(filename[2],filename[3],"EVEN",hex(len(temp[2])))
#    ["-------------- table 3 --------------"]
    print(filename[2],filename[3],"ODD",hex(len(temp[3])))


    j = 0
    l = 64
    order = [0,0,1,1]
#    order = [0,1,0,1]
    #ssf2t
    while j < (res_file.gfx_romsize[v>>2]) << 1:
#Interleave every 64 Bytes between groups
        #The first table stores the EVEN WORDs of the 
        #group
        #Grab 64 bytes from the 13/15 EVEN WORDs table
        tempfile2[(v >> 1) + order[0]] += temp[0][j:j+l]
        #Grab 64 bytes from the 17/19 EVEN WORDs table
        tempfile2[(v >> 1) + order[1]] += temp[2][j:j+l]
        #The second table stores the ODD WORDs of the 
        #group
        #Grab 64 bytes from the 13/15 ODD WORDs table
        tempfile2[(v >> 1) + order[2]] += temp[1][j:j+l]
        #Grab 64 bytes from the 17/19 ODD WORDs table
        tempfile2[(v >> 1) + order[3]] += temp[3][j:j+l]
        j += l
#    ["-------------- table2 - 0 --------------"]
    print(filename[v],filename[v+1],filename[v+2],filename[v+3],"EVEN")
#    ["-------------- table2 - 1--------------"]
    print(filename[v],filename[v+1],filename[v+2],filename[v+3],"ODD")

    j = 0
    while j < (romsize[v>>2]) << 2:
        #Table 0 stores the EVEN Bytes for 13/15m, 17/19m
        #Table 1 stores the ODD Bytes for 13/15m, 17/19m
        #Table 2 stores the EVEN Bytes for 17/19m
        #Table 3 stores the ODD Bytes for 17/19m
        tempfile3[v>>2] += tempfile2[(v>>1)][j:j+(2 << 19)]
        tempfile3[v>>2] += tempfile2[(v>>1) + 1][j:j+(2 << 19)]
        j += 2 << 19 #Add offset to grab the right data
    return tempfile3[v>>2] #gfx_table[0]

def cps2_de_interleave1(inp, loopindex):
    #Properly retrieve each "Group" of Even and Odd Bytes
#    ["-------------- table2 - 0 --------------"]
    print(filename[i],filename[i+1],filename[i+2],filename[i+3],"EVEN")
#    ["-------------- table2 - 1--------------"]
    print(filename[i],filename[i+1],filename[i+2],filename[i+3],"ODD")
    j = 0
    while j < (res_file.gfx_romsize[loopindex>>2]) << 2:
        tempfile2[(loopindex >> 1)] += inp[(loopindex>>2)][j:j+(2 << 19)]
        tempfile2[(loopindex >> 1)+1] += inp[(loopindex>>2)][j+(2 << 19):j+(2 << 20)]
        j += 2 << 20


        #Extract each 64 Byte chunk
    j = 0
#    ["-------------- table 0 --------------"]
    print(filename[loopindex],filename[loopindex+1],"EVEN")
#    ["-------------- table 1 --------------"]
    print(filename[loopindex],filename[loopindex+1],"ODD")
#    ["-------------- table 2 --------------"]
    print(filename[loopindex+2],filename[loopindex+3],"EVEN")
#    ["-------------- table 3 --------------"]
    print(filename[loopindex+2],filename[loopindex+3],"ODD")    
    while j < (res_file.gfx_romsize[loopindex>>2]) << 1:
#De-Interleave every 64 Bytes between groups
        #The first table in the group contains the
        #EVEN WORDs of 13/15m
        tempfile[loopindex] += tempfile2[loopindex >> 1][j:j+64]
        #The second table in the group contains the
        #EVEN WORDs of 17/19m
        tempfile[loopindex+2] += tempfile2[loopindex >> 1][j+64:j+128]
        #The third table in the group contains the
        #ODD WORDs of 13/15m
        tempfile[loopindex+1] += tempfile2[(loopindex >> 1)  + 1][j:j+64]
        #The fourth table in the group contains the
        #ODD WORDs of 17/19m
        tempfile[loopindex+3] += tempfile2[(loopindex >> 1) + 1][j+64:j+128]
        j += 128

    j = 0
    while j < res_file.gfx_romsize[loopindex>>2]:
        #At the beginning of interleaving, we stitched
        #the ROMs together 2 bytes  at a time, first
        #Grab 2 bytes from EVEN 13/15m for 13m
        gfx_table[loopindex] += tempfile[loopindex][j:j+2]
        #Grab 2 bytes from EVEN 13/15m for 15m
        gfx_table[loopindex+1] += tempfile[loopindex][j+2:j+4]
        #Grab 2 bytes from ODD 13/15m for 13m
        gfx_table[loopindex] += tempfile[loopindex+1][j:j+2]
        #Grab 2 bytes from 0DD 13/15m for 15m
        gfx_table[loopindex+1] += tempfile[loopindex+1][j+2:j+4]

        #Repeat this process for the other 2 GFX
        #ROMs in the group
        #Grab 2 bytes from EVEN 17/19m for 17m
        gfx_table[loopindex+2] += tempfile[loopindex+2][j:j+2]
        #Grab 2 bytes from EVEN 17/19m for 19m
        gfx_table[loopindex+3] += tempfile[loopindex+2][j+2:j+4]
        #Grab 2 bytes from ODD 17/19m for 17m
        gfx_table[loopindex+2] += tempfile[loopindex+3][j:j+2]
        #Grab 2 bytes from 0DD 17/19m for 19m
        gfx_table[loopindex+3] += tempfile[loopindex+3][j+2:j+4]
        j += 4
#   return gfx_table

#//////////////////// START OF CASE CPS2 ////////////////////
def CASE_CPS2():
#Based on the interleaver by Born2SPD
#///// INTERLEAVE DATA ///////////////
    if script_action == "1":
   #Grab data for the interleaved GFX file
        for i in range(0,num_of_gfx_roms,4):
            with open (os.path.join(gamepath, filename[i]), "rb") as in1:
                with open (os.path.join(gamepath, filename[i+1]), "rb") as in2:
                    with open (os.path.join(gamepath, filename[i+2]), "rb") as in3:
                        with open (os.path.join(gamepath, filename[i+3]), "rb") as in4:
                            gfx_file[i] = in1.read()
                            gfx_file[i+1] = in2.read()
                            gfx_file[i+2] = in3.read()
                            gfx_file[i+3] = in4.read()
                            gfx_table[0] += grab_ROM_Data(i,gfx_file[i],gfx_file[i+1],gfx_file[i+2],gfx_file[i+3])

        #See if a GFX Map exists for the given game. If so, split up each tile type
        try:
            res_file.GFX_MAP
        except:
            print("GFX_MAP: = NO")
        else:
            CPS_write_GFX_types(res_file,gfx_table)

        with open (os.path.join(out_path, inter_name), "wb") as Interleaved_GFX: 
    #            CPS2_Interleave_1048576()
            print("----------------TABLE3----------------")
            for i in range (0,len(tempfile3),1):
                print(len(tempfile3[i]),hex(len(tempfile3[i])))
            print("----------------TABLE2----------------")
            for i in range (0,len(tempfile2),1):
                print(len(tempfile2[i]),hex(len(tempfile2[i])))
            print("----------------TABLE1----------------")
            for i in range (0,len(gfx_file),1):
                print(len(gfx_file[i]),hex(len(gfx_file[i])))
            print("----------------OUTPUT----------------")
            for i in range (0,len(gfx_table),1):
                print(len(gfx_table[i]),hex(len(gfx_table[i])))
            Interleaved_GFX.write(bytes(gfx_table[0]))
    #            Interleaved_GFX.write[tempfile3[0]]

    #///// DE-INTERLEAVE DATA ////////////
    if script_action == "2":
        #Check De-interleave Mode. If omitted, de-interleave combined file, else de-interleave tile types
        #Make a copyu of the interleaved data to determine what to split
        try:
            res_file.DE_INTERLEAVE_MODE
        except:
            print("De-interleave: Mode 0")
            with open (os.path.join(out_path, inter_name), "rb") as Interleaved_GFX:   
                gfx_copy = Interleaved_GFX.read()
        else:
            print("De-interleave: Mode 1")
            gfx_copy = CPS_split_GFX_types(res_file)
    #Grab data from the interleaved GFX file
        b = 0
        for i in range (0, num_of_gfx_roms, 4):
            print("De-Interleaving", filename[i], filename[i+1],filename[i+2],filename[i+3])
            #Grab the groups again
            for k in range(0, len(tempfile3), 1):
                add = (res_file.gfx_romsize[k]) << 2
                tempfile3[k] += gfx_copy[b:b+add]
                b += add
#            gfx_table = cps2_de_interleave1(tempfile3,i)
            cps2_de_interleave1(tempfile3,i)


        print("----------------TABLE3----------------")
        for i in range (0,len(tempfile3),1):
            print(len(tempfile3[i]))
        print("----------------TABLE2----------------")
        for i in range (0,len(tempfile2),1):
            print(len(tempfile2[i]))
        print("----------------TABLE1----------------")
        for i in range (0,len(tempfile),1):
            print(len(tempfile[i]))
        print("----------------OUTPUT----------------")
        for i in range (0,len(gfx_table),1):
            print(len(gfx_table[i]))
        for i in range (0, num_of_gfx_roms, 1):
            with open (os.path.join(gamepath, filename[i]), "wb") as out:
                out.write(bytes(gfx_table[i]))

def write_m_files():
    #Write the final .M data
    for i in range (0, num_of_gfx_roms, 4):
        with open (os.path.join(gamepath, filename[i]), "wb") as gfx_file[i]:
            with open (os.path.join(gamepath, filename[i+1]), "wb") as gfx_file[i+1]: 
                with open (os.path.join(gamepath, filename[i+2]), "wb") as gfx_file[i+2]:
                    with open (os.path.join(gamepath, filename[i+3]), "wb") as gfx_file[i+3]: 
                        gfx_file[i].write(bytes(gfx_table[i]))
                        gfx_file[i+1].write(bytes(gfx_table[i+1]))
                        gfx_file[i+2].write(bytes(gfx_table[i+2]))
                        gfx_file[i+3].write(bytes(gfx_table[i+3]))
#                            print("WIP")
                            #print("De-Interleaving", filename[i], filename[i+1],filename[i+2],filename[i+3])

#//////////////////// END OF CASE CPS2 ////////////////////
### The process for the CPS1 is much and such the same as CPS2, only that due to the varied GFX sizes,
# we don't interleave every 2 << 19 chunk of data. Data is read from each Group, and any remaining data in essence
#"spills" over in to the next one
                        #CPS1 GFX INTERLEAVING STEPS
#    = Copy the files
#    = Go through every Group, making EVEN and ODD tables composed of 4 bytes per half of the group. For instance,
#   SF2 has ROM Groups of 4, each reading 2 bytes apiece. The first table would contain a WORD from each of the 
#   first 2 ROMs, then the next table would have the next 4 bytes.
#    = Interleave these EVEN and ODD tables together a tile apiece, 64 Bytes
#    = Finally, Append that interleaved group data to the output

def generate_split_table():
    split_tab = []
    index = 0
    for i in range(0, len(res_file.group_size), 1):
        temp = 0
        temp2 = 0
        for k in range (0, res_file.group_size[i], 1):
            add = res_file.rom_byte_size[res_file.group_indexes[index+k]-1]
            if temp2 >= 4:
                temp = 1
            else:
                 temp = 0
            split_tab.append(temp)
            temp2 += add
        index += res_file.group_size[i]
    print(split_tab)
    return split_tab

def generate_assemble_sizes():
    temp = 0
    output = []
    comp_table = []
    #First, make a copy of every GFX ROM
    for group in range(0, len(res_file.group_size), 1):
        output.append(0)
        k = 0
    #Gather temp Assemble sizes before comparison
        for index in range(0, res_file.group_size[group], 1):
            group_index = res_file.group_indexes[index+k]-1
            FILE_LOC = os.path.join(gamepath, filename[group_index])
            bytesize = res_file.rom_byte_size[group_index]
#            assemble_size = math.floor(os.path.getsize(FILE_LOC)/bytesize)
            assemble_size = os.path.getsize(FILE_LOC)>>(bytesize-1)
            comp_table.append(assemble_size)
        k +=  res_file.group_size[group]

    #Compare each Assemble size for each group, specifically choosing the smallest number
    temp = comp_table[0]
    k = 0
    for group in range(0, len(res_file.group_size), 1):
        for index2 in range(0, res_file.group_size[group], 1):
            if comp_table[index2+k] < temp:
                temp = comp_table[index2]
        output[group] = temp
        k +=  res_file.group_size[group]
        print("ASSEMBLE_SZZE - ", hex(output[group])) #," - ", hex(bytesize))
    return output

def grab_CPS1_ROM_Data():
    print("Interleaving GFX...")
    time.sleep(1)
    finalsize = 0
    #First, make a copy of every GFX ROM
    for i in range(0, len(res_file.gfx_prefix), 1):
        FILE_LOC = os.path.join(gamepath, filename[i])
        file_length = os.path.getsize(FILE_LOC)
        with open (FILE_LOC, "rb") as inp:
            bytesize = res_file.rom_byte_size[i]
            print(FILE_LOC, " - SIZE = ", hex(file_length), " - ", hex(bytesize))
            gfx_file[i] = inp.read(file_length)
            finalsize += file_length
    print("\tTOTAL SIZE OF GFX ROMS - ", hex(finalsize))

#x-y = Start/End Points of interleaved data
def convert_SCR3(table,x,y):#,x,y):
    temp = table
    out2 = []
    tiles = []
    ev_strips = []
    od_strips = []
    #First, seperate the tiles into even and odd strips of 4 bytes, 8 pixels apiece
    for i in range(x,y,0x08):
        ev_strips += temp[i:i+0x04]
        od_strips += temp[i+0x04:i+0x08]
    #interleave 2 Even tiles first, then 2 Odd tiles
    for i in range(0,len(ev_strips),0x40):
        tiles += ev_strips[i:i+0x40]
        tiles += od_strips[i:i+0x40]
    #At this point, the data resembles the final output, albeit placed incorrectly. This last bit
    #just shuffles the data around so it's 1-1 in stuff like TM
    #Write 4 8x8 tiles at a time
    #In the default view, there are 8 32x32 tiles on-screen
    #Each 32x32 tile is composed of 16 8x8 tiles
    #8x8 tiles take up 0x20 bytes,so to properly accomodata 32x32 tiles in TM, we need 4 apiece
    #In practice, we convert this
        #0000000000000000111111111111111122222222222222223333333333333333
        #4444444444444444555555555555555566666666666666667777777777777777
        #8888888888888888999999999999999aaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbb
        #ccccccccccccccccdddddddddddddddeeeeeeeeeeeeeeeeeffffffffffffffff
    #into this
        #0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff
        #0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff
        #0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff
        #0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff
    length = 0x80
    for i in range(0,len(tiles),0x1000):
        for ty in range(0,4,1):
            for tx in range(0,8,1):
                start = i + (ty*length)+(tx*0x200)
                end = start + length
                out2 += tiles[start:end]
    return out2

def de_convert_SCR3(table):#,x,y):
    temp = table
    out2 = []
    tiles = []
    ev_strips = []
    od_strips = []
    length = 0x80
    for i in range(0,len(temp),0x1000):
        for tx in range(0,8,1):
            for ty in range(0,4,1):
                start = i + (tx*length)+(ty*0x400)
                end = start + length
                tiles += temp[start:end]
    for i in range(0,len(tiles),0x80):
        ev_strips += tiles[i:i+0x40]
        od_strips += tiles[i+0x40:i+0x80]

    for i in range(0,len(ev_strips),0x04):
        out2 += ev_strips[i:i+0x04]
        out2 += od_strips[i:i+0x04]
    return out2

#x-y = Start/End Points of interleaved data
#8x8 tiles are stored wastefully. If you look at the data, ya see that 2 8x8 tiles
#are stored twice apiece, assumedly to fill out the given space, or perhaps because tiles
#needed to be within a 16x16 boundary?
#Whatever the case, ditch 2 tiles after every 2 tiles when interleaving. This leaves us with
#an identical output, and we can simply duplicate every 2 tiles when de-interleaving
def convert_SCR1(table,x,y):#,x,y):
    temp = []
    add = 0x80
    for i in range(x,y,add):
        grab = table[i:i+(add>>1)]
        temp += grab
    return temp

#table = scr1_file
#Strangely, to replicate what Capcom did, we copy 2 tiles twice
#A easily viewable example is the font in Knights of the Round, in the raw interleaved data,
#we see 010123234545
def de_convert_SCR1(table):#,x,y):
    temp = []
    add = 0x40
    for i in range(0,len(table),add):
        grab = table[i:i+add]
        temp += grab
        temp += grab #Write the same data twice to duplicate tiles
    return temp

#Used for CPS1/2 GFX_MAPs in order to write new files comprised of tiles of the 4 main types
#OBJ - Sprite tiles, 16x16
#SCR1 - 8x8 tiles
#SCR2 - 16x16 tiles
#SCR3 - 32x32 tiles
def CPS_write_GFX_types(res,gfx_table):
    SCR_OUT = {}
    #0-2 = SCR, 4 = OBJ
    for k in range (0, 4, 1):
        SCR_OUT.update({k : []})

    for p in range(0,len(res_file.GFX_MAP),1):
        START = res.GFX_MAP[p][1]
        END = res.GFX_MAP[p][2]
        print("GFX_MAP: = {} - {},{}".format(res.GFX_MAP[p][0],hex(START),hex(END)))
        if res.GFX_MAP[p][0] == "SCR1":
#                print("SCR1 LENGTH - ", hex(len(SCR_TABLE[k])))
            SCR_OUT[0] += convert_SCR1(gfx_table[0],START,END)
        if res.GFX_MAP[p][0] == "SCR2":
            SCR_OUT[1] += gfx_table[0][START:END]
        if res.GFX_MAP[p][0]  == "SCR3":
#                print("SCR3 LENGTH - ", hex(len(SCR_TABLE[k])))
#                SCR_OUT[2] += convert_SCR3(SCR_TABLE[2],START,END)
            SCR_OUT[2] += convert_SCR3(gfx_table[0],START,END)
#                SCR_OUT[2] += SCR_TABLE[2][START:END]
        if res_file.GFX_MAP[p][0] == "OBJ":
            SCR_OUT[3] += gfx_table[0][START:END]

    tile_types = {0 : "_SCR1",
                    1 : "_SCR2",
                    2 : "_SCR3",
                    3 : "_OBJ",
                    }
    #Write each GFX type to individiual files
    for k in range (0, 4, 1):
        if len(SCR_OUT[k]) != 0:
            print(tile_types[k], "LENGTH - ",hex(len(SCR_OUT[k])))
            name = os.path.join(out_path,inter_name+tile_types[k])
            with open(name,"wb") as out:
                out.write(bytes(SCR_OUT[k]))

#Returns a table containing the properly combined data from the individual files
def CPS_split_GFX_types(res_file):
    temp = []
    GFX_MAP = res_file.GFX_MAP
    #Grab each layer type, verifying each one exists as we go
    #Just to be safe, we'll create a temp file for each GFX type, and then we use GFX_MAP
    #to redistribute the data correctly. This way Tiles can be essentially anywhere in ROM
    #and as long as the map is correct, there shouldn't be any issues. Think of it as if we
    #get each "Bank", and split it up into the correct segments based on GFX_MAP
    data = {"OBJ" : [],
            "SCR1" : [],
            "SCR2" : [],
            "SCR3" : [],}
    for i in range(0,len(GFX_MAP),1):
        f_name = str("{}_{}".format(inter_name,GFX_MAP[i][0]))
        path = os.path.join(out_path,f_name)
        if not os.path.exists(path):
            print("{} not found! Terminating program...".format(path))
            time.sleep(2)
            exit()
        else:
            with open(path,"rb") as inp:
                if len(data[GFX_MAP[i][0]]) == 0:
                    data[GFX_MAP[i][0]] = inp.read()
                    print("{} - {}".format(GFX_MAP[i][0],
                                            hex(len(data[GFX_MAP[i][0]]))))
    #Now, redistribute the data from each file into the correct place in the combined
    #data via the GFX_MAP
    #Generate a table of counters for when we distribute data
    #Example, the GFX Map could say the first 0x0,0x100000 of data is OBJ tiles,
    #then 0x200000,0x220000. In this case, we take the data from the end of the previous
    #declaration, 0x100000, and append data from the start and end points
    #0x220000 - 0x200000 = 0x20000
    #So we grab 0x20000 bytes from 0x100000 onwards and place them into the combined data
    counter = {"OBJ" : 0,
                "SCR1" : 0,
                "SCR2" : 0,
                "SCR3" : 0,
    }
    gfx_file[0] = []
    for i in range(0,len(GFX_MAP),1):
        length = GFX_MAP[i][2] - GFX_MAP[i][1]
        start = counter[GFX_MAP[i][0]]
        end = start + length
        #OBJ and SCR2 tiles are the default, just add em
        if GFX_MAP[i][0] == "OBJ":
            temp += data["OBJ"][start:end]
        if GFX_MAP[i][0] == "SCR2":
            temp += data["SCR2"][start:end]
        #Perform operations on SCR1 and 3 tiles
        if GFX_MAP[i][0] == "SCR1":
            tmp = de_convert_SCR1(data["SCR1"][start:end])
            print("SCR1 LEN - ", hex(len(tmp)))
            temp += tmp
        if GFX_MAP[i][0] == "SCR3":
            tmp = de_convert_SCR3(data["SCR3"][start:end])
            print("SCR3 LEN - ", hex(len(tmp)))
            temp += tmp
    #Increment corresponding counter                
        counter[GFX_MAP[i][0]] += length
    return temp

def CPS1_Interleave_GFX_data():
    a = 0 #Keeps track of which Group Indexes to mess with
    increment = 0
    split_table = generate_split_table()
    assemble_sizes = generate_assemble_sizes()
    #For how many groups there are, grab Bytes from each file
    #and appropriately split them in to EVEN and ODD parts
    for group in range(0, len(res_file.group_size),1):
        print(group, " - assemble size  - ", hex(assemble_sizes[group]))
        for k in range(0, assemble_sizes[group], 1):
#        print(group, " - assemble size  - ", hex(res_file.assemble_sizes[group]))
#        for k in range(0, res_file.assemble_sizes[group], 1):
            for b in range(0, res_file.group_size[group],1):
                file_index = res_file.group_indexes[a+b]-1
                increment = res_file.rom_byte_size[file_index]
#                split = res_file.split_table[a+b]
                split = split_table[a+b]
                val = temp_counter[file_index]
                index = (group<<1)+split
#                print(index)
                tempfile[index] += gfx_file[file_index][val:val+increment]
                temp_counter[file_index] += increment

    #Add to a when done reading this group data
        a += res_file.group_size[group]        

    int_amount = 64
    #8X8 = 32
    #16X16 = 64

    #Once the Groups are properly split in to EVEN and ODD tables, Interleave
    #them one Tile at a time
    for i in range(0, len(res_file.group_size),1):
        j = 0
        while j < len(tempfile[i]):
            tempfile2[i] += tempfile[(i<<1)][j:j+int_amount]
            tempfile2[i] += tempfile[(i<<1)+1][j:j+int_amount]
            j += int_amount

    #Combine all Banks into 1 consistent file
    for i in range (0,len(tempfile2),1):
        print(len(tempfile2[i]), " - ", hex(len(tempfile2[i])))
        gfx_table[0] += tempfile2[i]

    #CONVERT SCR1/3 TILES
    #If applicable, apply needed conversions for SCR1/2 tiles
    try:
        res_file.GFX_MAP
    except:
        print("GFX_MAP: = NO")
    else:
        CPS_write_GFX_types(res_file,gfx_table)

    with open (os.path.join(out_path, inter_name), "wb") as Interleaved_GFX: 
        print("----------------TABLE3----------------")
        for i in range (0,len(tempfile3),1):
            print(len(tempfile3[i]), " - ", hex(len(tempfile3[i])))
        print("----------------TABLE2----------------")
        for i in range (0,len(tempfile2),1):
            print(len(tempfile2[i]), " - ", hex(len(tempfile2[i])))
        print("----------------TABLE1----------------")
        for i in range (0,len(tempfile),1):
            print(len(tempfile[i]), " - ", hex(len(tempfile[i])))
        print("----------------EVEN----------------")
        for i in range (0,len(even_tables),1):
            print(len(even_tables[i]), " - ", hex(len(even_tables[i])))
        print("----------------ODD----------------")
        for i in range (0,len(odd_tables),1):
            print(len(odd_tables[i]), " - ", hex(len(odd_tables[i])))
        print("----------------OUTPUT----------------")
        for i in range (0,len(gfx_table),1):
            print(len(gfx_table[i]), " - ", hex(len(gfx_table[i])))
        Interleaved_GFX.write(bytes(gfx_table[0]))

def cps1_de_interleave1():
    print("De-interleaving GFX...")
    try:
        res_file.DE_INTERLEAVE_MODE
    except:
        #Grab the Interleaved Data
        int_gfx_name = os.path.join(gfxpath, inter_name)
        int_gfx_size = os.path.getsize(int_gfx_name)
        with open(int_gfx_name, "rb") as inp: 
            gfx_file[0] = inp.read(int_gfx_size)
    else:
        gfx_file[0] = CPS_split_GFX_types(res_file)

    print(hex(len(gfx_file[0])))

    #Split the data back in to its individual ROM groups
    assemble_sizes = generate_assemble_sizes()
    offset = 0
    f_read = 0 #This is a caveman way of doing it but fuck it i'm tired lol
    for i in range(0, len(res_file.group_size),1):
        byte_read = assemble_sizes[i] << 3
        tempfile3[i] += gfx_file[0][offset:offset+byte_read]
        offset += byte_read
        f_read += 1


    #Split the ROM in to its EVEN and ODD groups again, tile by tile
    for i in range(0, len(res_file.group_size),1):
        j = 0
        while j < len(tempfile3[i]):
            tempfile2[(i<<1)]   += tempfile3[i][j:j+64]
            tempfile2[(i<<1)+1] += tempfile3[i][j+64:j+128]
            j += 128

    a = 0 #Keeps track of which Group Indexes to mess with
    increment = 0
    split_table = generate_split_table()
    #For how many groups there are, grab Bytes from each file
    #and appropriately split them in to EVEN and ODD parts
    for group in range(0, len(res_file.group_size),1):
        k = 0
        print(group, " - assemble size  - ", hex(assemble_sizes[group]))
        while k < len(tempfile2[group<<1])<<1:
            for b in range(0, res_file.group_size[group],1):
                file_index = res_file.group_indexes[a+b]-1
                increment = res_file.rom_byte_size[file_index]
                split = split_table[a+b]
                val = temp_counter[(group<<1)+split]

                tempfile[file_index] += tempfile2[(group<<1)+split][val:val+increment]
                temp_counter[(group<<1)+split] += increment
                k += 1

    #Add to a when done reading this group data
        a += res_file.group_size[group]
    print("----------------TABLE3----------------")
    for i in range (0,len(tempfile3),1):
        print(len(tempfile3[i]), " - ", hex(len(tempfile3[i])))
    print("----------------TABLE2----------------")
    for i in range (0,len(tempfile2),1):
        print(len(tempfile2[i]), " - ", hex(len(tempfile2[i])))
    print("----------------TABLE1----------------")
    for i in range (0,len(tempfile),1):
        print(len(tempfile[i]), " - ", hex(len(tempfile[i])))
    print("----------------EVEN----------------")
    for i in range (0,len(even_tables),1):
        print(len(even_tables[i]), " - ", hex(len(even_tables[i])))
    print("----------------ODD----------------")
    for i in range (0,len(odd_tables),1):
        print(len(odd_tables[i]), " - ", hex(len(odd_tables[i])))

    #Write the files back
    for i in range(0, num_of_gfx_roms, 1):
        FILE_LOC = os.path.join(gamepath, filename[i])
        with open(FILE_LOC,"wb") as out:
            out.write(bytes(tempfile[i]))
#    time.sleep(1)

#//////////////////// START OF CASE CPS2 ////////////////////
def CASE_CPS1():

#///// INTERLEAVE DATA ///////////////
    if script_action == "1":
   #Grab data for the interleaved GFX file
        grab_CPS1_ROM_Data()
    #Next, assemble EVEN and ODD tables based on ROM layout
        CPS1_Interleave_GFX_data()

#///// DE-INTERLEAVE DATA ////////////
    if script_action == "2":
    #Grab data from the interleaved GFX file
        cps1_de_interleave1()


#        print("----------------TABLE3----------------")
#        for i in range (0,len(tempfile3),1):
#            print(len(tempfile3[i]))
#        print("----------------TABLE2----------------")
#        for i in range (0,len(tempfile2),1):
#            print(len(tempfile2[i]))
#        print("----------------TABLE1----------------")
#        for i in range (0,len(tempfile),1):
#            print(len(tempfile[i]))
#        print("----------------OUTPUT----------------")
#        for i in range (0,len(gfx_table),1):
#            print(len(gfx_table[i]))
#        write_m_files()

#//////////////////// END OF CASE CPS1 ////////////////////


#//////////////////// DECIDE WHAT TO DO WITH DATA ////////////////////

if gfx_ok == 1:
    if res_file.System == "Neo-Geo":
        CASE_NEO_GEO()

    if res_file.System == "CPS1" or res_file.System == "CPS2" :
    #Only Interleave GFX if there is GFX to interleave
        #Generate required tables to store data
            tempfile = {}
            even_tables = {}
            odd_tables = {}
            for i in range (0, num_of_gfx_roms, 1):
                tempfile.update({i : []})
                even_tables.update({i : []})
                odd_tables.update({i : []})
            tempfile2 = {}
            for i in range (0, num_of_gfx_roms >> 1, 1):
                tempfile2.update({i : []})
            tempfile3 = {}
            for i in range (0, num_of_gfx_roms>>2, 1):
                tempfile3.update({i : []})
            if res_file.System == "CPS2":
                CASE_CPS2()
            if res_file.System == "CPS1":
                temp_counter = {}
                for i in range (0, num_of_gfx_roms, 1):
                        temp_counter.update({i : 0})
                CASE_CPS1()

if prg_ok == 1:
    if script_action == "1":
        Interleave_PRG()
    if script_action == "2":
       De_Interleave_PRG()
