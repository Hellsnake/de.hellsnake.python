import pyperclip
import matplotlib as malp
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import math

def main():
	plots = parse_values(pyperclip.paste())
	ticks = create_ticks(plots[0].get_xvalues())
	#formatter0 = EngFormatter(unit='Hz')
	fig, (ax0) = plt.subplots(nrows=1, figsize=(9.6, 7))
	
	ax0.set_xscale('log')
	#ax0.xaxis.set_major_formatter(formatter0)
	
	ax0.set_ylabel('Level [dbuV/m]')
	ax0.set_xlabel('Frequency')
	ax0.grid(True)
	#ax0.set_xlim(min(ticks), max(ticks))
	ax0.set_xticks(ticks)
	plt.xlim(min(plots[0].get_xvalues()), max(plots[0].get_xvalues()))
	#plt.xticks(ticks , ticks)

	for plot in plots:
		ax0.plot(plot.get_xvalues(), plot.get_yvalues(), label=plot.get_name())

	ax0.legend()
	plt.tight_layout()
	plt.show()



def parse_values(val):
	x_val = list()
	y_val = list()
	plots = list()
	name = str()
	row_index_x = int()
	row_index_y = int()
	row_index_name = int()

	''' Seperate Rows '''
	rows = val.split('\n')

	for row in range(0,len(rows) - 1):
		# seperate columns and replace not necessary characters
		column = rows[row].replace('\r', '').split('\t')

		if(len(column) > 3):
			row_index_x = 2
			row_index_y = 3
			row_index_name = 0
		elif(len(column) == 3):
			row_index_x = 1
			row_index_y = 2
			row_index_name = 0
		if(name != column[row_index_name]):
			print(name)
			name = str(column[row_index_name])
			p = PlotLine(name)
			plots.append(p)
		x = column[row_index_x]
		y = column[row_index_y]

		if(bool(x.strip())):
			print('x: {0:s}, y: {1:s}'.format(x, y))
			p.add_xvalues(float(x.replace(',', '.')))
			p.add_yvalues(float(y.replace(',', '.')))

	print(plots[0].get_xvalues())
	return plots
		
def create_ticks(vals):
	max_val = max(vals)
	min_val = min(vals)
	i = min_val
	ticks = list()
	print('max: {0:4.2f}, min: {1:4.2f}'.format(max_val, min_val))
	ticks.append(min_val)
	ticks.append(max_val)
	step = (max_val - min_val) / (10 / math.log(max_val - min_val))
	while(i < max_val):
		i = i + step
		if(i > 0):
			i = round(i,0)
		if(i > max_val):
			break
		ticks.append(i)
	return ticks

class PlotLine(object):

	countOfPlotLine = 0

	def __init__(self, name=''):
		self._xvalues = list()
		self._yvalues = list()
		self._name = str(name)
		PlotLine.countOfPlotLine = PlotLine.countOfPlotLine + 1

	def add_xvalues(self,val):
		self._xvalues.append(val)

	def add_yvalues(self,val):
		self._yvalues.append(val)

	def get_xvalues(self):
		return self._xvalues

	def get_yvalues(self):
		return self._yvalues

	def get_name(self):
		return self._name

if __name__ == '__main__':
	main()