#if order in the file is Name Surname

NameSurname=True

import shutil
import os
import time
import datetime
import math
import urllib
from array import array
import re
import hashlib

override={
#    'ANDERSEN':'J.R.Andersen.1',
#    'AKEROYD':'A.G.Akeroyd.1',
#    'KULESZA':'A.Kulesza.1',
#    'DANIEL':'M.K.Daniel.1',
#    'HAN':'Z.HAN.2',
#    'HU':'B.HU.3',
#    'ILLARIONOV':'Y.Y.Illarionov.1',
#    'ROBERTS':'M.D.Roberts.1',
#    'MARTIN':'A.Martin.4',
#    'SMITH':'C.Smith.1',
    'YEPES TAMAYO':'Juan.Yepes.Tamayo.1',
    'VASQUEZ CARMONA':'J.C.Vasquez.1',
    'GALETA ALONSO':'L.Galeta.2',
    'O\'LEARY':'B.O.Leary.1',
    'PILKINGTON':'T.Pilkington.1',
    'TALBERT JR':'J.Talbert.1',
    'BEA BESADA':'Y.Bea.1',
    'MIR':'M.Faizal.1',
    'RAMIREZ KRAUSE':'I.Ramirez.1',
    'SHABAZI ALONSO':'C.S.Shahbazi.1',
    'ZHAOFENG':'Z.F.Kang.1',
    'COX':'P.J.Cox.1',
    'CHENG':'T.Cheng.1',
    'COLLINS':'J.Collins.1',
    'DAS':'A.Das.1',
    'DAVIES':'J.Davies.999',  # not in the field
    'WILSON':'D.J.Wilson.2',
    'WINKLER':'M.Winkler.1',
    'YAMADA':'M.Yamada.5',
    'YAMAMOTO':'Y.Yamamoto.7',
    'GROEBER':'R.Grober.2',
    'MARTINEZ LIZANA':'J.M.Lizana.1',
    'REGALADO LAMPREA':'D.R.Lamprea.1',
    'SCHUBERT-MIELNIK':'Ulrich.Schubert.1'
}

override2={
    ('GHOSH','TATHAGATA'):'Tathagata.Ghosh.1',
    ('HUANG','PEISI'):'Peisi.Huang.1',
    ('HUANG','DA'):'D.Huang.1',
    ('HUANG','XIAOYUAN'):'Xiao.Yuan.Huang.1',
    ('KIM','DOOJIN'):'Doojin.Kim.1',
    ('KIM','DOYOUN'):'Doyoun.Kim.1',
    ('KIM','JIHUN'):'Jihun.Kim.1',
    ('LI','WENLIANG'):'Wenliang.Li.1',
    ('LI','JINMIAN'):'Jin.Mian.Li.1',
    ('LI','TONG'):'T.Li.2',
    ('LIU','DA'):'Da.Liu.1',
    ('LIU','ZE'):'Ze.Long.Liu.1',
    ('LU','LEI'):'L.Lu.5',
    ('LU','RAN'):'R.Lu.3',
    ('MA','LI'):'L.Ma.6',
    ('TANG','YONG'):'Yong.Tang.1',
    ('WANG','SAI'):'Sai.Wang.1',
    ('WANG','XUANGONG'):'X.G.Wang.2',
    ('WANG','ZHIWEI'):'Z.Wang.13',
    ('YANG','RUNQIU'):'Run.Qiu.Yang.1',
    ('ZHANG','JUE'):'J.Zhang.53',
    ('ZHANG','MENGCHAO'):'M.Zhang.18',
    ('ZHANG','XINYI'):'Xin.Yi.Zhang.1',
    ('ZHOU','JIA'):'Jia.Zhou.1',
    ('LIN','LING'):'L.Lin.14',
    ('KHAN','SUBRATA'):'S.Khan.1',
    ('KIKUCHI','MARIKO'):'M.Kikuchi.1',
    ('MATSUI','TOSHINORI'):'T.Matsui.5',
    ('MURPHY','CHRISTOPHER'):'C.W.Murphy.1',
    ('PENG','CHENG'):'C.Peng.1',
    ('RAO','SOUMYA'):'S.Rao.1',
    ('SUN','SICHUN'):'Si.Chun.Sun.1',
    ('TANG','YONG'):'Yong.Tang.1',

    ('GARCIA TORMO','XAVIER'):'X.Garcia.I.Tormo.1',
    ('KIM','JONG'):'Jong.Soo.Kim.1',
    ('MATTIA','FORNASA'):'Mattia.Fornasa.1',
    ('SCHOENHERR', 'MAREK'):'M.Schonherr.1'
}

