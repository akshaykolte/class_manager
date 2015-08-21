# Student Search

The implemented student search provides you with the fuctionality to open a new child browser window on clicking a button (student search button). The end user can then search for student_id or student_batch_id as required. After the end user chooses a Student or StudentBatch, the child browser window returns the value of the selected Student ID/StudentBatch ID to an input form of the parent browser window.

Note that using the implemented search means only changing the html files to fetch the Student ID or StudenetBatch ID from the child browser window.

Use the two code samples given in the documentation to integrate the implementation with your code.

### To use the student search facility in your code follow these steps:

 - Make sure that the logged in user is manager, accountant or admin
 
 - Copy the following code in your html file (preferably in base_*.html folder):
 
 ```
  <script>
  	function call_student_search_window(type) {
  		window.open("/student-search/?type="+type,"name_" + Math.random(), "toolbar=1,status=1,");
  	}
  </script>
 ```
 
 - Call the student search when a button is clicked.
   In the following code, the following needs to be taken care of:
   - Make sure that the input field (which needs to be filled with the Student/StudentBatch ID has the parameter id="chooseStudentId" or id="chooseStudentBatchId" appropriately
   - Replace {{your_search_type}} with 'student' or 'studentbatch' depending on the need to search for student_id or student_batch_id respectively
   - Replace {{your_name}} by the name you want to give to the input.
  
 - Reference code 2:
 
 ```  
<div class="form-group input-group">
    <input type="text" name="{{your_name}}" class="form-control" id="chooseStudentId" onchange="this.form.submit()">
    <span class="input-group-btn">
      <button class="btn btn-default" type="button"><i class="fa fa-search" onClick="call_student_search_window('{{your_search_type}}')"></i>
      </button>
		</span>
</div>
 ```
