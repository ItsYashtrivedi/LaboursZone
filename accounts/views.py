from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import Labour, Contractor,Job,Company
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q






# Create your views here.
# --------------------Register Page  View----------------------
def register_home(request):
    return render(request, 'register/register_home.html')


#  -------------------Register Labour Form-------------------------
def register_labour(request):
    if request.method == 'POST':
        lab_fname = request.POST['lab_fname']
        lab_mname = request.POST['lab_mname']
        lab_lname = request.POST['lab_lname']
        gender = request.POST['gender']
        occupation = request.POST['occupation']
        skillset = ','.join(request.POST.getlist('skillset'))  # Convert the list to a comma-separated string
        lab_phone_no = request.POST['lab_phone_no']
        address = request.POST['address']
        password = request.POST['password']
        location = request.POST['location']

        # Check if the phone number already exists
        if Labour.objects.filter(phone=lab_phone_no).exists():
            error_message = "Phone number already taken"
            print("User with this phone number already exists")
            return render(request, 'register/register_labour.html', {'error_message': error_message})
        else:
            # Create the new labourer
            new_labour = Labour.objects.create(
                fname=lab_fname,
                mname=lab_mname,
                lname=lab_lname,
                phone=lab_phone_no,
                gender=gender,
                address=address,
                password=password,
                location=location,
                skillset=skillset,
                occupation=occupation,
            )
            print("User created")

            # Set the session variables to log in the user
            request.session['labour_id'] = new_labour.id
            request.session['is_logged_in'] = True

            # Redirect to the labour_home page
            return redirect("labour_home")

    return render(request, 'register/register_labour.html')





#  -------------------Register contractor Functionality------------
# def register_contractor(request):
def register_contractor(request):
    if request.method == "POST":
        # Get the user information from POST
        con_fname= request.POST['con_fname']
        con_mname = request.POST['con_mname']
        con_lname = request.POST['con_lname']
        con_email = request.POST['con_email']
        con_phone_no = request.POST['con_phone_no']
        address = request.POST['address']
        password = request.POST['password']
        location = request.POST['location']
        
        if Contractor.objects.filter(phone=con_phone_no).exists():
                print("User with this email already exist")
                error_message = "Phone number already taken"
                return render(request, 'register/register_contractor.html', {'error_message':error_message})
        elif Contractor.objects.filter(email=con_email).exists():
                error_message = "Email-Id already taken"
                return render(request, 'register/register_contractor.html', {'error_message':error_message})
        else:
           contractor =   Contractor.objects.create(
            fname=con_fname,
            mname=con_mname,
            lname=con_lname,
            email=con_email,
            phone=con_phone_no,
            address=address,
            password=password,
            location=location
        )
        request.session['is_logged_in'] = True
        request.session['contractor_id'] = contractor.id  # Store contractor ID if needed
            
        print("User created")
        # success_message = "Registered Successfully"
        return redirect("contractor_home")
    
    return render(request, 'register/register_contractor.html')


def login_home(request):
    return render(request, 'register/login_home.html')