keywords=['NLO','QCD','AMPLITUDE','POWHEG','CORRECTION','NNLO','MONTE CARLO','MC','HIGGS','TOP QUARK','TOP PAIR','MSSM','SQUARK','GLUINO','W BOSON','Z BOSON','PHOTON','SUSY','N=4','N=8','1-LOOP','ONE-LOOP','2-LOOP','TWO-LOOP','ELECTRO-WEAK','STRING','UNIFICATION','CP-VIOLATION','GLUON','HEAVY QUARK','JET','NEUTRINO','COSMIC RAY','GUT','SUSY BREAKING','GAUGE MEDIATION','SUPERGRAVITY','RESUMMATION','MASS MIXING','RENORMALIZATION GROUP','RENORMALISATION GROUP','MATHEMATICA','LHC','TEVATRON','ILC','NLL','NNLL','HIGGSLESS','HESS','TOP-PAIR','TOPS','DARK MATTER','WHIMP','STRING','BRANE','PION','DARK','MATTER','SHERPA','HERWIG','J/PSI','TWO-LOOP','CONFORMAL','HOLOGRAPHIC','TECHNICOLOR','GRAVITON','WRAPED','BEYOND THE STANDARD MODEL','EXTRA DIMENSION','EFFECTIVE FIELD THEORY','EFFECTIVE FIELD THEORIES','RANDALL-SUNDRUM','CLIFFORD ALGEBRA','INSTANTONS','HALO','COLOR GLASS CONDENSATE','WIMP','HADRON','LEPTONIC','LEPTON','MIXING','ANTENNA SUBTRACTION','CHARM','BOTTOM','SUM RULE','CP VIOLATION','SCET','WILSON LINE','PARTON DISTRIBUTION','BLACK HOLE','HIGHER DIMENSION','Z BOSON','Z-BOSON','W-BOSON','W BOSON','EXCLUSIVE DECAY','GRAVITATIONAL','QUANTUM MECHANICS','MULTIFIELD','EFFECTIVE THEORY','NONPERTURBATIVE','NON-PERTURBATIVE','DIS','DEEP INELASTIC SCATTERING','QUANTUM','JET QUENCHING','FRAGMENTATION','NUCLEON','AMPLITUDES','SUPER-YANG-MILLS','STERILE','MAJORANA']


def getKeywords(text):
    if len(text) ==0:
        print 'Keyword search for empty string...'
    txt=text.upper()
    #print txt
    allKeys=list()
    for key in keywords:
        n=txt.count(key)
        if n > 0 :
            #print key,' : ',n
            allKeys.append( (n,key) )
    allKeys.sort()
    allKeys.reverse()
    return [x[1] for x in allKeys[0:5]]




def getCiteInfo(source):
    text= source.read()
#    print text
    text=text.replace(' ','')
    text=text.replace('\n' ,'')
#    print text
    tagRegex=re.compile('<[^<]*>')
    text=tagRegex.sub('<>',text)
    text=re.sub('(<>)*<>','<>',text)
