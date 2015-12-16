from urllib import quote
import requests

def send_sms(message_text, phone_number):

    text = quote(message_text)
    api_string = "http://bhashsms.com/api/sendmsg.php?user=9404792579&pass=8ac45b9&sender=MDHOBI&phone="+str(phone_number)+"&text="+text+"&priority=ndnd&stype=normal"
    try:
    	return_string = requests.get(api_string).text
    	return True
    except:
        return False
