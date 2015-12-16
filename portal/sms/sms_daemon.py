import daemon
import time
from portal.models import SMS
from portal.sms.sms import *

# Daemon function which picks all pending sms from SMS table and sends using send_sms function from sms.py
def sms_daemon():
    print "SMS Daemon Initiated"
    SMSDaemonLogFile = open('portal/sms/SMSDaemonLogFile.log', 'w')
    with daemon.DaemonContext(stdout=SMSDaemonLogFile,stderr=SMSDaemonLogFile):
        while True:
            pending_sms = SMS.objects.filter(status="Pending")
            for sms in pending_sms:
                print "Sending SMS to " + sms.student.first_name + " " + sms.student.last_name + "... ",
                result = send_sms(sms.message_text, sms.phone_number)
                if result == True:
                    print "Success"
                    sms.status = "Success"
                else:
                    print "Failed. Attempt No.:",sms.tries + 1
                sms.tries += 1
                if sms.tries >= 10:
                    sms.status = "Failed" # if tries exceed 10 then it is marked as failed SMS
                sms.save()
            time.sleep(1)
