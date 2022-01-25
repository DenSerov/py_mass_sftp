import subprocess
import time
import sys
import zlib
from zlib import decompressobj, MAX_WBITS


#def myJob2(pipe_inpus):
#  

def myJob(fname, pipe_input):
  bsize=1024*1024
  f=open(fname,'wb')
  buffer=ssh.stdout.read(bsize)
  while buffer:
    f.write(buffer)
    buffer=ssh.stdout.read(bsize)
  f.close()

#p_output, p_input = Pipe()  #writer() writes to p_input from _this_ process
#reader_p = Process(target=myJob, args=((p_output, p_input),))
#reader_p.daemon = True
#reader_p.start()     # Launch the reader process

user=input('Enter username [admin]: ')
if user=='': user='admin'

password=input('Enter Password: ')
if password=='': 
  print('Error. Password can not be blank.')
  exit(0)

address=sys.argv[1]
path=sys.argv[2]
if password!='': delim=':'
else: delim=''

logsizes={}
print(user,password,address,path)
url='sftp://'+user+delim+password+'@'+address+path
#print(url)
#url='sftp://admin:bycast@dc1-adm1.demo.netapp.com/var/local/audit/export/'
#print(url)

print(url)
ssh = subprocess.Popen(['curl','--silent','--insecure',url],stdout=subprocess.PIPE)
#print('launched')
i=1
for line in ssh.stdout:
  line=line.decode()[:-1]
  words=line.split()
  fname=words[-1]
  fsize=int(words[4])
  if not fname.startswith('.'):
    logsizes[fname]=fsize
  print(i,fname,fsize)

for fname in logsizes:
  start = time.time()
  url = 'sftp://'+user+delim+password+'@'+address+path+fname
  ssh = subprocess.Popen(['curl', '--silent','--insecure',url],stdout=subprocess.PIPE)
  myJob(fname, ssh.stdout)
  elapsed=time.time()-start
  speed=round(logsizes[fname]/elapsed/1024/1024,1)
  print('{0:22s}: {1:2.3f} seconds. {2:3.3f} MB/sec'.format(fname,elapsed,speed))
