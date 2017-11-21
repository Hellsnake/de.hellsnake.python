
from BaseConfig import BaseConfig
import json


def main():
	conf = BaseConfig("Test", 1)
	print(json.dumps(conf, default = jdefault))

def jdefault(o):
	return o.__dict__


if __name__ == '__main__':
	main()