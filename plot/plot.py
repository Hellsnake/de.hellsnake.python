import pyperclip
import matplotlib as malp
import matplotlib.pyplot as plt

def main():
	val = parse_clipboard()
	max_x = max(val[0])
	min_x = min(val[0])

	plt.ylabel('Level (dbuV/m)')
	plt.xlabel('frequency (Hz)')
	plt.xscale('log')
	plt.xlim(min_x, max_x)
	plt.xticks([min_x, 200, 500, 700, max_x], [min_x, 200, 500, 700, max_x])
	plt.plot(val[0], val[1], marker='', linestyle='-', label='Average')
	plt.grid(True)
	plt.show()



def parse_clipboard():
	val = pyperclip.paste()
	x_val = list()
	y_val = list()

	''' Seperate Rows '''
	rows = val.split('\n')

	for row in range(0,len(rows) - 1):
		# seperate columns and replace not necessary characters
		column = rows[row].replace('\r', '').split('\t')
		x_val.append(float(column[0].replace(',', '.')))
		y_val.append(float(column[1].replace(',', '.')))

	return [x_val, y_val]
		
def create_seperators(min, max):
	vals = list()

	vals.append(min)


if __name__ == '__main__':
	main()