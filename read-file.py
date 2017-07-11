import time
import os

def main(): 
        loop_usbtest()

def loop_usbtest():
        path = 'G:/temp.txt'

        while (1):
                start = time.time()
                end = time.time()
                f = open(path, 'w')
                while ((end - start) < 10):
                        f.write('Start: ' + str(start) + 'End: ' + str(end) + '\n')
                        end = time.time()
                f.close()
                os.remove(path)
        

if __name__ == '__main__':
    main()
