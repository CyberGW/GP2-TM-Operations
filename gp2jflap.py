import os
import re

__author__ = "George Williams"
__version__ = "alpha"
__email__ = "gew518@york.ac.uk"

#input file
gp2 = open("graph.output", "r")

#separate nodes and edges and remove [ and ] at start and end
text = gp2.read().split("|")
text[0] = text[0].replace("[","")
text[0] = text[0].replace("(R)","")
text[1] = text[1].replace("]","")
#split elements and form into a list of lists
#nodes = [ [id, label] ... ]
#edges = [ [id, source, target, label] ... ]
for i in range(0,2):
    text[i] = text[i].replace(")","\n")
    text[i] = text[i].replace("(","")
    text[i] = text[i].replace("\"","")
    text[i] = text[i].replace(" ","")
    text[i] = os.linesep.join([s for s in text[i].splitlines() if s])
    text[i] = text[i].splitlines()
    for j in range(0, len(text[i])):
        text[i][j] = text[i][j].split(",")
        #text[i][j] = text[i][j].split("#")

#split into separate variables
nodes = text[0]
edges = text[1]

#==================================================
# CREATE OUTPUT
#==================================================
text = ""
#write header
text += """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!--Created for JFLAP 6.4. with gp2jflap.py--><structure>
\t<type>turing</type>
\t<tapes>1</tapes>
\t<automaton>"""

#comment the start of states
text += "\n\t\t<!--The list of states.-->"
#write in nodes
final = 0
for i in range(0, len(nodes)):
    n = nodes[i]
    if "#green" in n[1]: #if final state
        n[1] = n[1].replace("#green","") #remove marker
        final = 1 #remember it's a final state
    text += "\n\t\t<state id=\"" + n[0] + "\" name=\"" + n[1] + """\">
    \t\t<x>""" + str(i*200) + """</x>
    \t\t<y>0</y>""" #separate each state on the x-axis
    if final: #if final state
        text += "\n\t\t\t<final/>" #add final tag
        final = 0
    text += "\n\t\t</state>"

#comment the start of transitions
text += "\n\t\t<!--The list of transitions.-->"
#write in edges
for e in edges:
    if "#dashed" in e[3]: #if the edge representing initial state
        initial = e[1] #save initial state id, but don't save edge
    else:
        e[3] = e[3].split(":") #split the list into section
        tapes = len(e[3]) // 3 #get the total number of tapes
        text += """\n\t\t<transition> 
        \t<from>""" + e[1] + """</from>
        \t<to>""" + e[2] + "</to>"        
        for i in range(0, len(e[3]), 3): #for each tape
            curr_tape = str( (i//3)+1 )
            text += "\n\t\t\t<read tape=\"" + curr_tape + "\""
            if e[3][i] == "_":
                text += "/>"
            else:
                text += ">" + e[3][i] + "</read>"
            text += "<write tape=\"" + curr_tape + "\""
            if e[3][i+1] == "_":
                text += "/>"
            else:
                text += ">" + e[3][i+1] + "</write>"
            text += "<move tape = \"" + curr_tape + "\">" + e[3][i+2] + "</move>"
        text += "\n\t\t</transition>"
text += "\n</automaton> \n </structure>"

#find inital state declaration
match = re.search("<state id=\"" + initial + ".*>", text).group()
#add on the initial tag
text = text.replace(match, match + "<initial/>")

#find initial state transition
match = re.search("<from>" + initial + ".*\n.*\t.*\n.*\t.*<read tape=\"1\"/>", text, re.M).group()
#change text read on tape 1 to _ (as blanks can't be entered in JFLAP)
text = text.replace(match, match[:-2] + ">_</read>")

#update tape number
text = text.replace("<tapes>1", "<tapes>" + str(tapes))

#==================================================
# WRITE TO OUTPUT FILE
#==================================================
jflap = open("output.jff", "w")
jflap.write(text) #write over file with changes
jflap.close() #close
