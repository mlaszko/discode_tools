#! python
#-*- coding: utf-8 -*-

import subprocess
from xml.dom import minidom

#uruchamia zadanie discode podane w parametrze task w formacie DCL:task
#zabija wszystkie discode po zakończeniu sekwencji
#wyjście zapisuje do pliku filename
def run_sequence(task, filename, info = '', log_level = 0):
    command = 'discode -T' + task + ' -L' + str(log_level)
    file = open(filename, 'w')
    if info != '':
        file.write(info)
        file.write('\n------------------------------------------------------\n')
    proc = subprocess.Popen(command, 
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )

    while True:
        output = proc.stdout.readline() 
        print output.rstrip()
        file.write(output)
        if output.find('Select failed!: Invalid argument')>=0:
            file.close()
            subprocess.call(["killall", "discode"])
            run_sequence(task, filename, info)
            return
        if output.find(' End of sequence')>=0:
            print "Koniec!!!"
            file.close()
            subprocess.call(["killall", "discode"])
            return
    file.close()
    
#edytuje parametry w tasku filename
#params to slownik z nazwami i wartosciami parametrow
def edit_task(filename, params):
    DOMTree = minidom.parse(filename)
    cNodes = DOMTree.childNodes
    subtasks = cNodes[0].getElementsByTagName("Subtasks")
    subtask = subtasks[0].getElementsByTagName("Subtask")
    executors = subtask[0].getElementsByTagName("Executor")
    for e in executors:
        components = e.getElementsByTagName("Component")  #komponenty w executorze
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

    