def login_contractor(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password'] 
        
        try:
            contractor = Contractor.objects.get(phone=phone, password=password)
            print(contractor)
        except Contractor.DoesNotExist:
            contractor = None
    
        if contractor is not None:
            # If the password matches, set session and redirect to home page
            request.session['contractor_id'] = contractor.id
            request.session['is_logged_in'] = True
            print(contractor.id)
            print("login")
            return redirect('contractor_home')
        else:
            # If the contractor doesn't exist or password doesn't match, show error message
            error_message = "Invalid Phone or password"
            return render(request, 'register/login_contractor.html', {'error_message': error_message})
               
    else:
        return render(request, 'register/login_contractor.html')

    
def login_labour(request):
    if request.method == 'POST':
        phone=request.POST['phone']
        password=request.POST['password'] 
        
        try:
            labour = Labour.objects.filter(phone=phone,password=password).first()
            print(labour)
            print(phone,password)
        except Labour.DoesNotExist:
            labour = None
    
        if labour is not None :
            # If the password matches, set session and redirect to home page
            request.session['labour_id'] = labour.id
            request.session['is_logged_in'] = True
            print("login")
            return redirect('labour_home')
        else:
            # If the contractor doesn't exist or password doesn't match, show error message
            error_message = "Invalid Phone or password"
            return render(request, 'register/login_labour.html', {'error_message':error_message})
               
    else:
         return render(request, 'register/login_labour.html')

 
def logout(request):
    if 'is_logged_in' in request.session:
        del request.session['is_logged_in']
    request.session.flush()
    return redirect( "index")




def contractor_home(request):
    is_logged_in = request.session.get('is_logged_in')
    print(is_logged_in)
    if is_logged_in is None:
        return redirect('index.html')
    return render(request, 'contractor_home.html')


def labour_home(request):
    # Check if laborer is logged in
    if 'labour_id' in request.session and request.session.get('is_logged_in'):
        labour_id = request.session['labour_id']
        
        # Retrieve the laborer object using the ID
        logged_in_labour = Labour.objects.get(id=labour_id)
        
        # Get the laborer's skills
        laborer_skills = logged_in_labour.skillset.split(',') if logged_in_labour.skillset else []
        
        # Query all jobs
        all_jobs = Job.objects.all()
        
        # Filter relevant jobs that match laborer's skills
        relevant_jobs = []
        for job in all_jobs:
            job_skills = job.skillset.split(',') if job.skillset else []
            if any(skill.strip() in laborer_skills for skill in job_skills):
                relevant_jobs.append(job)
        
        # Pass the relevant job posts to the template for rendering
        return render(request, 'register/labour_home.html', {'relevant_jobs': relevant_jobs})
    else:
        # If not logged in, redirect to the login page
        return redirect('login_labour')




def postjob(request):
    if request.method == 'POST':
        try:
            # Retrieve form data
            project_name = request.POST.get('project_name')
            project_location = request.POST.get('project_location')
            wage = int(request.POST.get('wage'))
            startdate_str = request.POST.get('startdate')
            enddate_str = request.POST.get('enddate')
            skillset =request.POST.getlist('skillset') 
            occupation = request.POST.get('occupation')
            description = request.POST.get('desc')

            # Parse date strings to datetime objects
            startdate = datetime.strptime(startdate_str, '%m/%d/%Y').strftime('%Y-%m-%d')
            enddate = datetime.strptime(enddate_str, '%m/%d/%Y').strftime('%Y-%m-%d') if enddate_str else None
            
            # Check if contractor is logged in
            contractor_id = request.session.get('contractor_id')
            if contractor_id is None:
                return redirect('login_contractor')  # Redirect to login page if contractor is not logged in
            
            # Get the contractor object
            contractor = Contractor.objects.get(id=contractor_id)

            # Create a new job object
            Job.objects.create(
                pname=project_name,
                location=project_location,
                wage=wage,
                description=description,
                startdate=startdate,
                enddate=enddate,
                occupation=occupation,
                contractor=contractor,
                skillset=skillset  # Assign the comma-separated skillset directly
            )

            # Redirect to contractor home page after successful job creation
            return redirect('contractor_home')  # Assuming you have a valid URL named 'contractor_records'

        except Contractor.DoesNotExist:
            # Handle the case where the contractor does not exist
            return HttpResponse("Contractor does not exist.")
        except Exception as e:
            # Handle any other exceptions and print the error for debugging
            print("An error occurred:", e)
            return HttpResponse("An error occurred while posting the job.")
    else:
        # If request method is not POST, render the postjob.html template
        return render(request, 'postjob.html')

def contractor_records(request):
    if request.session.get('is_logged_in'):
        try:
            contractor_id = request.session.get('contractor_id')
            logged_in_contractor = Contractor.objects.get(id=contractor_id)
            job_posts = Job.objects.filter(contractor=logged_in_contractor)

            # Preprocess skillset in each job post to split the string into a list
            for job_post in job_posts:
                job_post.skillset_list = job_post.skillset.split(',')

            return render(request, 'register/contractor_records.html', {'job_posts': job_posts})
        except ObjectDoesNotExist:
            return HttpResponse("Contractor does not exist.")
    else:
        return redirect('login_contractor')






def labour_profile(request):
     # Check if labour_id exists in session and if the user is logged in
    if 'labour_id' in request.session and request.session.get('is_logged_in'):
        labour_id = request.session['labour_id']
        # Retrieve the labour object using the ID
        logged_in_labour = Labour.objects.get(id=labour_id)
        return render(request, 'register/labour_profile.html', {'logged_in_labour': logged_in_labour})
    else:
        # If not logged in, redirect to the login page
        return redirect('login_labour')


def labour_records(request):

    return render(request,'register/labour_records.html')

# # @login_required
# def postjob(request):
#     if request.method == 'POST':
#         project_name = request.POST['project_name']
#         project_location = request.POST['project_location']
#         wage = int(request.POST['wage'])
#         startdate_str = request.POST.get('startdate')
#         enddate_str = request.POST.get('enddate')
#         skillset =request.POST.getlist('skillset') 
#         description = request.POST['desc']
#         # print(request.user)
#         startdate = datetime.strptime(startdate_str, '%m/%d/%Y').strftime('%Y-%m-%d')
#         enddate = datetime.strptime(enddate_str, '%m/%d/%Y').strftime('%Y-%m-%d') if enddate_str else None
        
#         contractor_id = request.session.get('contractor_id')
#         print(contractor_id)
        
#         # Check if contractor is logged in
#         if contractor_id is None:
#             return redirect('login_contractor')  # Redirect to login page if contractor is not logged in
        
#         # Get the contractor object
#         contractor = Contractor.objects.get(id=contractor_id)
#         print(contractor)

#         new_job=Job.objects.create(
#                pname=project_name,
#                location=project_location,
#                wage=wage,
#                description=description,
#                startdate=startdate,
#                enddate=enddate,
#                contractor=contractor,
#            )
        
#         for skill_name in skillset:
#             skill, _ = Skill.objects.get_or_create(name=skill_name)
#             new_job.skillset.add(skill)
#         return redirect('contractor_home')
#     else:
#         return render(request,'postjob.html')
    

def  update_labour(request,id):
 lab=Labour.objects.get(pk=id)
 return redirect('update_labour',{'lab':lab})



def do_update_labour(request,id):
    lab_fname = request.POST['lab_fname']
    lab_mname = request.POST['lab_mname']
    lab_lname = request.POST['lab_lname']
    gender = request.POST['gender']
    occupation = request.POST['occupation']
    skillset =request.POST.getlist('skillset') 
    lab_phone_no = request.POST['lab_phone_no']
    address = request.POST['address']
    password = request.POST['password']
    location = request.POST['location']


    Labour.objects.get(pk=id)

    Labour.objects.create(
               fname=lab_fname,
                mname=lab_mname,
                lname=lab_lname,
                phone=lab_phone_no,
                gender=gender,
                address=address,
                password=password,
                location=location,
                skillset=skillset,
                occupation=occupation,

           )
    return redirect(labour_home)


def company_details(request):
    

    return render(request,"register/company_details.html") 

def company_form(request):
    if request.method =='POST':
       company_name = request.POST.get('company_name')
       owner_name = request.POST.get('owner_name')
       contact_number = request.POST.get('contact_number')
       email = request.POST.get('email')
       city = request.POST.get('city')
       state = request.POST.get('state')
       postal_code = request.POST.get('postal_code')
       address = request.POST.get('address')
       services = request.POST.getlist('services')  # Use getlist for multiple selections
       years_experience = request.POST.get('years_experience')
       
       contractor_id = request.session.get('contractor_id')
       if contractor_id is None:
                return redirect('login_contractor')  # Redirect to login page if contractor is not logged in

       contractor = Contractor.objects.get(id=contractor_id)


       Company.objects.create(
            contractor=contractor,
            company_name=company_name,
            owner_name=owner_name,
            contact_number=contact_number,
            email=email,
            city=city,
            state=state,
            postal_code=postal_code,
            address=address,
            services=', '.join(services),
            years_experience=years_experience
        )
    #    print(request.POST)
       return redirect("company_details")

    return render(request,"register/company_form.html") 