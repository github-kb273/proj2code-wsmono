#from scorekeep import *
from flask import Flask
from flask import redirect,url_for,render_template,jsonify
from flask import request
import requests

#
# #
# #
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
#
#
#----------------------------------------------------------------------------#
#Function:  funcCheckGuess()
#----------------------------------------------------------------------------#
def funcCheckGuess(strInGuess,strInWord):
    strInGuess=strInGuess.upper()
    strInWord=strInWord.upper()
    nLenGuess=len(strInGuess)
    nLenWord=len(strInWord)
    nScore=0
    strScore=""
    for nLoop in range(0,nLenWord):
        if(nLoop<nLenGuess):
            if(strInWord[nLoop]==strInGuess[nLoop]):
                strScore=strScore+str("O")
                nScore=nScore+1
            else:
                strScore=strScore+str("X")
        else:
            strScore=strScore+str("?")
        if(gdictGlobal["bDebug"]!=False):
            print(f"funcCheckGuess()::{nLoop}:{strScore}:nS{nScore}:lenG{nLenGuess}:lenW{nLenGuess}")
#    nTemp=nScore+1
    if((nScore==nLenWord) and (nScore==nLenGuess)):
        if(gdictGlobal["bDebug"]!=False):
            print(f"win {nScore}:{nLenWord}:{nLenGuess}")
        strScore="*"
    else:
        if(gdictGlobal["bDebug"]!=False):
            print(f"lose {nScore}:{nLenWord}:{nLenGuess}")
    return strScore
#
#
#----------------------------------------------------------------------------#
#Global main()
#----------------------------------------------------------------------------#
gdictGlobal=dict()
gdictGlobal["nGuessCount"]=int(0)  #init guess count
gdictGlobal["strHeader"]="Header<BR>"
gdictGlobal["strFooter"]="Footer<BR>"
gdictGlobal["strContent"]="Content<BR>"
gdictGlobal["strPOSTURL"]="http://127.0.0.1:5000/formpost"
listGuess=[]
gdictGlobal["listGuess"]=listGuess
listCheck=[]
gdictGlobal["listCheck"]=listCheck
listWords=[]
gdictGlobal["listWords"]=listWords
gdictGlobal["nWordCount"]=int(0)
gdictGlobal["strCount"]="Count<BR>"
gdictGlobal["strCategory"]="Category<BR>"
gdictGlobal["bDebug"]=bool(False)
#
app=Flask(__name__,
          template_folder="templates",
          static_folder="static")
#
#----------------------------------------------------------------------------#
#Function:  getguess()
#****make single render_template()****
#----------------------------------------------------------------------------#
@app.route("/getguess")
def getguess():
    print("getguess():Enter")
    strGuess=request.args.get("wordguess")  #Obtain user word guess
    strUsername=request.args.get("username") #Obtain user name
#
    strGuess=strGuess.upper()
    strUsername=strUsername.upper()
 #
    #increment guess count
    nGuessCount=int(gdictGlobal["nGuessCount"])
    nGuessCount=nGuessCount+1  #increment guess count
    gdictGlobal["nGuessCount"]=int(nGuessCount)   
#
    strCount=str(nGuessCount)  #Guess count string
    print(f"getguess():  guess count {strCount}")
    listGuess=gdictGlobal["listGuess"]
    listCheck=gdictGlobal["listCheck"]
#
    listWords=gdictGlobal["listWords"]
    nSelect=gdictGlobal["nWordSelect"]
    listSep=listWords[nSelect].split(',')
    print(f"Comma: {listSep[0]},{listSep[1]},{listSep[2]}")
    strCategory=listSep[1]
    strLength=len(listSep[2])
    strWinWord=listSep[2]
    gdictGlobal["strWinWord"]=strWinWord
    nWinWordLen=len(strWinWord)
#
    strCheck=funcCheckGuess(strGuess,strWinWord)
    dictSCORE=SCOREKEEP_Open(gstrFILENAME_SCORE)
    if(strCheck != "*"):
#        print(f"Check:{strCheck}-G{strGuess}-W{strWinWord}")
#        print("Get guess.")
#
#    strTemp=strGuess+"["+strCheck+"]"
        strTemp=strGuess
        if(strGuess == ""):
            strTemp="[*empty*]"
        listGuess.append(strTemp)
        listCheck.append(strCheck)
