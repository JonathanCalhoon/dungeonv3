import json, os


def class_to_json(object):
	"""Converts a 'nested' class to 'nested' JSON"""

	result = json.loads(json.dumps(object, default=lambda o: o.__dict__))

	return result


def map_to_string(_map):
	"""Converts a Nested List map to String"""
	string = ""

	for i in _map:
		row = ""
		for j in i:
			row += j
		row += '\n'
		string += row

	return string


def map_from_file(file):
	"""Converts a string to a nested list"""
	with open(file, 'r') as file:
		data = file.read()

	_map = []

	rows = data.split("\n")

	for row in rows:
		r = [char for char in row]
		_map.append(r)

	return _map

