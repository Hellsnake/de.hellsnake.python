import pyperclip
import matplotlib as malp
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import math

def main():
	plots = parse_values(pyperclip.paste())
	ticks = create_ticks(plots[0].get_xvalues())
	formatter0 = EngFormatter(places=1, sep=u"\N{THIN SPACE}")
	fig, (ax0) = plt.subplots(nrows=1, figsize=(9.6, 7))
	
	
	
	ax0.set_xscale('log')
	ax0.xaxis.set_major_formatter(formatter0)
	
	ax0.set_ylabel('Level [dbuV/m]')
	ax0.set_xlabel('Frequency [MHz] ')
	ax0.grid(True)
	#ax0.set_xlim(min(ticks), max(ticks))
	ax0.set_xticks(ticks)
	#plt.xlim(min(ticks), max(ticks))
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

	''' Seperate Rows '''
	rows = val.split('\n')

	for row in range(0,len(rows) - 1):
		# seperate columns and replace not necessary characters
		column = rows[row].replace('\r', '').split('\t')
		if(len(column) > 3 or len(column) < 2):
			return ret
		elif(len(column) == 3 and name != column[0]):
			name = str(column[0])
			p = PlotLine(name)
			plots.append(p)
		p.add_xvalues(float(column[1].replace(',', '.')))
		p.add_yvalues(float(column[2].replace(',', '.')))

	return plots
		
def create_ticks(vals):
	max_val = int(max(vals))
	min_val = int(min(vals))
	i = min_val
	ticks = list()
	print('max: {0:d}, min: {1:d}'.format(max_val, min_val))
	ticks.append(min_val)
	ticks.append(max_val)
	while i < max_val:
		mult = int(str(math.log(i) / math.log(10))[0:1])
		i = i + (mult * 20)
		
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