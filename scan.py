import visa
import time

def main():
	rm = visa.ResourceManager()
	rm.list_resources()
	frequencies = [5684, 5742, 5800, 5858, 5916]
	pause = 5	
	time.sleep(1)
	
	for i in frequencies:
		signalgenerator = rm.open_resource('GPIB::6::INSTR')
		print("SET Frequency to %d MHz" % i)
		signalgenerator.write(":SOUR:FREQ:CW %d MHz" % i)
		signalgenerator.close()
		amp = rm.open_resource('GPIB::8::INSTR')
		print("SET AMPLIFIER %d s ON" % pause)
		amp.write("AMP_ON")
		
		time.sleep(pause)
		print("SET AMPLIFIER %d s OFF" % pause)
		amp.write("AMP_OFF")
		amp.close()
		time.sleep(pause)
		

if __name__ == '__main__':
    main()