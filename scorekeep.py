#import wordfun

#----------------------------------------------------------------------------#
#Class:  SCOREKEEP
#---------------------- -----------------------------------------------------#
#SCORE properties/data
gstrDELIM_SCORE=":"
gstrFILENAME_SCORE="userscore.txt"
#
#----------------------------------------------------------------------------#
#Function:  SCOREKEEP_ParseRecord()
#----------------------------------------------------------------------------#
def SCOREKEEP_ParseRecord(dictSCORE,strIn):
    nError = 0x0000
    IsFound = False
    nFound=-1
    strUsername=""
    strScore=""
    nCount = len(strIn)
    nLoop=0
    while((IsFound==False)and(nLoop<nCount)):
        charIn=strIn[nLoop]
        if(charIn==gstrDELIM_SCORE):
            nFound=nLoop
            IsFound=True
        nLoop=nLoop+1
    strUsername=strIn[0:(nFound)]
    nFound=nFound+1
    strScore=strIn[nFound:nCount]
    dictSCORE["strUsername"]=strUsername
    dictSCORE["strScore"]=strScore
    return nError
#
#----------------------------------------------------------------------------#
#Function:  SCOREKEEP_AddScore()
#----------------------------------------------------------------------------#
def SCOREKEEP_AddScore(dictSCORE,strUsername,nAdd):
    linesIn=dictSCORE["linesIn"]
    nOutScore=0
    nFoundLine=-1
    IsFound = False
    nLine = 0
    nCount=len(linesIn)
    while((IsFound==False) and (nLine<nCount)):
        strLine=linesIn[nLine]
        dictSCORE["strUsername"]=""
        dictSCORE["strScore"]=""
        SCOREKEEP_ParseRecord(dictSCORE,strLine)
        strName=dictSCORE["strUsername"]
        strScore=dictSCORE["strScore"]
        if(strUsername.upper() == strName.upper()):
            nOutScore = int(strScore)
            IsFound=True
            nFoundLine=nLine
        nLine=nLine+1
    if(IsFound==False):
        strAdd=strUsername+gstrDELIM_SCORE+str(nAdd)
        linesIn.insert(0,strAdd)
        nOutScore=nAdd
    else:
        nTemp = nOutScore+nAdd
        strAdd=strUsername+gstrDELIM_SCORE+str(nTemp)
        linesIn[nFoundLine]=strAdd
        nOutScore=nTemp
    print(f"SCOREKEEP_GetScore:  Add:{strAdd} Found:{nFoundLine}")
    return nOutScore
#
#----------------------------------------------------------------------------#
#Function:  SCOREKEEP_GetScore()
#----------------------------------------------------------------------------#
def SCOREKEEP_GetScore(dictSCORE,strUsername):
    linesIn=dictSCORE["linesIn"]
    nOutScore=0
    nFoundLine=-1
    IsFound = False
    nLine = 0
    nCount=len(linesIn)
    while((IsFound==False) and (nLine<nCount)):
        strLine=linesIn[nLine]
        dictSCORE["strUsername"]=""
        dictSCORE["strScore"]=""
        SCOREKEEP_ParseRecord(dictSCORE,strLine)
        strName=dictSCORE["strUsername"]
        strScore=dictSCORE["strScore"]
        if(strUsername.upper() == strName.upper()):
            nOutScore = int(strScore)
            IsFound=True
            nFoundLine=nLine
        nLine=nLine+1
    if(IsFound==False):
        strAdd=strUsername+gstrDELIM_SCORE+"0"
        linesIn.insert(0,strAdd)
        strTemp=linesIn[0]
        print(f"SCOREKEEP_GetScore:  Add:{strAdd} Lines:{strTemp}")
#    else:
#        strAdd=strUsername+gstrDELIM_SCORE+str(nOutScore)
#        linesIn[nFoundLine]=strAdd
    return nOutScore
#
#----------------------------------------------------------------------------#
#Function:  SCOREKEEP_Open()
#----------------------------------------------------------------------------#
def SCOREKEEP_Open(strFilename):
    dictSCORE = dict()
    dictSCORE["strFilename"]=strFilename
    try:
#        strFilename = dictSCORE["strFilename"]
        fileScore = open(strFilename,"r")
    except FileNotFoundError:
        fileScore = open(strFilename,"xt")
    dictSCORE["fileScore"]=fileScore
    strRead = fileScore.read()
    linesIn = strRead.splitlines()
    dictSCORE["linesIn"]=linesIn
    return dictSCORE
#
#----------------------------------------------------------------------------#
#Function:  SCOREKEEP_Close()
#----------------------------------------------------------------------------#
def SCOREKEEP_Close(dictSCORE):
    fileScore=dictSCORE["fileScore"]
    if(fileScore!=None):
        fileScore.close()
        strFilename=dictSCORE["strFilename"]
        fileScore=open(strFilename,"w")
        linesIn=dictSCORE["linesIn"]
        nCount=len(linesIn)
        nLines = 0
        for strLine in linesIn:
            strTemp=strLine+"\n"
            fileScore.write(strTemp)
            nLines=nLines+1
        if(nLines==nCount):
            nReturn=1
        else:
            nReturn=0
        fileScore.close()
        fileScore=None
    strFilename=""
    strFilename=None
    linesIn=dictSCORE["linesIn"]
    linesIn.clear()
    linesIn=None
    dictSCORE.clear()
    dictSCORE=None
    return nReturn
