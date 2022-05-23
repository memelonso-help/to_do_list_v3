Change elaborate textbox to textarea and find a way to reference (done)
Change to modal pages(done)
Need to highlight which pages you are on (what does this even mean, can be achieved by beautifying the page and introducing page distinctions)
Be able to select multiple check boxes using shift and control (later, this is javascript)
Allow a way to retain passwords and reset passwords 
Figure out how to remember users (flask loginmanager and flask-wtf, done)
Remove the details when form has been submitted (I will have to live with this one since I wanna use modal window instead of flash)

For changing of passwords, I need to do the following steps: set up a setter method to change password, set up a settings/change password function that is decorated by fresh_login_required decorator, set the redirect view, setup a form and html for change password (done)

Add more help to travelling around the webpage (done)
Need to tidy up the code
Add a function to the tables to be able to sort through them
<!-- set up unit tests -->

Create errors for when they don't input sufficient values
Set fixed size for column widths (a continuous input fks this up, ok i really can't solve this)
Provide zoom box for table deets (similar to the idea in column widths)
Either write some CSS, or hook in some bootstrap to beautiful the code a bit (weekend)
Honestly this should be something you should be doing on your todolist you know

<!-- NOTES -->
<!-- enctype = "multipart/form-data" to encode file type data in a form, standard format won't be able to send file data -->
<!-- flaskform is a package used to understand data in html request forms sent, without hardcoding, with methods such as is_submitted() and validate_on_submit() -->
<!-- flaskwtf also include recaptcha support -->