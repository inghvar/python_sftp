import shutil
import paramiko
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(levelname)s: %(message)s')
logHandler = TimedRotatingFileHandler('./log_sftp.log', when='D', interval=1)
#logHandler.suffix = '_%Y%m%d'
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


HOSTNAME = '000.000.000.00'
USERNAME = 'admin'
PASSWORD = 'mypassword'
PRIVATE_KEY = '/home/myname/.ssh/ssh_key'
PORT = 22

download_remotepath = './'
download_localpath = './'
upload_remotepath = './'
upload_localpath = './to_upload'
remotefile = 'remotefile.txt'
localfile = 'localfile.txt'



def establish_connection(host, username, password, port, private_key):
    """ Connects and logs into the specified hostname. """
    try:
        transport = paramiko.Transport((host, port))
        # by password
        transport.connect(None, username, password)
        # by private key
        #transport.connect(None, username, private_key)

        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp
    except Exception as e:
        transport_live = False
        logger.info('An error occurred creating SFTP client: %s: %s' % (e.__class__, e))
        return transport_live


def list_remote_dir():
    """ show directories on the remote host. """
    sftpclient = establish_connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, 
                                        port=PORT, private_key=PRIVATE_KEY)
    if sftpclient is False:
        logger.info('Connecting not establish')
    else:
        dirlist = sftpclient.listdir('.')
        for row in dirlist:
            print (row)
        sftpclient.close()


def get_file(download_remotepath, download_localpath, remotefile, localfile):
    """ Download a file from the remote host to the local host. """
    sftpclient = establish_connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, 
                                        port=PORT, private_key=PRIVATE_KEY)
    if sftpclient is False:
        logger.info('Connecting not establish')
    else:
        sftpclient.get(download_remotepath + '/' + remotefile, download_localpath + '/' + localfile)
        logger.info('File is download')
        sftpclient.close()


def put_file(upload_remotepath, upload_localpath, remotefile, localfile):
    """ Upload a file from the local host to the remote host."""
    sftpclient = establish_connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, 
                                        port=PORT, private_key=PRIVATE_KEY)
    if sftpclient is False:
        logger.info('Connecting not establish')
    else:
        sftpclient.put(upload_localpath + '/' + localfile, upload_remotepath + '/' + remotefile)
        shutil.move(upload_localpath + '/' + localfile, 'uploaded/' + localfile)
        logger.info('File is upload')
        sftpclient.close()


#list_remote_dir()
#get_file(download_remotepath, download_localpath, remotefile, localfile)
put_file(upload_remotepath, upload_localpath, remotefile, localfile)