#
        strContent="<TABLE>"
        nLines=len(listGuess)
        for nLoop in range(0,nLines):
            strGuess0=str(listGuess[nLoop])
            strCheck0=str(listCheck[nLoop])
            strContent=strContent+"<FONT SIZE=4><TR><TD>"+strGuess0+"</TD><TD>["+strCheck0+"]"+"</TD></TR></FONT>"
#            print(f"getguess()::strG{strGuess0}:strC{strCheck0}")
        strContent=strContent+"</TABLE>"
        #
        strTemp=f"getguess():WinWord={strWinWord} Guess={strGuess} Count={strCount}"
        print(f"getguess():{strTemp}")
        if(strGuess==""):
            strTemp="[*empty*]"
        else:
            strTemp=strGuess.upper()
        strCount0=strCount
        strHeader=f"<FONT SIZE=5>Guess my word.  <BR>Guess: {strTemp} --- Guess number: {strCount}</FONT><BR>"
        if(strUsername==""):
            strFooter=f"<FONT SIZE=5>Guess my word.</FONT><BR>"
        else:
            strFooter="<FONT SIZE=5>Guess my word, " + strUsername + ".</FONT><BR>"
#        strFooter="<FONT SIZE=5>Guess my word.</FONT><BR>"
        gdictGlobal["strHeader"]=strHeader
        gdictGlobal["strFooter"]=strFooter
        gdictGlobal["strContent"]=strContent
        strPOSTURL=gdictGlobal["strPOSTURL"]
#    if(strCheck!="*"):
        strCategory=f"My word is a {strCategory} and {strLength} letters long.<BR>"
        print(f"getdguess():{strCategory}")
#        strGuessCount=str(gdictGlobal["nGuessCount"])
#        print(f"getguess():  guess count {strCount}")
        nWordScore=""
        if(strUsername!=""):
#            dictSCORE=SCOREKEEP_Open(gstrFILENAME_SCORE)
            nWordScore=10*nWinWordLen-1*(nGuessCount)
            strWordScore=f"The word score is {nWordScore}."
            nLifeScore=gdictGlobal["nLifeScore"]
            nLifeScore=SCOREKEEP_GetScore(dictSCORE,strUsername)
            strLifeScore=f"<BR>{strUsername} has {nLifeScore} points."
            strGuessCount0=f"<FONT SIZE=4>There has been {strCount0} guess(es).  "+ strWordScore + strLifeScore + "</FONT><BR>"
#            SCOREKEEP_Close(dictSCORE)
        else:
            strGuessCount0=f"<FONT SIZE=4>There has been {strCount0} guess(es).</FONT><BR>"
#        print("getguess()::strCount:{strCount}")
        gdictGlobal["strCategory"]=strCategory
        gdictGlobal["strUsername"]=strUsername
        gdictGlobal["strCount"]=strGuessCount0
#        print(f"getguess():  guess count {strGuessCount0} {strCount}")
#        strReturn = render_template("wordfun.html",
#                                    htmlHeader0=strHeader,
#                                    htmlFooter0=strFooter,
#                                    htmlContentList0=strContent,
#                                    htmlPOSTURL=strPOSTURL,
#                                    htmlCount=strCount,
#                                    htmlCategory=strCategory)
#        strReturn = redirect(url_for("getguess",
#                                    htmlHeader0=strHeader,
#                                    htmlFooter0=strFooter,
#                                    htmlContentList0=strContent,
#                                    htmlPOSTURL=strPOSTURL))
#        strReturn=redirect("/",code=302)
#        print(f"{strReturn}")
    else:
        #Player guessed word.
        print(f"Check:{strCheck}")
        print("Player guessed word.")
        strWord0=strWinWord.upper()
        #increment word selection
        nSelect=gdictGlobal["nWordSelect"]
        listWords=gdictGlobal["listWords"]
        nWordLen=len(listWords)
        nSelect=nSelect+1
        if(nSelect>=nWordLen):
            nSelect=0
        gdictGlobal["nWordSelect"]=int(nSelect)
        #
        strTemp=listWords[nSelect]
        listSep=strTemp.split(",")
        strWinWord=listSep[2]
        strLength=str(len(listSep[2]))
        strCategory=listSep[1]
