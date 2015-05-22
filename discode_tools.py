#! python
#-*- coding: utf-8 -*-

import subprocess
from xml.dom import minidom

#uruchamia komendę command
#wyjście zapisuje do pliku filename
def run(command, filename):
    file = open(filename, 'w')
    proc = subprocess.Popen(command, 
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )

    while True:
        output = proc.stdout.readline() 
        if output.find('SequenceRGB: end of sequence')>=0:
            print "Koniec!!!"
            proc.kill()
            break
        print output.rstrip()
        file.write(output)
#    remainder = proc.communicate()[0]
#    print remainder   
    file.close()
    
#edytuje parametry w tasku filename tylko w pierwszym executorze
#params to slownik z nazwami i wartosciami parametrow
def edit_task(filename, params):
    DOMTree = minidom.parse(filename)
    cNodes = DOMTree.childNodes
    subtasks = cNodes[0].getElementsByTagName("Subtasks")
    subtask = subtasks[0].getElementsByTagName("Subtask")
    executor = subtask[0].getElementsByTagName("Executor")
    components = executor[0].getElementsByTagName("Component")  #komponenty w pierwszym executorze
    for i in components:
        #print i.getAttribute("name") #component name
        for j in i.getElementsByTagName("param"):
            #print j.getAttribute("name") + ' = ' + j.childNodes[0].toxml()
            if j.getAttribute("name") in params:
                j.childNodes[0].nodeValue = params[j.getAttribute("name")]
        #print ' '
    #print DOMTree.toxml()
    
    file = open(filename, 'w')
    file.write(DOMTree.toxml())
    file.close()

    
