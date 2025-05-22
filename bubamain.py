#!/usr/bin/env python3
import sys,time,os, basics
def main():
    try:
        while True:
            try:
                curdir = [".."] + os.listdir()
                index, selected = basics.menu(curdir)
                selected_path = os.path.abspath(selected) #Ensuring its an absolute path
                #print(selected_path)
                if basics.is_buba_exec(selected_path):
                    basics.run_buba_exec(selected_path)
                elif os.path.isdir(selected_path):
                    os.chdir(selected_path)
                else:
                    print("Bad dir")
            except Exception as e:
                try:
                    print("ERROR: "+ str(type(e)))
                except Exception:
                    print("ERROR! Also, there was an error displaying the error type, GLHF (: ")
                basics.error_warn()
    except KeyboardInterrupt:
        sys.exit("Goodbye")

main()