#    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
#    print text
#    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    regexTxt=r'Totalnumberofcitations:<>(?P<totalCitationsRaw>\d+,?\d*)<>(?P<pubCitationsRaw>\d+,?\d*)<>Averagecitationsperpaper:<>[^<]*<>[^<]*<>Breakdownofpapersbycitations:<>Renownedpapers\(500\+\)<>(?P<over500>\d+)<>(?P<over500published>\d+)<>Famouspapers\(250-499\)<>(?P<over250>\d+)<>(?P<over250published>\d+)<>Verywell-knownpapers\(100-249\)<>(?P<over100>\d+)<>(?P<over100published>\d+)<>Well-knownpapers\(50-99\)<>(?P<over50>\d+)<>(?P<over50published>\d+)<>Knownpapers\(10-49\)<>(?P<over10>\d+)<>(?P<over10published>\d+)<>Lessknownpapers\(1-9\)<>(?P<over1>\d+)<>(?P<over1published>\d+)<>Unknownpapers\(0\)<>(?P<unknown>\d+)<>(?P<unknownpublished>\d+)<>'
    regex=re.compile(regexTxt,re.IGNORECASE)
    match = regex.search(text)
    if (match):
        return match.groupdict()
    else:
        #print 'No match ! '
        #print text
        return None

def getNameInfo(source,surname):
    text= source.read()
#    print text
    regex=r'<b>.*?'+surname+r',\s.*?</b>'
#    print regex
    names=re.compile(regex,re.IGNORECASE)
    return names.findall(text) 

def getDifferentNamesFromNormal(source,surname):
    text= source.read()
#    print text
    #regex=r'<b>.*?'+surname+r',\s.*?</b>'
    #regex='<a class="authorlink" href="(?P<url>http://inspirebeta.net/author/(?P<name>%s%%2C%%20.*?)\?[^"]*)"' % surname
    #regex='<a class="authorlink" href="(?P<url>http://inspirebeta.net/author/(?P<name>%s%%2C%%20.*?)\?[^"]*)"' % surname 
    regex='<a class="authorlink" href="(?P<url>/author/(?P<name>%s%%2C%%20.*?)\?[^"]*)"' % surname 
    regex='<a class="authorlink" href="(?P<url>/author/profile/(?P<name>%s%%2C%%20.*?)\?[^"]*)"' % surname 
    reg=re.compile(regex,re.IGNORECASE)
#    print regex
    allNames=[]
    allLinks=[]
    for i in reg.finditer(text):
        #print i.group()
        if not i.group('name') in allNames:
            allNames.append(i.group('name'))
            allLinks.append(i.group('url'))
        
    allFinalURL=[]
    allFinalNames=[]
    for nn,ll in zip(allNames,allLinks):
        filehandle = urllib.urlopen('http://inspirebeta.net%s' % ll)
        uu=filehandle.geturl()
        if uu not in allFinalURL:
            allFinalURL.append(uu)
            allFinalNames.append(nn)
    

        return allFinalNames,allFinalURL

    #print set(allNames)
    #print allLinks
    if len(allNames)==0:
        return [],[None]
    h=hashlib.md5()
    h.update(allLinks[0])
    
    filename='cache/%s_name_%s' % (surname,h.hexdigest())
    if not os.path.isfile(filename):
        filehandle = urllib.urlopen('http://inspirebeta.net%s' % allLinks[0])
        refTxt=filehandle.read()
        refTxt2=re.sub('This site is also available.*','',refTxt)
        ff=open(filename,'w')
        ff.write(refTxt2)
        filehandle.close()
    reffile=open(filename)
    refTxt=reffile.read()
    nonEquivalentNames=[allNames[0]]
    for i,link in enumerate(allLinks[1:]):
        h=hashlib.md5()
        h.update(link)
        filename='cache/%s_name_%s' % (surname,h.hexdigest())
        if not os.path.isfile(filename):
            filehandle = urllib.urlopen('http://inspirebeta.net%s' % link)
            txt2=filehandle.read()
            txt2=re.sub('This site is also available.*','',txt2)
            ff=open(filename,'w')
            ff.write(txt2)
            filehandle.close()

        txt=open(filename).read()
        txt2=re.sub('This site is also available.*','',txt)
        if not txt2==refTxt:
            f=open('%s_%d_nameInfo.html' % (surname,i),'w')
            f.write(txt2)
            nonEquivalentNames.append(allNames[i+1])
        #else:
            #print 'names equivalent'
    if len(nonEquivalentNames)>1:
        print 'name not unique %s %s' % (surname,[n.replace('%2C',',').replace('%20',' ') for n in nonEquivalentNames]) 
    return nonEquivalentNames,allLinks


