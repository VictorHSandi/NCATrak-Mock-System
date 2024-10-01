from faker import Faker
from faker_education import SchoolProvider
import random
from datetime import datetime
from rich import print

# Configurable
# Note: CAC_TO_GENERATE * CAC_TO_AGENCY_RATIO < 32767
#TODO: Write a check for this
CAC_TO_GENERATE = 5
CAC_TO_AGENCY_RATIO = 5         # Agency per CAC

# This is the age that I cutoff for prior_convictions, 
# convicted_against_children, sexual_offender and sexual_predator
PERSON_AGE_CUTOFF = 15


# Data Tables
cac_data = []
agency_data = []
person_data = []
case_person_data = []

# Custom Fields
religions = ["Christianity", "Islam", "Hinduism", "Buddhism", "Other"]

races = [
    "White",
    "Black or African American",
    "Asian",
    "Hispanic or Latino",
    "Native American",
    "Pacific Islander",
    "Middle Eastern",
    "Mixed Race",
    "Other",
]

state_abbreviations = [
"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
"HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
"NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
"SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# CAC_AGENCY
def generate_cac_agency():
    data = []
    fake = Faker()
    fake.seed_instance(0)
    for cac in cac_data:
        for _ in range(CAC_TO_AGENCY_RATIO):
            agency = {}
            # Data to be generated
            agency["agency_id"] = fake.unique.random_number(digits=8)
            agency["cac_id"] = cac["cac_id"]
            city = fake.unique.city()                     
            agency["agency_name"] = city + " Agenecy"
            agency["addr_line_1"] = fake.street_address()
            agency["addr_line_2"] = None
            agency["city"] = city
            agency["state_abbr"] = random.choice(state_abbreviations)
            agency["phone_number"] = fake.unique.numerify("(###)###-####")
            agency["zip_code"] = fake.postalcode()
            agency_data.append(agency)

# child_advocacy_center
def generate_child_advocacy_center():
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(CAC_TO_GENERATE):
        cac = {}
        # Data to be generated
        cac["cac_id"] = fake.unique.random_int(min = 1, max = CAC_TO_GENERATE + CAC_TO_GENERATE)
        city = fake.unique.city()
        cac["agency_name"] = city + " Child Advocacy Center"
        cac["addr_line_1"] = fake.street_address()
        cac["addr_line_2"] = None
        cac["city"] = city
        cac["state_abbr"] = random.choice(state_abbreviations)
        cac["phone_number"] = fake.unique.numerify("(###)###-####")
        cac["zip_code"] = fake.postalcode()
        cac_data.append(cac)

# TODO: Fix Nones
def generate_person(amount: int):
    fake = Faker()
    fake.seed_instance(0)
    for _ in range(amount):
        person = {}
        
        person["cac_id"] = random.choice(cac_data)["cac_id"]        # Choose a random cac
        person["person_id"] = fake.unique.random_number(digits=10)
        # Generates a male or female randomly.
        x = 0 if fake.random_int(min=0, max=1) == 0 else 1
        person["first_name"] = fake.first_name_male() if x == 0 else fake.first_name_female()
        person["middle_initial"] = fake.first_name_male()[0]  # Middle Initial
        person["last_name"] = fake.last_name_male() if x == 0 else fake.last_name_female()
        person["suffix"] = None
        person["birthdate"] = fake.date_of_birth(minimum_age=3, maximum_age=100).strftime('%d-%m-%Y')
        #TODO: Put this in a utility file
        birthdate = datetime.strptime(person["birthdate"], '%d-%m-%Y')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        person["gender"] = "M" if x == 0 else "F"
        person["language"] = fake.language_name()
        person["race"] = random.choice(races)
        person["religion"] = random.choice(religions)
        person["prior_convictions"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["convicted_against_children"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["sexual_offender"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person["sexual_predator"] = False if (age <= PERSON_AGE_CUTOFF) else fake.boolean(chance_of_getting_true = 10)
        person_data.append(person)

#TODO: Figure out how this exactly works, is there multiple of these types of cases per person.
def generator_case_person(amount: int):
    fake = Faker()
    fake.add_provider(SchoolProvider)
    fake.seed_instance(0)
    for _ in range(amount):
        person  = random.choice(person_data)   
        case = {}
             
        case["person_id"] = person["person_id"]
        case["case_id"] = fake.unique.random_number(digits = 9)
        case["cac_id"] = person["cac_id"]
        birthdate = datetime.strptime(person["birthdate"], '%d-%m-%Y')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        # TODO: Check if it is Months / Days
        case["age"] = age
        case["age_unit"] = "year"
        case["addr_line_1"] = fake.street_address()
        case["addr_line_2"] = None
        city = fake.unique.city()
        case["city"] = city
        case["state_abbr"] = random.choice(state_abbreviations)
        case["zip_code"] = fake.postalcode()
        case["phone_number"] = fake.unique.numerify("(###)###-####")
        #TODO: Set Chances / NULL
        case["phone_number"] = fake.unique.numerify("(###)###-####")
        case["phone_number"] = fake.unique.numerify("(###)###-####")
        school_data = fake.school_object()
        case["school_or_employer"] = school_data["school"] if age < 18 else fake.job()
        case["custody"] = fake.boolean()
        #TODO: Get Clarification on these
        case["education_level"] = school_data["level"] if age < 18 else random.choice(["GED", "No_GED", "Associates", "Bachelors", "Masters", "Doctorate"])
        case["income_level"] = random.choice(["Low", "Medium", "High"])
        #TODO: AGE CHECK PLEASE ZANE
        case["martial_status"] = random.choice(["Single", "Married", "Divocred", "Widowed", "Seperated", "Anullued"])
        #TODO: Get Clarification
        case["relationship"] = "placeholder"
        case["case_role"] = random.choice(["Victim", "Family", "Aggressor"])
        case["same_household"] = fake.boolean()
        case["victim_status_id"] = fake.unique.random_number(digits = 8)
        case_person_data.append(case)
        
if __name__ == "__main__":
    print("[bold blue]NCA-Trak-Mock Data Generator")
    print("[yellow]How many data entries would you like to be generated?")
    n = int(input())
    print("[yellow]Generating Data...")
    # Call to make
    # TODO: Clean up calls, idk how yet...
    generate_child_advocacy_center()
    generate_cac_agency()
    generate_person(amount = n)
    generator_case_person(amount= n * n)

    
    # Print Testing
    #print(cac_data)
    #print(agency_data)
    print(person_data)
    print(case_person_data)