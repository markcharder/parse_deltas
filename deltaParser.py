#!/usr/bin/env python

import optparse
import re

# Create instance of OptionParser from optparse.

parser = optparse.OptionParser()

# Populate instance with options from command line.

parser.add_option(	"-d", 
			"--delta", 
			dest	= "input", 
			help	= "Input delta file.", 
			metavar	= "DELTA"	)
parser.add_option(	"-o", 
			"--output", 
			dest	= "out_file", 
			help	= "Output svg file. Defaults to 'out.svg'", 
			metavar	= "OUTPUT"	)

(options, args) = parser.parse_args()

if not options.input:
	parser.error("Please specify input delta file.")
if not options.out_file:
	options.out_file = 'out.svg'

# Open delta file and read into list.

delta_file	= open(options.input, "r")
contents	= delta_file.readlines()

# Define function to append to dictionary. Maybe add to external mod.

def dict_append(a,b):
	x = a.copy()
	b.update(x)
	return b

# Read lines of delta file.

refs		= dict()
rlens		= dict()
qlens		= dict()
ref		= ''
query		= ''
rlen		= ''
qlen		= ''
queries		= dict()
query_list	= []

for line in contents:
	line_list = line.split()
	if re.match(">", line):
		ref 		= line_list[0]
		query 		= line_list[1]
		rlen 		= line_list[2]
		qlen 		= line_list[3]
		queries		= {query:''}
		rlens[ref]	= rlen
		qlens[query]	= qlen
		if ref not in refs:
			refs[ref] = queries
		else:
			refs[ref] = dict_append(refs[ref], queries)
		query_list.append(query)
	else:

		if len(line_list) > 1 and not re.match('/', line):
			rstart		= line_list[0]
			rend		= line_list[1]
			qstart		= line_list[2]
			qend		= line_list[3]
			indels		= line_list[4]
			diffs		= line_list[5]
			stops		= line_list[6]
			attributes	= {	'rstarts':[rstart],
						'rends':[rend],
						'qstarts':[qstart],
						'qends':[qend],
						'indels':[indels],
						'diffs':[diffs],
						'stops':[stops]	}
			if refs[ref][query] == '':
				refs[ref][query] =  attributes
			else:
				refs[ref][query]['rstarts'].append(rstart)
				refs[ref][query]['rends'].append(rend)
				refs[ref][query]['qstarts'].append(qstart)
				refs[ref][query]['qends'].append(qend)
				refs[ref][query]['indels'].append(indels)
				refs[ref][query]['diffs'].append(diffs)
				refs[ref][query]['stops'].append(stops)


query_list	= list(set(query_list))
sizes		= []
size_dict	= dict()
refsize_dict 	= dict()

for item in query_list:
	for okey in refs.iterkeys():
		for ikey, value in refs[okey].iteritems():
			if ikey == item:
				start_list	= refs[okey][ikey]['rstarts']
				end_list	= refs[okey][ikey]['rends']
				for i in range(0,len(refs[okey][ikey]['rstarts'])):
					if int(start_list[i]) > int(end_list[i]):
						size = int(start_list[i]) - int(end_list[i])
					elif int(end_list[i]) > int(start_list[i]):
						size = int(end_list[i]) - int(start_list[i])
					sizes.append(size)
				sizes.sort(reverse=True)
				refsize_dict = dict_append(refsize_dict, {okey: sizes[0]})
				sizes = []
	new_dict 	= {item: refsize_dict}
	size_dict 	= dict_append(size_dict, new_dict)
	refsize_dict	= dict()

# Define function to return dictionary items with largest first array value. Maybe add to external mod.

def get_best_aligns(dictionary):
	for key, value in dictionary:
		if value > previous:
			new = key
		previous = value
	return new
		

for okey, value in refsize_dict.iteritems():
	get_best_aligns
			

#for key, value in refs[ref]

# Open SVG file and print dot plot to it.

#yaxlen = 0
#for key, value in rlens.iteritems():
#	yaxlen += int(value)

#xaxlen = 0
#for key, value in qlens.iteritems():
#	xaxlen += int(value)

#xaxlen = 400.0 / float(xaxlen) * float(xaxlen) + 20.0
#yaxlen = 400.0 / float(yaxlen) * float(yaxlen) + 20.0

#svg_begin		= "<svg height='500' width='500'>"
#rect			= "<rect height='500' width='500' fill='white'/>"
#svg_set_start		= "<g fill='white' stroke='black' stroke-width='1.5'>"
#xaxis_properties 	= "<line x1='" + str(yaxlen) + "' x2='20' y1='" + str(yaxlen) + "' y2='" + str(yaxlen) + "'/>"
#yaxis_properties 	= "<line x1='20' x2='20' y1='20' y2='" + str(yaxlen) + "'/>"
#svg_set_end		= "</g>"
#svg_end			= "</svg>"


#svg_file	= open(options.out_file, 'w')
#svg_file.write(svg_begin + "\n\t" + rect + "\n\t" + svg_set_start + "\n\t\t" + xaxis_properties + "\n\t\t" + yaxis_properties + "\n\t" + svg_set_end + "\n" + svg_end)
