from django.db import models

class Contractor(models.Model):
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=200)
    password = models.CharField(max_length=50, default='default_password', null=False) 
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Labour(models.Model):
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100) 
    skillset = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=200)
    password = models.CharField(max_length=50, default='default_password', null=False) 
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Job(models.Model):
    pname = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    description = models.TextField()
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    wage = models.CharField(max_length=10)
    startdate = models.DateField(auto_now_add=True)
    enddate = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=100) 
    skillset = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pname} - {self.contractor}"

class Company(models.Model):
    SERVICES_CHOICES = [
        ("Project Management", "Project Management"),
        ("Building Construction", "Building Construction"),
        ("Renovation and Remodeling", "Renovation and Remodeling"),
        ("Demolition", "Demolition"),
        ("Site Preparation", "Site Preparation"),
        ("Electrical Work", "Electrical Work"),
        ("Plumbing", "Plumbing"),
        ("HVAC", "HVAC"),
        ("Roofing", "Roofing"),
        ("Flooring", "Flooring"),
        ("Painting and Decorating", "Painting and Decorating"),
        ("Carpentry", "Carpentry"),
        ("Masonry", "Masonry"),
        ("Landscaping", "Landscaping"),
        ("Insulation", "Insulation"),
        ("General Repairs", "General Repairs"),
        ("Property Maintenance", "Property Maintenance"),
        ("Pest Control", "Pest Control"),
        ("Cleaning Services", "Cleaning Services"),
        ("Handyman Services", "Handyman Services"),
        ("Architectural Design", "Architectural Design"),
        ("Engineering Services", "Engineering Services"),
        ("Interior Design", "Interior Design"),
        ("Environmental Consulting", "Environmental Consulting"),
        ("Safety Consulting", "Safety Consulting"),
        ("Green Building", "Green Building"),
        ("Historical Restoration", "Historical Restoration"),
        ("Waterproofing", "Waterproofing"),
        ("Fireproofing", "Fireproofing"),
        ("Security Systems", "Security Systems"),
        ("Emergency Repairs", "Emergency Repairs"),
        ("Disaster Recovery", "Disaster Recovery"),
        ("Permitting and Inspections", "Permitting and Inspections"),
        ("Material Procurement", "Material Procurement"),
        ("Logistics and Transportation", "Logistics and Transportation"),
    ]
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    address = models.TextField()
    services = models.CharField(max_length=255, choices=SERVICES_CHOICES)
    years_experience = models.PositiveIntegerField()

    def __str__(self):
        return self.company_name
