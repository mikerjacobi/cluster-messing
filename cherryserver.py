import cherrypy
import os
import time
import subprocess
import random
import boto
import datetime
import unicodedata
from pymongo import *
import S3

os.system('mongod --dbpath ./mongodatadir &')
time.sleep(3)
c=Connection()
AWS_ACCESS_KEY_ID=open('akid','r').read().split('\n')[0]
AWS_SECRET_ACCESS_KEY=open('sak','r').read().split('\n')[0]

class HelloWorld(object):
    def index(self):
        s='''
           Navigate to:<br>
           /time for a clock <br>
           /cpu for cpu autoscaling <br>
           /paint to see an html5 paint application <br> <br>

        '''
        s+=os.popen('hostname').readline()
        return s
    index.exposed = True

class Paintjs(object):
    def index(self):
        output=""
        f=open("paint.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    index.exposed = True

class Paint(object):
    global c
    global AWS_ACCESS_KEY_ID
    global AWS_SECRET_ACCESS_KEY

    def u2s(self,u):
	#unicode to string
	s=""
	for c in u:
		if ord(c)<128:
			s+=c
	return s

    def index(self, fname='', uname='', pword='', actionInput='', data=None):
	BUCKET_NAME="jacobi-bucket-1"
	conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	generator = S3.QueryStringAuthGenerator(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


	uname=self.u2s(uname)
	pword=self.u2s(pword)
	fname=self.u2s(fname)
	action=self.u2s(actionInput)	
        origpword=pword

        #ROOT='http://localhost:8080/'
	ROOT='http://myloadbalancer-2126499955.us-west-2.elb.amazonaws.com/'
        if pword!='':
            pword=str(hash(pword))
        name='images/'+uname+'.'+fname+'.'+pword+'.png'
	#s3name='images/'+fnamestr+'.png'
        #conn.put(BUCKET_NAME,name,S3.S3Object(str(time.time())),
        #{'Content-Type':'text/plain'}).message
	


        #save file to filesystem and mongo
        #if "save" in action:
	if action=="save":
            data=data.split(',')[-1]
            f=open(name,'wb')
            try:
                #f.write(data.decode('base64'))
		conn.put(BUCKET_NAME,name,S3.S3Object(data.decode('base64')),
		{'x-amz-acl': 'public-read', 'Content-Type':'image/png'}).message
            except:
                pass
            f.close()
            c['pictures']['data'].insert({'path':name,'username':uname,'filename':fname,'password':pword})
        #create output html
        output=''
        f=open('paint.html','r').read().split('\n')

        for l in f:
            #if "load" in action:
	    if action=="load":
                if '</head>' in l:
                    output+='<script type="text/javascript">\n'
                    output+='function loadCanvas()\n{\n'
                    #output+='alert("1");\n'
                    output+='var imageObj = new Image();\n'
                    #output+='alert("2");\n'
                    #fileURL=ROOT+name
		    #generator.calling_format = S3.CallingFormat.PATH
		    fileURL=generator.make_bare_url(BUCKET_NAME,name)
		    print '\n\n'
		    print fileURL
		    print '\n\n'
                    output+='imageObj.src = "'+fileURL+'";\n'
                    #output+='alert("3");\n'
                    output+='var context = document.getElementById("imageView").getContext("2d");\n'
                    #output+='alert("4");\n'
                    output+='var draw = context.drawImage(imageObj,0,0);\n'
                    #output+='alert("5");\n'
                    output+='}\n</script>\n'
                    output+=l+'\n'
                elif '<body' in l:
                    #output+='<body onload="loadCanvas()">\n'
		    output+=l+'\n'
                elif '</body>' in l:
                    output+='<script type="text/javascript" > window.onload=loadCanvas();</script>\n'
                    output+=l+'\n'
                else:
                    output+=l+'\n'
            else: 
                output+=l+'\n'
        output+='Server: <input id="hostname" type="text" value="'+os.popen('hostname').readline().rstrip()+'"/>\n'
        link=ROOT+"paint?uname="+uname+"&fname="+fname+"&pword="+origpword+"&actionInput=load"
        output+="<br><a href='"+link+"'> "+link+"</a>"
        return output
    index.exposed=True
'''
    def upload(self, myFile, username, filename, password):  #,tags):
        if username=="":
            username="DEFAULT"
        password=str(hash(password))
        if filename=="":
            filename="DEFAULT"
        name='images/'+username+'.'+filename+'.'+password+'.png'
        data=myFile.split(',')[-1]
        f=open(name,'wb')
        try:
            f.write(data.decode('base64'))
        except:
            pass
        f.close()
        c['pictures']['data'].insert({'path':name,'username':username,'filename':filename,'password':password})
        return self.index()
    upload.exposed = True

    def download(self, dlUsername, dlFilename, dlPassword):
        #myFile=c['pictures']['data'].find({"username":dlUsername})
        url='"http://localhost:8080/images/'+dlUsername+'.'+dlFilename+'.'+str(hash(dlPassword))+'.png"'
        #size=0
        #for record in myFile:
        #    size+=1
        #    print str(record)
        #print 'size:'+str(size)

        output=''
        f=open('paint.html','r').read().split('\n')
        for l in f:
            if '</head>' in l:
                output+='<script type="text/javascript">\n'
                output+='function loadCanvas()\n{\n'
                output+='var imageObj = new Image();\n'
                output+='imageObj.src = '+url+';\n'
                output+='var context = document.getElementById("imageView").getContext("2d");\n'
                output+='var draw = context.drawImage(imageObj,0,0);\n'
                output+='}\n</script>\n'
                output+=l+'\n'
            elif '<body' in l:
                #output+='<body onload="loadCanvas();">\n'
                output+='<body>\n'
            elif '</body>' in l:
                output+='<script type="text/javascript" > window.onload=loadCanvas();</script>\n'
                output+=l
            else:
                output+=l+'\n'

        return output
    download.exposed=True
'''

class Time(object):
    #this is a network test
    def index(self):
        output=""
        f=open("time.html",'r').read().split('\n')
        for l in f:
            if "timeinputgoeshere" in l:
                output+='<input id="time" type="text" value="'+str(round(time.time()*1000))+'"/>\n'
            else:
                output+=l+'\n'

        output+='<input id="hostname" type="text" value="'+os.popen('hostname').readline()+'"/>\n'
        return output
    index.exposed=True

class CPU(object):
    #this is a CPU test
    def index(self):
        output=""
        f=open("cpu.html",'r').read().split('\n')
        for l in f:
            if 'cpuusagegoeshere' in l:
                users=len(os.popen('ps aux | grep crankcpu').read().split('\n'))-3
                cpu=0
                if users<6:
                    pid=subprocess.Popen(['python', 'crankcpu.py', '&']).pid
                    os.system('cpulimit -l 10 -p '+str(pid)+' &')
                    time.sleep(1)
                for c in os.popen('ps -e -o pcpu | grep -v 0.0').read().split('\n')[1:-1]:
                    cpu+=float(c)
                color = 'rgb('+str(int(cpu/100*255))+',30,30)'
                output+='<input id="cpu" type="text" value="'+str(cpu)+'"/> <br> \n'
                output+='<label>users: </label>\n'
                output+='<input id="users" type="text" value="'+str(users)+'"/>\n'
                output+='<input id="hostname" type="text" value="'+os.popen('hostname').readline()+'"/>\n'
            else:
                output+=l+'\n'
        return output
    index.exposed=True

class IO(object):
    def index(self):
        output=""
        io={}
        f=open("io.html",'r').read().split('\n')
        for l in f:
            if "iogoeshere" in l:
                name='io.'+str(int(random.random()*10000))
                os.system('python crankio.py &')
                os.system('(iotop -k -o -b -qq -P -d .5| grep junk) > '+name+' &')
                time.sleep(5)
                data=os.popen('cat '+name).read().split('\n')
                for d in data:
                    print d
            else:
                output+=l+'\n'
        return output
    index.exposed=True

class Monitor(object):
    def index(self,s=1,e=0,f=60):
	global AWS_ACCESS_KEY_ID
	global AWS_SECRET_ACCESS_KEY

        s=int(s)
        e=int(e)
        f=int(f)
        #AWS_EC2_URL="http://aws.amazon.com/ec2/"
        CWconn=boto.connect_cloudwatch(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        metrics=CWconn.list_metrics()
        cpuMetrics={}
        key=''
        for m in metrics:
            if 'CPUUtilization' in str(m):
                try:
                    key=str(m.dimensions['InstanceId'])
                    cpuMetrics[key]=m
                except:
                    cpuMetrics['--"Average"-']=m


        #search

        end = datetime.datetime.now()-datetime.timedelta(hours=e)
        start = end - datetime.timedelta(hours=s)

        allCpus=[]

        #get times
        timeQuery=cpuMetrics[key].query(start,end,'Average','Percent', f)
        times=[]
        for d in timeQuery:
            t=str(d['Timestamp']).split(' ')
            #times.append(t[0]+'<br>'+t[1])
            times.append(d['Timestamp'])

        times.sort()
        for i in range(len(times)):
            t=str(times[i]).split(' ')
            times[i]=t[0]+'<br>'+t[1]

        output=""
        file=open('monitor.html','r').read().split('\n')
        for l in file:
            if 'xAxis:' in l:
                output+=l+'\n'
                output+='categories: '+str(times)+',\n'
            elif 'series:' in l:
                output+=l+'\n'
                for instance in cpuMetrics.keys():
                    data=cpuMetrics[instance].query(start,end, 'Average', 'Percent', f)
                    cpus=[]
                    for d in data:
                        cpus.append(d['Average'])
                    output+="{name: "+instance[2:-1]+",\n"
                    output+="data: "+str(cpus)+"},\n"
                '''
                i=1
                for instance in allCpus:
                    output+="{name: "+str(i)+",\n"
                    output+="data: "+str(instance)+"},\n"
                    i+=1
                '''
            else:
                output+=l+'\n'
        return output
    index.exposed=True

class Clean(object):
    def index(self):
        os.system('killall -s 9 iotop')
        os.system('killall -s 9 cp')
        return ''
    index.exposed=True

root=HelloWorld()
root.time=Time()
root.cpu=CPU()
root.paint=Paint()
root.paintjs=Paintjs()
#root.io=IO()
#root.clean=Clean()
root.monitor=Monitor()

PATH='/home/mike/Documents/ws/images/'
cherrypy.tree.mount(root, '/images', config={'/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH,
                'tools.session.timeout': 5,
                #'tools.staticdir.index': 'index.html',
            },
    })

cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':8080})
cherrypy.quickstart(root)