def makeYear(twoDigits):
    if (int(twoDigits)>50):
        return 1900+int(twoDigits)
    else:
        return 2000+int(twoDigits)


newregex=r'abs/arXiv:(?P<yy>\d\d)\d\d\.\d\d\d\d'
oldregex=r'abs/hep\-\w\w/(?P<yy>\d\d)\d\d\d\d\d'
oldPapersRegex=re.compile(oldregex,re.IGNORECASE)
newPapersRegex=re.compile(newregex,re.IGNORECASE)

DESYRegex=re.compile("DESY-(?P<year>\d\d)-\d+",re.IGNORECASE)
NSFRegex=re.compile("NSF-KITP-(?P<year>\d\d)-\d+",re.IGNORECASE)


def getFirstPaper(source):
    text= source.read()
#    print text


    olds=oldPapersRegex.findall(text)
    if len(olds) > 0:
        #print olds
        yrs=map(makeYear,olds)
        yrs.sort()
        return yrs[0]
    else :
        news=newPapersRegex.findall(text)
        #print news
        if len(news)>0:
            #print news
            yrs=map(makeYear,news)
            yrs.sort()
            return yrs[0]
        else :
            print "No papers!"
            return 2099
            

def getFromSpires(authorInfo):
    betterName=override.get(authorInfo['surname'],False)
    # this is if the override is for more that one person with the same surname
    if not betterName:
        print (authorInfo['surname'],authorInfo['firstname'].upper())
        betterName=override2.get((authorInfo['surname'],authorInfo['firstname'].upper()),False)
        print betterName
    if betterName:
        print 'using overrided name ',betterName 
        InspireUrlNormal='http://inspirebeta.net/search?ln=en&ln=en&p=author%%3A%s&action_search=Search&sf=&so=d&rm=&rg=200&sc=0&of=hb' % betterName
        InspireUrlCiteSummary='http://inspirebeta.net/search?ln=en&ln=en&p=author%%3A%s&action_search=Search&sf=&so=d&rm=&rg=200&sc=0&of=hcs' % betterName
        print InspireUrlNormal
    else:
        InspireUrlNormal='http://inspirebeta.net/search?ln=en&ln=en&p=FIND+A+%(surname)s%%2C%(firstname)s&action_search=Search&sf=&so=d&rm=&rg=200&sc=0&of=hb' % authorInfo
    
        InspireUrlCiteSummary="http://inspirebeta.net/search?ln=en&ln=en&p=FIND+A+%(surname)s%%2C%(firstname)s&action_search=Search&sf=&so=d&rm=&rg=100&sc=0&of=hcs" % authorInfo 
    
    InspireUrlNames='http://inspirebeta.net/person/search?q=%(surname)s%%2C+%(firstname)s' % authorInfo