#        print(f"getguess()::strNew{strWinWord} and select {nSelect}:{strLength}:{strCategory}")
#        
        gdictGlobal["strLength"]=strLength
        gdictGlobal["strCategory"]=strCategory
        strLifeScore=""
        if(strUsername!=""):
            nWordScore=10*nWinWordLen-1*(nGuessCount)
            strWordScore=f"The word score is {nWordScore}."
            dictSCORE["strUsername"]=""
            dictSCORE["strScore"]=""
            nLifeScore=SCOREKEEP_AddScore(dictSCORE,strUsername,nWordScore)
            strUsername=dictSCORE["strUsername"]
            nWordScore=int(dictSCORE["strScore"])
            gdictGlobal["nLifeScore"]=nLifeScore
            strLifeScore=f"<BR>{strUsername} has {nLifeScore} points."
#            strCount="<FONT SIZE=4>There has been "+strCount+f" guess(es).  "+ strWordScore + strLifeScore + "</FONT><BR>"
        strCount="<FONT SIZE=4>I have selected a new word.  Guess my word."+ strLifeScore +"</FONT><BR>"
        strCategory=f"My word is a {strCategory} with {strLength} letters.<BR>"
        gdictGlobal["strCount"]=strCount
        strGuessCount=str(gdictGlobal["nGuessCount"])
        strHeader=f"<FONT size=5>You guessed my word in {strGuessCount} tries/try.  My word is {strWord0}.</FONT><BR>"
        if(strUsername==""):
            strFooter=f"<FONT size=5>Guess My Word.</FONT><BR>"
        else:
            strFooter=f"<FONT size=5>Guess My Word, " + strUsername + ".</FONT><BR>"
        print(f"getguess()::strF{strFooter}")
        listGuess.append(strGuess)
        listCheck.append(strCheck)
        strContent="<TABLE>"
        nLines=len(listGuess)
        for nLoop in range(0,nLines):
            strGuess0=str(listGuess[nLoop])
            strCheck0=str(listCheck[nLoop])
            strContent=strContent+"<FONT SIZE=4><TR><TD>"+strGuess0+"</TD><TD>["+strCheck0+"]"+"</TD></TR></FONT>"
        strContent=strContent+"</TABLE>"
#        strContent="strContent<BR>"
        strTemp=strGuess.upper()
#        strHeader=f"<FONT SIZE=5>Guess my word.  <BR>Guess: {strTemp} --- Guess number: {strGuessCount}</FONT><BR>"
#        strFooter=f"<FONT SIZE=5>Guess my word {strWinWord}.</FONT><BR>"
        gdictGlobal["strCategory"]=strCategory
        gdictGlobal["strHeader"]=strHeader
        gdictGlobal["strFooter"]=strFooter
        gdictGlobal["strContent"]=strContent
        strPOSTURL=gdictGlobal["strPOSTURL"]
        gdictGlobal["strUsername"]=strUsername
        gdictGlobal["nGuessCount"]=0
        listGuess=gdictGlobal["listGuess"]
        listGuess.clear()
        listGuess=[]
        gdictGlobal["listGuess"]=listGuess
        listCheck=gdictGlobal["listCheck"]
        listCheck.clear()
        listCheck=[]
        gdictGlobal["listCheck"]=listCheck
#        strReturn=redirect("/",code=302)
    SCOREKEEP_Close(dictSCORE)
    strReturn = render_template("wordfun.html",
                                htmlHeader0=strHeader,
                                htmlFooter0=strFooter,
                                htmlContentList0=strContent,
                                htmlPOSTURL=strPOSTURL,
                                htmlCount=strCount,
                                htmlCategory=strCategory,
                                htmlUsername=strUsername)
#    strReturn=redirect("/",code=302)
    print("getguess():Exit")
    return strReturn
#
#----------------------------------------------------------------------------#
#Function:  home()
#----------------------------------------------------------------------------#
@app.route("/")
def home():
    print("home():Enter")
