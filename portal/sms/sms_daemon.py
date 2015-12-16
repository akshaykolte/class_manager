import daemon
import time
from portal.models import SMS
from portal.sms.sms import *
def sms_daemon():

    with daemon.DaemonContext():
        while True:
            pending_sms = SMS.objects.filter(status="Pending")
            for sms in pending_sms:
                print "Sending SMS to " + sms.student.last_name
                result = send_sms(sms.message_text, sms.phone_number)
                if result == True:
                    print "Success"
                    sms.status = "Success"
                else:
                    print "Failed"
                sms.tries += 1
                if sms.tries >= 10:
                    sms.status = "Failed"
                sms.save()
            time.sleep(1)