#    print 'urlCiteSummary:',urlCiteSummary
    filename='cache/%(surname)s_%(name)s_CS.html' % authorInfo
    if not os.path.isfile(filename):
        print 'retrieving info from %s ' % InspireUrlCiteSummary
        filehandle = urllib.urlopen(InspireUrlCiteSummary)
        txt=filehandle.read()
        ff=open(filename,'w')
        ff.write(txt)
        ff.close()
        filehandle.close()
        print 'done'
    CSfile=open(filename)
    citeInfo=getCiteInfo(CSfile)

    if citeInfo is None:
        #print 'No information about name %(surname)s' % authorInfo
        return None
    filename='cache/%(surname)s_%(name)s_N.html' % authorInfo
    if not os.path.isfile(filename):
        filehandle = urllib.urlopen(InspireUrlNames)
        ff=open(filename,'w')
        ff.write(filehandle.read())
        filehandle.close()
    Nfile=open(filename)
    differentNames=getNameInfo(Nfile,authorInfo['surname'])
    citeInfo['differentNames']=differentNames
    retry=3
    while retry>0:
        filename='cache/%(surname)s_%(name)s_Normal.html' % authorInfo
        if not os.path.isfile(filename):
            filehandle = urllib.urlopen(InspireUrlNormal)
            ff=open(filename,'w')
            ff.write(filehandle.read())
            filehandle.close()
        Normalfile=open(filename)
        yearOfFirstPaper=getFirstPaper(Normalfile)
        citeInfo['yearOfFirstPaper']=2099
        if (yearOfFirstPaper != 2099):
            citeInfo['yearOfFirstPaper']=yearOfFirstPaper
            retry=0
        else :
            print "Failed to retrieve year of first publication:",yearOfFirstPaper
            print "the url was: ",InspireUrlNormal
            retry-=1

    filename='cache/%(surname)s_%(name)s_Normal.html' % authorInfo

    nf=open(filename)
    differentNames,profilesLinks=getDifferentNamesFromNormal(nf,authorInfo['surname'])
    citeInfo['differentNames']=differentNames
    citeInfo['profileLink']=profilesLinks[0]
    citeInfo['profileLinks']=profilesLinks
    nf.seek(0)
    citeInfo['Keywords']=':'.join(getKeywords(nf.read()))
    topcite=int(citeInfo['over500'])+int(citeInfo['over250'])+int(citeInfo['over100'])+int(citeInfo['over50'])
    topcitePublished=int(citeInfo['over500published'])+int(citeInfo['over250published'])+int(citeInfo['over100published'])+int(citeInfo['over50published'])
    total=int(citeInfo['over500'])+int(citeInfo['over250'])+int(citeInfo['over100'])+int(citeInfo['over50'])+int(citeInfo['over10'])+int(citeInfo['over1'])+int(citeInfo['unknown'])
    totalPublished=int(citeInfo['over500published'])+int(citeInfo['over250published'])+int(citeInfo['over100published'])+int(citeInfo['over50published'])+int(citeInfo['over10published'])+int(citeInfo['over1published'])+int(citeInfo['unknownpublished'])
    citeInfo['topcite']=topcite
    citeInfo['topcitePublished']=topcitePublished
    citeInfo['numberOfPapers']=total
    citeInfo['numberOfPapersPublished']=totalPublished
    citeInfo['totalCitations']=citeInfo['totalCitationsRaw'].replace(',','')
    citeInfo['pubCitations']=citeInfo['pubCitationsRaw'].replace(',','')
    citeInfo.update(authorInfo)
    return citeInfo

def NicePrint(citeInfo):
    print "topCite: %(topcite)s topCitePub: %(topcitePublished)s" % citeInfo 

def CSVPrint(citeInfo,CSVfile):
    try:
        s= "%(surname)s, %(name)s, %(numberOfPapers)s, %(numberOfPapersPublished)s, %(yearOfFirstPaper)s, %(totalCitations)s, %(pubCitations)s, %(topcite)s, %(topcitePublished)s, %(Keywords)s  " % citeInfo 
    except KeyError:
        s= "%(surname)s, %(name)s " % citeInfo
        print "Problem with ",s
        print citeInfo
        
    CSVfile.write(s)
    CSVfile.write('\n')



def HTMLPrint(citeInfo,HTMLfile):
    profilelist=['<a href=%s target="_blank">profile' % citeInfo['profileLink']]
    if len(citeInfo['profileLinks']) >1:
        profilelist=['<a href=%s target="_blank">%d</a>' % (pp[1],pp[0]) for pp in enumerate(citeInfo['profileLinks'])]
        profilelist='\n'.join(profilelist)

    citeInfo['profilelist']=profilelist
    #print profilelist
    try:
        s= """
<tr>
<td><a href=cache/%(htmlName)s_CS.html>cite summary </a></td>
<td><a href=cache/%(htmlName)s_Normal.html>papers</a></td>
<td>%(profilelist)s</td>
<td>%(surname)s</td>
<td>%(name)s</td>
<td>%(numberOfPapers)s</td>
<td>%(numberOfPapersPublished)s</td>
<td>%(yearOfFirstPaper)s</td>
<td>%(totalCitations)s</td>
<td>%(pubCitations)s</td>
<td>%(topcite)s</td>
<td>%(topcitePublished)s</td>
<td>%(Keywords)s</td>
</tr>
""" % citeInfo 
    except KeyError:
        s= "%(surname)s, %(name)s " % citeInfo
        print "Problem with ",s
        #print citeInfo
    HTMLfile.write(s)
    HTMLfile.write('\n')


