#!/usr/bin/env python3
import sys,time,os, bubasics
def main():
    try:
        while True:
            try:
                curdir = [".."] + os.listdir()
                index, selected = bubasics.menu(curdir)
                selected_path = os.path.abspath(selected) #Ensuring its an absolute path
                #print(selected_path)
                if bubasics.is_buba_exec(selected_path):
                    bubasics.run_buba_exec(selected_path)
                elif os.path.isdir(selected_path):
                    os.chdir(selected_path)
                else:
                    print("Bad dir")
            except Exception as e:
                try:
                    print("ERROR: "+ str(type(e)))
                except Exception:
                    print("ERROR! Also, there was an error displaying the error type, GLHF (: ")
                bubasics.error_warn()
    except KeyboardInterrupt:
        sys.exit("Goodbye")
    finally:
        bubasics.button_cleanup()

main()