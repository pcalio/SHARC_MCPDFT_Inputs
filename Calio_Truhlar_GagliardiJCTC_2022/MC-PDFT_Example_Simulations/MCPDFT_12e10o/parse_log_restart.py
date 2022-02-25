import shutil
import sys
from os import path

#if path.exists("output.log"):
shutil.move("output.log", "output.log.full")

f=open("output.log.full", "r")
ifile = f.readlines()
f.close()

fp=open("output.log", "w")

CheckBeg=[]
CheckEnd=[]

Time=[]
BegOfFile=[]
EndOfFile=[] #[] = list (aka array), while {} = dictionary
end = False
first=False
beg = False

BegOfFile.append(0)

#First, check if the file has sections that were completed correctly.
for i in range( len(ifile) ):
    line = ifile[i].split()
    if len(line) != 0:
        if line[0] == 'EXECUTION' and line[1] ==  'INFORMATION:':
            CheckBeg.append(i)
        if line[0] == 'Total' and line[1] ==  'wallclock' and line[2] == 'time:':
            CheckEnd.append(i)

#If each segment completed correctly ...
if len( CheckBeg ) == len (CheckEnd ):
    #print ( 'Equal', CheckBeg, CheckEnd )
    for i in range( len(ifile) ):
        line = ifile[i].split()
        if len(line) != 0:
            if line[0] == 'Total' and line[1] ==  'wallclock' and line[2] == 'time:':
                Time.append(i)
                end = True
            if end:
                if line[0] == '------------------------------------------------------------------------------------------':
                    if first==False:
                        first=True
                        continue
                    if first==True:
                        EndOfFile.append(i)
                        end = False
                        first = False
                        beg = True
            if len(EndOfFile) > 0 and beg:
                if line[0] == '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<':
                    if line[1] == 'Entering' and line[2] == 'timestep':
                        BegOfFile.append(i-1)
                        beg=False

#print(EndOfFile)
    for i in range( len(EndOfFile) ):
        for j in range(BegOfFile[i],Time[i]): #I don't want to print the "total wallclock time" line
            fp.writelines(ifile[j])

    for i in range( Time[ len(EndOfFile)-1 ], len(ifile)):
        fp.writelines(ifile[i])

#If segments didn't complet correctly ...
else:
    prevstep = 0
    nextstep = 0
    #print ( CheckBeg, CheckEnd )
    for i in range( len(ifile) ):
        iline = ifile[i].split()
        if len(iline) != 0:
            if iline[0] == 'EXECUTION' and iline[1] ==  'INFORMATION:':
                if i == CheckBeg[0]:
                    continue
                else:
                    for j in range(i, -1, -1):
                        jline = ifile[j].split()
                        if len(jline) != 0:
                            if jline[0] == '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<':
                                if jline[1] == 'Entering' and jline[2] == 'timestep':
                                    prevstep = jline[3]
                                    tmpEndOfFile = j-1
                                    break
                    for j in range(i, len(ifile)):
                        jline = ifile[j].split()
                        if len(jline) != 0:
                            if jline[0] == '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<':
                                if jline[1] == 'Entering' and jline[2] == 'timestep':
                                    nextstep = jline[3]
                                    tmpBegOfFile = j-1
                                    break
                    if prevstep == nextstep:
                        #print(i, tmpEndOfFile, tmpBegOfFile)
                        EndOfFile.append(tmpEndOfFile)
                        BegOfFile.append(tmpBegOfFile)
                    else:
                        print('Problem in parsing the log file. Timesteps do not overlap')
                        sys.exit(1)
    EndOfFile.append( len(ifile) )

    if len(BegOfFile) == len(EndOfFile):
        for i in range( len(EndOfFile) ):
            for j in range(BegOfFile[i], EndOfFile[i]) :
                fp.writelines(ifile[j])

fp.close()