def GetInfo(surname,name):
    authorInfo={'surname':surname.upper(),'name':name.upper(),'initial':name[0].upper()} 
    htmlname='%(surname)s_%(name)s' % authorInfo
    authorInfo['htmlName']=htmlname.replace(' ','%20')
    authorInfo['firstname']=name.split(' ')[0]
#    print authorInfo
    return getFromSpires(authorInfo)

#authorInfo={'surname':'Goertz'.upper(),'name':'Florian'.upper(),'initial':'F'.upper()} 


names=[
('Spanos','Vassilis') , ('Sanz','Veronica')
]

#citeInfo=GetInfo('Spanos','Vassilis')
#citeInfo=GetInfo('Dixon','Lance')
#citeInfo=GetInfo('Sanz','Veronica')

CSVfile=open('postdocs.csv','w')

def extractName(st):
    
    tt=st.replace('\t',',').split(',')
    print tt
    if len(tt)>1 :
         print  [tt[0].rstrip().lstrip(),tt[1].rstrip().lstrip()]    
         return [tt[0].rstrip().lstrip(),tt[1].rstrip().lstrip()]    
    if len(tt)==1 :
        tt=tt[0].rstrip().lstrip().split(' ') 
        if len(tt)==2:
            print  [tt[0].rstrip().lstrip(),tt[1].rstrip().lstrip()]    
            return [tt[0].rstrip().lstrip(),tt[1].rstrip().lstrip()]    
        else:
            print "not unique name-surname split for %s, please add a comma!" % st
        return [tt[0].rstrip().lstrip(),' '.join([ ttt.rstrip().lstrip() for ttt in tt[1:]]).rstrip().lstrip() ]    

namefile=open('names')
allnames=namefile.readlines()
#print allnames
thenames=map(extractName,allnames)
names=filter(
lambda e: e not in names,
thenames
)

names=set([ (a[0],a[1]) for a in names])
names=list(names)
names.sort()

print names


if NameSurname:
    names=[[l[0],l[1]] for l in names]
else:
    names=[[l[1],l[0]] for l in names]
print names

#import sys
#sys.exit(0)

htmlfile=open('index.html','w')

htmlfile.write("""
<!DOCTYPE html>
<html>
<body>

<h1>Postdocs</h1>

<p>
<ul>
<li> NOP: number of papers 
<li> NOPP: number of papers published 
<li> YFP: yearOfFirstPaper
<li> TC: totalCitations
<li> PC: published citations
<li> topC: number of topcite papers
<li> topCP: number of topcite papers published
</ul>
</p>
<table border="1">
<tr>
<td></td>
<td></td>
<td></td>
<td>surname</td>
<td>name</td>
<td>NOP</td>
<td>NOPP</td>
<td>YFP</td>
<td>TC</td>
<td>PC</td>
<td>topC</td>
<td>topCP</td>
<td>Keywords</td>
</tr>
"""
)

noInfo=[]

for name in names:
    print "Processing: %s, %s" % (name[0],name[1])
    citeInfo=GetInfo(name[0],name[1])
    if citeInfo is None:
        print "No info for",name[0],' ',name[1]
        noInfo.append(name)
    else :
        CSVPrint(citeInfo,CSVfile)
        CSVfile.flush()

        HTMLPrint(citeInfo,htmlfile)
        if  len(citeInfo['differentNames'])>1:
            print "Possible multiple names for ",name[0],' ',name[1]
            print citeInfo['differentNames']
            
CSVfile.close()

htmlfile.write("""

</table>
</body>
</html>
""")

htmlfile.close()


print "No Info for:"
for i in noInfo:
    print ' '.join(i)