#
#    listWords=gdictGlobal["listWords"]
#
#    nSelect=gdictGlobal["nWordSelect"]
#    nC=len(listWords)
#    print(f"select: {nSelect} {nC}")
#    strTemp=listWords[nSelect]
#    print(f"split: {strTemp}")
#    listSep=strTemp.split(",")
#    strTemp=listSep[0]
#    print(f"Comma0: {strTemp}")
#    strTemp=listSep[1]
#    print(f"Comma1: {strTemp}")
#    strTemp=listSep[2]
#    print(f"Comma2: {strTemp}")
#    gdictGlobal["strCategory"]=listSep[1]
#    gdictGlobal["strLength"]=len(listSep[2])
#    gdictGlobal["strWinWord"]=listSep[2]
    strCategory=gdictGlobal["strCategory"]
    strHeader=gdictGlobal["strHeader"]
    strFooter=gdictGlobal["strFooter"]
    strContent=gdictGlobal["strContent"]
    strPOSTURL=gdictGlobal["strPOSTURL"]
    strCount=gdictGlobal["strCount"]
    strCategory=gdictGlobal["strCategory"]
    strUsername=gdictGlobal["strUsername"]
#    strGuessCount=str(gdictGlobal["nGuessCount"])
#    strLength=gdictGlobal["strLength"]
#    strCategory=f"<FONT SIZE=4>My word is {strLength} letters long and a {strCategory}.</FONT><BR>"
#    strCount="<FONT SIZE=4>There has been "+strGuessCount+" guesses.</FONT><BR>"
    strReturn = render_template("wordfun.html",
                                htmlHeader0=strHeader,
                                htmlFooter0=strFooter,
                                htmlContentList0=strContent,
                                htmlPOSTURL=strPOSTURL,
                                htmlCount=strCount,
                                htmlCategory=strCategory,
                                htmlUsername=strUsername)
    print("home():Exit")
    return strReturn
#
#----------------------------------------------------------------------------#
#Function:  formpost()
#----------------------------------------------------------------------------#
@app.route("/formpost",methods=["POST","GET"])
def formpost():
    print("formpost():Enter")
    if(request.method=="POST"):
        strGuess=request.form["wordguess"]
        strUsername=request.form["username"]
    else:
        strGuess=request.args.get("wordguess")
        strUsername=request.args.get["username"]
#    nGuessCount=int(gdictGlobal["nGuessCount"])
#    nGuessCount=nGuessCount+1
#    gdictGlobal["nGuessCount"]=int(nGuessCount)    
    dictParams=dict()
    dictParams["wordguess"]=strGuess.strip()
    dictParams["username"]=strUsername.strip()
    requests.get(url="http://127.0.0.1:5000/getguess",params=dictParams)
#    strReturn="FORMPOST<BR>"
#    strReturn=redirect(())
    print("formpost():Exit")
    strReturn=redirect("/")
    return strReturn
#
#
#----------------------------------------------------------------------------#
#Function:  app.run()
#----------------------------------------------------------------------------#
if(__name__=="__main__"):
    print("app.run()")
#  Load word set from file
    fileWords=open("wordlist.txt","r")
    strFile=fileWords.read()
    lineFile=strFile.split()
    fileWords.close()
#
    listWords=gdictGlobal["listWords"]
    for strLine in lineFile:
        listWords.append(strLine)
#        print(f"Word:{strLine}")
#
    nSelect=1
    nCheck=len(listWords)
    if(nSelect<nCheck):
        gdictGlobal["nWordSelect"]=nSelect
    else:
        gdictGlobal["nWordSelect"]=0
#
    listWords=gdictGlobal["listWords"]
#
    nSelect=gdictGlobal["nWordSelect"]
    strTemp=listWords[nSelect]
    listSep=strTemp.split(",")
    strCategory=listSep[1]
    gdictGlobal["strCategory"]=listSep[1]  #Word category
    gdictGlobal["strLength"]=str(len(listSep[2]))  #Get length of guess word
    gdictGlobal["strWinWord"]=listSep[2]  #Word to guess
#    gdictGlobal["nGuessCount"]=int(0)
    strCount=str(gdictGlobal["nGuessCount"])  #guess count string
    strLength=gdictGlobal["strLength"]
#    strCategory=gdictGlobal["strCategory"]
    strCategory=f"<FONT SIZE=4>My word is a {strCategory} and has {strLength} letters.</FONT><BR>"
    strCount="<FONT SIZE=4>There has been "+strCount+" guesses.</FONT><BR>"
    gdictGlobal["strCount"]=strCount  #String message for guess count
    gdictGlobal["strCategory"]=strCategory  #String message for category output
    gdictGlobal["strUsername"]=""
    gdictGlobal["nLifeScore"]=0
#
    app.run(debug=True)
