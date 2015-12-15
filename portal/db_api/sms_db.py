from portal.models import StudentBatch, SMS, StudentParent, Parent
SIGNATURE = "Your Class Name."

def send_sms(phone_number, text):
    pass

# Function that sends message to parents of absent students
def sms_for_attendance(student_id_list, date):

    for student_id in student_batch_id_list:
        parent_id = StudentParent.objects.get(student__id=student_id)
        parent_phone_number = Parent.objects.get(id=parent_id).phone_number
        text = "Your ward " + student_object.first_name + " was absent on " + date + ". " + SIGNATURE
        sms_object = SMS(phone_number=parent_phone_number, sms_type = "Attendance", message_text=text, status="Pending", student=student_object)
        sms_object.save()


def sms_for_notices(student_batch_id_list):
    pass

def sms_for_marks(student_batch_id_list):
    pass
