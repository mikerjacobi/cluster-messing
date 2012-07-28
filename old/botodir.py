import boto
import datetime

akid="AKIAJRRUC3AJVTIAFL4A"
sak="5OJBVRNx3IBwtSz/VO+T8JxSD+8IzPfjgGjia519"

ec2conn=boto.connect_ec2(akid,sak)
asconn=boto.connect_autoscale(akid,sak)
cwconn=boto.connect_cloudwatch(akid,sak)

metricList=cwconn.list_metrics()
cpumetric=metricList[26]

end = datetime.datetime.now()-datetime.timedelta(hours=5)
start = end - datetime.timedelta(hours=5)
frequency=60 #frequency is in seconds

myQuery=cpumetric.query(start,end,'Average','Percent', frequency)
print "MYQUERY"
print myQuery[0]

print "\n\nDIR"
print dir(boto)

