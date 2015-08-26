# Staff Search

The implemented staff search provides you with the fuctionality to open a new child browser window on clicking a button (staff search button). The end user can then search for staff_id. After the end user chooses a Staff, the child browser window returns the value of the selected Staff ID to an input form of the parent browser window.

Note that using the implemented search means only changing the html files to fetch the Staff ID from the child browser window.

Use the two code samples given in the documentation to integrate the implementation with your code.

### To use the staff search facility in your code follow these steps:

 - Make sure that the logged in user is admin
 
 - Copy the following code in your html file (preferably in base_*.html folder):
 
 ```
  <script>
  	function call_staff_search_window(type) {
  		window.open("/staff-search/?type="+type,"name_" + Math.random(), "toolbar=1,status=1,");
  	}
  </script>
 ```
 
 - Call the staff search when a button is clicked.
   In the following code, the following needs to be taken care of:
   - Make sure that the input field (which needs to be filled with the Staff ID has the parameter id="chooseStaffId" appropriately
   - Replace {{your_search_type}} with 'staff' depending on the need to search for staff_id
   - Replace {{your_name}} by the name you want to give to the input.
  
 - Reference code 2:
 
 ```  
<div class="form-group input-group">
    <input type="text" name="{{your_name}}" class="form-control" id="chooseStaffId" onchange="this.form.submit()">
    <span class="input-group-btn">
      <button class="btn btn-default" type="button" onClick="call_staff_search_window('staff')">
        <i class="fa fa-search"> &nbsp;or search for staff</i>
      </button>
    </span>
</div>
 ```

 - A sample implementation can be found out at the url: TODO
