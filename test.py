#!/usr/bin/python3
from dc_source import *
import time



def main():
    source = DC_SOURCE('DPH5015_3')
    source.set(7.58, 2)
    source.toggle('ON')
    
    time.sleep(1)

    print("Power: " + str(source.getPower()))
    print("Info:")

    info = source.getInfo()

    print("\tU-set x100: ", info[0])
    print("\tI-set x100: ", info[1])
    print("\tU-out x100: ", info[2])
    print("\tI-out x100: ", info[3])
    print("\tP-out x100: ", info[4])
    print("\tU-in x100: ", info[5])
    print("\tlock/unlock 1/0 (R/W): ", info[6])
    print("\tProtected 1/0: ", info[7])
    print("\tOperating mode CC/CV 1/0: ", info[8])
    print("\ton/off 1/0 (R/W): ", info[9])
    print("\tDisplay intensity 1..5 (R/W): ", info[10])
    print('ENTER!')
    input()
    
    
if __name__ == "__main__":
    main()
