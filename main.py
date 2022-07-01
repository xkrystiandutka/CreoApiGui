import creopyson
import win32api
import subprocess


c = creopyson.Client()
c.connect()
c.creo_set_creo_version(7)

# CONSTANTS

path = 'D:\API\PROJEKT2'
file = "model2copy.prt"

def authorApi():
    print ("""
                                    _                                               
                        /\         (_)                                              
   ___ _ __ ___  ___   /  \   _ __  _                                               
  / __| '__/ _ \/ _ \ / /\ \ | '_ \| |                                              
 | (__| | |  __/ (_) / ____ \| |_) | |                                              
  \___|_|  \___|\___/_/    \_\ .__/|_|  _               _____        _   _          
 | |           | |/ /        | |   | | (_)             |  __ \      | | | |         
 | |__  _   _  | ' / _ __ _  |_|___| |_ _  __ _ _ __   | |  | |_   _| |_| | ____ _  
 | '_ \| | | | |  < | '__| | | / __| __| |/ _` | '_ \  | |  | | | | | __| |/ / _` | 
 | |_) | |_| | | . \| |  | |_| \__ \ |_| | (_| | | | | | |__| | |_| | |_|   < (_| | 
 |_.__/ \__, | |_|\_\_|   \__, |___/\__|_|\__,_|_| |_| |_____/ \__,_|\__|_|\_\__,_| 
         __/ |             __/ |                                                    
        |___/             |___/                                                     
"""
)

authorApi()

def setCreoWorkingPath():
    userInput = input("Do you want to modify working directory (y/n)? ")
    if userInput.lower() == 'n':
        worikngPath = 'D:\API\PROJEKT2'
        print("he path of the working directory remains the same!")
    elif userInput.lower() == 'y':
        newWorkingPath = input('Set new working path for creo:')
        c.creo_cd(newWorkingPath)        
    else:
        print('Error: Wrong input, Use y or n! Try again')
        setCreoWorkingPath()




setCreoWorkingPath()


c.file_open("model2copy.prt", display=True)



listaParametrow  = [[100, 100, 8, 100, 36, 10],
                    [100, 140, 8, 100, 36, 10],
                    [100, 180, 8, 100, 36, 10],
                    [140, 100, 10, 100, 38, 12],
                    [140, 140, 10, 100, 38, 12],
                    [140, 180, 10, 100, 38, 12],
                    [180, 100, 11, 100, 40, 14],
                    [180, 140, 11, 100, 40, 14],
                    [180, 180, 11, 100, 40, 14]]

while True:
    i = int(input("Choose a variant(1 - 9): "))
    if (i > 10 or type(i) != int or i < 0):
        print("\ERROR: incorrect value!\n")
        continue
    break


A = listaParametrow[i-1][0]
B = listaParametrow[i-1][1]
C = listaParametrow[i-1][2]
D = listaParametrow[i-1][3]
E = listaParametrow[i-1][4]
F = listaParametrow[i-1][5]

PatternA = 0

if (A == 180):
    PatternA = 4
elif (A == 140):
     PatternA = 3
elif (A == 100):
    PatternA = 2

PatternB = 0

if (B == 180):
    PatternB = 4
elif (B == 140):
     PatternB = 3
elif (B == 100):
    PatternB = 2   

c.feature_suppress(name="GROUP_A")
c.feature_suppress(name="GROUP_B")

c.parameter_set('A', A)
c.parameter_set('B', B)
c.parameter_set('C', C)
c.parameter_set('D', D)
c.parameter_set('E', E)
c.parameter_set('F', F)
c.parameter_set('p37', PatternA)
c.parameter_set('p26', PatternB)

if (PatternA > 2):
    c.feature_resume(name="GROUP_A")

if (PatternB > 2):
    c.feature_resume(name="GROUP_B")

c.file_regenerate()

materials = c.file_list_materials()
counter = 0
for x in materials:
    print(str(counter) + " - " + x)
    counter = counter+1

material = int(input("Select material(number):"))

c.file_set_cur_material(str(materials[material]))
c.file_regenerate()

filePath = path + "/data.txt"
text_file = open(filePath, "w")

text_file.write('Name:W')
text_file.write(str(i))
text_file.write('\nA=' + str(A))
text_file.write('\nB=' + str(B))
text_file.write('\nC=' + str(C))
text_file.write('\nD=' + str(D))
text_file.write('\nE=' + str(E))
text_file.write('\nF=' + str(F))
text_file.write('\nF=' + str(F))
text_file.write('\nMaterial name: ' + str(materials[material]))
massprops = c.file_massprops()["mass"]
masspropsFormat = "{:.2f}".format(massprops)
text_file.write('\nWeight of the material ' + str(masspropsFormat))
text_file.close()
print("\nData export to file!")

#export do pliku step
c.interface_export_file("STEP")
print("\nExport  STEP!")

#export do pdf
c.interface_export_3dpdf()
print("\nExport 3dpdf!")

input("\nTime for you to check the results.")

c.file_save()
c.file_close_window()

c.file_open("zlozenie.asm")
c.file_assemble("model2copy.prt")

c.disconnect()


