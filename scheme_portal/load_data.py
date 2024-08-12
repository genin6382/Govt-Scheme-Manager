import json,os,django

#setting up django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheme_portal.settings')
django.setup()


from scheme_manager.models import Scheme

# Function to convert "Yes" and "No" to boolean
def yes_no_to_boolean(value):
    return value.lower() == 'yes'

#loading data from json file
with open(r'D:\backend\Django-startup\Government-scheme\scheme_portal\myschemes.json') as f:
    schemes=json.load(f)


#inserting data into database using bulk_create

scheme_objects = [
    Scheme(
        scheme_name=scheme['scheme_name'],
        scheme_link=scheme['scheme_link'],
        tags=scheme['tags'],
        details=scheme['details'],
        benefits=scheme['benefits'],
        eligibility_criteria=scheme['eligibility_criteria'],
        application_process=scheme['application_process'],
        documents_required=scheme['documents_required'],
        scheme_short_title=scheme['schemeShortTitle'],
        scheme_category=scheme['schemeCategory'],
        scheme_sub_category=scheme['schemeSubCategory'],
        gender=scheme['gender'],
        minority=yes_no_to_boolean(scheme['minority']),
        beneficiary_state=scheme['beneficiaryState'],
        residence=scheme['residence'],
        caste=scheme['caste'],
        disability=yes_no_to_boolean(scheme['disability']),
        occupation=scheme['occupation'],
        marital_status=scheme['maritalStatus'],
        education=scheme['education'],
        age=scheme['age'],
        is_bpl=yes_no_to_boolean(scheme['isBpl']),
        is_student=yes_no_to_boolean(scheme['isStudent']),
        original_eligibility=scheme['original_eligibility'],
        summary=scheme['summary'],
    )
    for scheme in schemes
]

Scheme.objects.bulk_create(scheme_objects)
print("Data Inserted Successfully")

