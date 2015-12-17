from portal.models import StudentBatch, SMS, StudentParent, Parent, Student, Staff, Notice
SIGNATURE = "Your Class Name."

def send_sms(phone_number, text):
    pass

# Function that sends message to parents of absent students
def sms_for_attendance(student_id_list, date, staff_id):

    for student_id in student_id_list:
        student_object = Student.objects.get(id=student_id)
        parent_id = StudentParent.objects.get(student=student_object).parent.id
        parent_phone_number = Parent.objects.get(id=parent_id).phone_number
        text = "Your ward " + student_object.first_name + " " + student_object.last_name + " was absent on " + date + ".\n" + SIGNATURE
        sms_object = SMS(phone_number=parent_phone_number, sms_type = "Attendance", message_text=text, status="Pending", student=student_object, staff=Staff.objects.get(id=staff_id))
        sms_object.save()


def sms_for_notices(student_id_list,notice_title,notice_description,staff_id):

    for student_id in student_id_list:
        student_object = Student.objects.get(id=student_id)
        parent_id = StudentParent.objects.get(student=student_object).parent.id

        parent_phone_number = Parent.objects.get(id=parent_id).phone_number
        text = "Class Notice:\n" + notice_title + "\nNotice Description:\n" +notice_description+'\n'+ SIGNATURE
        sms_object = SMS(phone_number=parent_phone_number, sms_type = "Notice", message_text=text, status="Pending", student=student_object, staff=Staff.objects.get(id=staff_id))
        sms_object.save()


def sms_for_marks(student_batch_id_list):
    pass

# Returns all pending and failed sms sent by the respective staff
def get_pending_sms(staff_id):
    sms_pending_objects = SMS.objects.filter(status="Pending", staff=Staff.objects.get(id=staff_id))
    sms_list = []

    for sms in sms_pending_objects:
        sms_dict = {}
        sms_dict['phone_number'] = sms.phone_number
        sms_dict['student_name'] = sms.student.first_name + " " + sms.student.last_name
        sms_dict['sms_type'] = sms.sms_type
        sms_dict['status'] = sms.status
        sms_dict['retry_link'] = "Put retry link here"
        sms_list.append(sms_dict)

    sms_failed_objects = SMS.objects.filter(status="Failed", staff=Staff.objects.get(id=staff_id))

    for sms in sms_failed_objects:
        sms_dict = {}
        sms_dict['phone_number'] = sms.phone_number
        sms_dict['student_name'] = sms.student.first_name + " " + sms.student.last_name
        sms_dict['sms_type'] = sms.sms_type
        sms_dict['status'] = sms.status
        sms_dict['retry_link'] = "Put retry link here"
        sms_list.append(sms_dict)

    return sms_list
