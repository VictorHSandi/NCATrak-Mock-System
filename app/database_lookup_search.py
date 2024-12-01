import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkcalendar import DateEntry
import Generaltab_interface
import MH_basic_interface
import people_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import case_notes
from database.config import load_config
from database.connect import connect

heading_font = ("Helvetica", 18, "bold")
bold_label_font = ("Helvetica", 12, "bold")
normal_text_font = ("Helvetica", 12)
entry_width = 30

padx = 10
pady = 5

religions = [
    "Christianity",
    "Islam",
    "Judaism",
    "Hinduism",
    "Buddhism",
    "Sikhism",
    "Jainism",
    "Atheist/Agnostic",
    "Other"
]

languages = [
    "English",
    "Spanish",
    "French",
    "German",
    "Portuguese",
    "Russian",
    "Arabic",
    "Turkish",
    "Hindi",
    "Urdu",
    "Chinese",
    "Japanese",
    "Vietnamese",
    "Korean",
    "Other"
]

races = [
    "Asian",
    "American Indian",
    "Biracial",
    "Biracial - African-American/White",
    "Biracial - Hispanic/White",
    "Black/African-American",
    "White",
    "Hispanic",
    "Native Hawaiian/Other Pacific Islander",
    "Alaska Native",
    "Multiple Races",
    "Not Reported",
    "Not Tracked",
    "Other"
]

case_roles = [
    "Alleged Victim/Client",
    "Alleged Co-Victim",
    "Alleged Offender",
    "Caregiver",
    "Other"
]

relationships_to_victim = [
    "Self",
    "Mother",
    "Biological Mother",
    "Adoptive Mother",
    "Step-Mother",
    "Father's Girlfriend",
    "Father",
    "Biological Father",
    "Adoptive Father",
    "Step-Father",
    "Mother's Boyfriend",
    "Brother",
    "Sister",
    "Step-Brother",
    "Step-Sister",
    "Adoptive Brother",
    "Adoptive Sister",
    "Grandmother",
    "Grandfather",
    "Friend",
    "Other Known Person"
]

victim_statuses = [
    "Primary",
    "Secondary",
    "N/A"
]

age_units = [
    "Years",
    "Months"
]

states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "District of Columbia",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina"
    "South Dakota"
    "Tennessee",
    "Texas"
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
    "Other"
]

education_levels = [
    "None",
    "Preschool",
    "Elementary School",
    "Middle School",
    "High School",
    "High School Graduate - GED",
    "Some College",
    "Associate's Degree",
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "Unknown"
]

marital_statuses = [
    "Single",
    "Married",
    "Divorced",
    "Widowed",
    "Unknown"
]

income_levels = [
    "less than $15,000",
    "between $15,000 and $25,000",
    "between $25,000 and $50,000",
    "between $50,000 and $75,000",
    "greater than $75,000"
]

class lookup_interface(tk.Frame):
    
    def __init__(self, parent, controller):
        
        self.controller = controller

        tk.Frame.__init__(self, parent)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame = scrollable_frame
        
        # label = ttk.Label(self, text="back to main page", font = ("Verdana", 35))
        # label.grid(row = 0, column=0, padx = 5, pady = 5)

        # Navigation Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky='w')

        # Create a list of tuples with button text and corresponding function placeholders
        nav_buttons = [
            ("Lookup", self.show_lookup_page),
            ("General", self.show_general_tab),
            ("People", self.show_people_tab),
            ("Mental Health - Basic", self.show_mh_basic),
            ("Mental Health - Assessment", self.show_mh_assessment),
            ("Mental Health - Treatment Plan", self.show_mh_treatment_plan),
            ("Mental Health - Case Notes", self.show_case_notes),
            ("VA", self.show_va_tab),
        ]

        for btn_text, btn_command in nav_buttons:
            button = ttk.Button(button_frame, text=btn_text, command=btn_command)
            button.pack(side='left', padx=5)
        
        # Reload button - fully reloads the application
        refresh_button = ttk.Button(button_frame, text="Reload", command=controller.refresh)
        refresh_button.pack(side='right', padx=5)

        # Create a window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Link scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.patient_data = self.load_first_100_patients()
        self.filtered_patients = self.patient_data  # Initialize filtered_patients

        # creates frame for search and patient list
        search_frame = tk.Frame(scrollable_frame)
        search_frame.grid(row=1, column=0, padx=20, pady=20)

        # create search entry
        tk.Label(search_frame, text="Search Patient:", font=bold_label_font).grid(row=1, column=0, padx=padx, pady=pady)
        self.search_entry = tk.Entry(search_frame, font=normal_text_font, width=entry_width)
        self.search_entry.grid(row=1, column=1, padx=padx, pady=pady)
        self.search_entry.bind("<KeyRelease>", self.search_patients)

        # creates a listbox to display search results
        self.patient_list = tk.Listbox(search_frame, width=entry_width * 2, height=10, font=normal_text_font)
        self.patient_list.grid(row=2, column=0, columnspan=2, padx=padx, pady=pady)

        # creates frame for patient details
        self.details_frame = tk.Frame(scrollable_frame)
        self.details_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20)
        canvas = tk.Canvas(self.details_frame)
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(self.details_frame)

        # button for creating new case
        new_case_button = ttk.Button(self.scrollable_frame, text="Create New Case", command=self.create_new_case_popup)
        new_case_button.grid(row=1, column=9, sticky='ne', pady=20)

    def get_religion(self, id):
        if id is not None and id >= 0:
            return religions[id]
        else:
            return ""
        
    def get_race(self, id):
        if id is not None and id >= 0:
            return races[id]
        else:
            return ""
        
    def get_language(self, id):
        if id is not None and id >= 0:
            return languages[id]
        else:
            return ""

    def get_relationship(self, id):
        if id is not None:
            return relationships_to_victim[id]
        else:
            return "Not Listed"

    def get_role(self, id):
        if id is not None:
            return case_roles[id]
        else:
            return "Not Listed"
        
    def get_id_of_race(self, race):
        for i in range((len(races) - 1)):
            if races[i] == race:
                return i
            else:
                return -1
            
    def get_id_of_religion(self, religion):
        for i in range((len(religions) - 1)):
            if religions[i] == religion:
                return i
            else:
                return -1
            
    def get_id_of_languages(self, language):
        for i in range((len(languages) - 1)):
            if languages[i] == language:
                return i
            else:
                return -1

    def load_first_100_patients(self):

        patient_data = []
        config = load_config(filename="database.ini")
        conn = connect(config)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM person ORDER BY last_name FETCH FIRST 100 ROWS ONLY") 
            row = cur.fetchone()
                    
            while row is not None:
                patient_data.append(row)
                row = cur.fetchone()

            return patient_data
        
    # to populate the details of the selected patient
    def show_patient_details(self, patient):
        # Clear previous patient details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        tk.Label(self.details_frame, text="First Name:", font=bold_label_font).grid(column=0, row=0, sticky="e", padx=padx, pady=pady)
        first_name_entry = tk.Entry(self.details_frame, font=normal_text_font)
        first_name_entry.insert(0,patient[2])
        first_name_entry.grid(column=1, row=0, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Last Name:", font=bold_label_font).grid(column=0, row=1, sticky="e", padx=padx, pady=pady)
        last_name_entry = tk.Entry(self.details_frame, font=normal_text_font)
        last_name_entry.insert(0, patient[4])
        last_name_entry.grid(column=1, row=1, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Middle Name:", font=bold_label_font).grid(column=0, row=2, sticky="e", padx=padx, pady=pady)
        middle_name_entry = tk.Entry(self.details_frame, font=normal_text_font)
        middle_name_entry.insert(0, patient[3])
        middle_name_entry.grid(column=1, row=2, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Date of Birth:", font=bold_label_font).grid(column=0, row=4, sticky="e", padx=padx, pady=pady)
        birthdate_entry = DateEntry(self.details_frame, font=normal_text_font)
        birthdate_entry.set_date(patient[6])
        birthdate_entry.grid(column=1, row=4, sticky="w", padx=padx, pady=pady)

        race_var = tk.StringVar()
        race_var.set(self.get_race(patient[9]))
        tk.Label(self.details_frame, text="Race:", font=bold_label_font).grid(column=0, row=5, sticky="e", padx=padx, pady=pady)
        race_dropdown = ttk.Combobox(self.details_frame, values=races, font=normal_text_font, textvariable=race_var)
        race_dropdown.grid(column=1, row=5, sticky="w", padx=padx, pady=pady)

        # genders = ["Male", "Female", "Transgender Male", "Transgender Female", "Non-Binary", "Other"]
        genders = ["M", "F"]
        gender_frame = tk.Frame(self.details_frame)
        gender_frame.grid(row=6, column=1, padx=padx, pady=pady, sticky='w')
        patient_gender = tk.StringVar()
        patient_gender.set(patient[7])
        tk.Label(self.details_frame, text="Gender:", font=bold_label_font).grid(column=0, row=6, sticky="e", padx=padx, pady=pady)
        column_counter = 1
        for gender in genders:
            button = ttk.Radiobutton(gender_frame, text=gender, variable=patient_gender, value=gender)
            button.grid(row=0, column=column_counter)
            column_counter += 1
        style = ttk.Style()
        style.configure("TRadiobutton", font=('Helvetica', 12))

        religion_var = tk.StringVar()
        religion_var.set(self.get_religion(patient[10]))
        tk.Label(self.details_frame, text="Religion:", font=bold_label_font).grid(column=0, row=7, sticky="e", padx=padx, pady=pady)
        religion_dropdown = ttk.Combobox(self.details_frame, values=religions, font=normal_text_font, textvariable=religion_var)
        religion_dropdown.grid(column=1, row=7, sticky="w", padx=padx, pady=pady)

        language_var = tk.StringVar()
        language_var.set(self.get_language(patient[8]))
        tk.Label(self.details_frame, text="Language:", font=bold_label_font).grid(column=0, row=8, sticky="e", padx=padx, pady=pady)
        language_dropdown = ttk.Combobox(self.details_frame, values=languages, font=normal_text_font, textvariable=language_var)
        language_dropdown.grid(column=1, row=8, sticky="w", padx=padx, pady=pady)

        prior_convictions_var = tk.BooleanVar()
        prior_convictions_var.set(patient[11])
        tk.Label(self.details_frame, text="Prior Convictions:", font=bold_label_font).grid(column=2, row=0, sticky="e", padx=padx, pady=pady)
        prior_convictions_checkbox = ttk.Checkbutton(self.details_frame, variable=prior_convictions_var, onvalue=True, offvalue=False)
        prior_convictions_checkbox.grid(column=3, row=0, sticky="w", padx=padx, pady=pady)

        convicted_against_children_var = tk.BooleanVar()
        convicted_against_children_var.set(patient[12])
        tk.Label(self.details_frame, text="Convicted of Crimes Against Children:", font=bold_label_font).grid(column=2, row=1, sticky="e", padx=padx, pady=pady)
        convicted_against_children_checkbox = ttk.Checkbutton(self.details_frame, variable=convicted_against_children_var, onvalue=True, offvalue=False)
        convicted_against_children_checkbox.grid(column=3, row=1, sticky="w", padx=padx, pady=pady)

        sex_offender = tk.BooleanVar()
        sex_offender.set(patient[13])
        tk.Label(self.details_frame, text="Sexual Offender:", font=bold_label_font).grid(column=2, row=2, sticky="e", padx=padx, pady=pady)
        sex_offender_checkbox = ttk.Checkbutton(self.details_frame, variable=sex_offender, onvalue=True, offvalue=False)
        sex_offender_checkbox.grid(column=3, row=2, sticky="w", padx=padx, pady=pady)

        sex_predator = tk.BooleanVar()
        sex_predator.set(patient[14])
        tk.Label(self.details_frame, text="Sexual Predator:", font=bold_label_font).grid(column=2, row=3, sticky="e", padx=padx, pady=pady)
        sex_predator_checkbox = ttk.Checkbutton(self.details_frame, variable=sex_predator, onvalue=True, offvalue=False)
        sex_predator_checkbox.grid(column=3, row=3, sticky="w", padx=padx, pady=pady)

        # creates a listbox to display search results for cases
        tk.Label(self.details_frame, text="Case ID\t\tRelationship to Victim\t\tRole\t\tAge\t\tSame Household?\t\tCustody?", font=bold_label_font).grid(column=0, row=10, columnspan=7, sticky="e", padx=padx, pady=pady)
        cases_list = tk.Listbox(self.details_frame, width=entry_width * 4, height=10, font=normal_text_font)
        cases_list.grid(row=11, column=0, columnspan=5, padx=padx, pady=pady)

        def save_person():
            update_query = """
                UPDATE person SET 
                    first_name = %s, 
                    middle_name = %s, 
                    last_name = %s, 
                    date_of_birth = %s, 
                    language_id = %s, 
                    race_id = %s, 
                    religion_id = %s,
                    prior_convictions = %s,
                    convicted_against_children = %s,
                    sex_offender = %s,
                    sex_predator = %s
                WHERE person_id = %s;
            """

            try:
                config = load_config(filename="database.ini")
                conn = connect(config)
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE person SET 
                            first_name = %s, 
                            middle_name = %s, 
                            last_name = %s, 
                            date_of_birth = %s, 
                            language_id = %s, 
                            race_id = %s, 
                            religion_id = %s,
                            prior_convictions = %s,
                            convicted_against_children = %s,
                            sex_offender = %s,
                            sex_predator = %s
                        WHERE person_id = %s;
                        """, (
                        first_name_entry.get(),
                        middle_name_entry.get(),
                        last_name_entry.get(),
                        str(birthdate_entry.get_date()),
                        str(self.get_id_of_languages(language_var.get())),
                        str(self.get_id_of_race(race_var.get())),
                        str(self.get_id_of_religion(religion_var.get())),
                        str(prior_convictions_var.get()),
                        str(convicted_against_children_var.get()),
                        str(sex_offender.get()),
                        str(sex_predator.get()),
                        str(patient[1]))
                    )
                    conn.commit()
                    messagebox.showinfo("Success", "Updated record successfully")
            except Exception as e:
                messagebox.showinfo("Error", f"Failed to update person: {e}")

        # button for saving edits to personal profile
        save_button = ttk.Button(self.scrollable_frame, text="Save", command=save_person)
        save_button.grid(row=1, column=8, sticky='ne', pady=25)

        # to search cases based on specific person
        def search_cases_by_patient(person_id, event=None):
            global filtered_cases
            config = load_config(filename="database.ini")
            conn = connect(config)

            search_query = self.search_entry.get().lower()
            filtered_cases = []

            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM case_person WHERE person_id={person_id} FETCH FIRST 100 ROWS ONLY".format(search_query))
                row = cur.fetchone()

                while row is not None:
                    filtered_cases.append(row)
                    row = cur.fetchone()

            update_cases_list(filtered_cases)

        #update the patient list based on search 
        def update_cases_list(filtered_cases):
            cases_list.delete(0, tk.END)
            for case in filtered_cases:
                # this might be the most scuffed line of code i've ever written but for some reason tabs aren't working so this is the only way to get the spacing to behave     -zac
                cases_list.insert(tk.END, f"                {case[1]}                 {self.get_relationship(case[17])}                                                      {self.get_role(case[18])}                    {case[3]}                               {case[19]}                                             {case[13]}")
            cases_list.bind("<Double-1>", on_case_select_from_list)

        # callback function when a patient is selected from the list
        def on_case_select_from_list(event):
            selected_index = cases_list.curselection()
            if selected_index:
                case_index = selected_index
                case_id = filtered_cases[case_index[0]][1]
                case_id_file = open("case_id.txt", "w")
                case_id_file.write(str(case_id))
                messagebox.showinfo("Success", f"Selected case {case_id}")

        search_cases_by_patient(patient[1])

    def create_new_case_popup(self):
        new_case_popup = tk.Toplevel(self)
        new_case_popup.title("Create New Case")
        new_case_popup.geometry("1600x900")

        # Scrollable Frame Setup
        new_canvas = tk.Canvas(new_case_popup)
        new_scrollbar = ttk.Scrollbar(new_canvas, orient="vertical", command=new_canvas.yview)
        new_canvas.configure(yscrollcommand=new_scrollbar.set)
        new_scrollbar.pack(side="right", fill="y")

        new_canvas.pack(side="left", fill="both", expand=True)
        scrollable_frame = ttk.Frame(new_canvas)

        new_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: new_canvas.configure(
                scrollregion=new_canvas.bbox("all")
            )
        )

        # Personal Profile Information
        personal_profile_frame = tk.LabelFrame(scrollable_frame, text="Personal Profile", width=200)
        personal_profile_frame.grid(row=1, column=0, sticky='w')

        tk.Label(personal_profile_frame, text="First Name*", font=bold_label_font).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        first_name_entry = tk.Entry(personal_profile_frame, font=normal_text_font, width=50)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_profile_frame, text="Middle Name", font=bold_label_font).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        middle_name_entry = tk.Entry(personal_profile_frame, font=normal_text_font, width=50)
        middle_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_profile_frame, text="Last Name*", font=bold_label_font).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        last_name_entry = tk.Entry(personal_profile_frame, font=normal_text_font, width=50)
        last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_profile_frame, text="Suffix", font=bold_label_font).grid(row=3, column=0, padx=5, pady=5, sticky='e')
        suffix_entry = tk.Entry(personal_profile_frame, font=normal_text_font, width=8)
        suffix_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_profile_frame, text="Date of Birth", font=bold_label_font).grid(row=4, column=0, padx=5, pady=5, sticky='e')
        birthdate_entry = DateEntry(personal_profile_frame, font=normal_text_font)
        birthdate_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        genders = ["M", "F"]
        gender_frame = tk.Frame(personal_profile_frame)
        tk.Label(personal_profile_frame, text="Gender:", font=bold_label_font).grid(column=0, row=5, sticky="e", padx=padx, pady=pady)
        gender_frame.grid(row=5, column=1, padx=padx, pady=pady, sticky='w')
        gender_var = tk.StringVar()
        column_counter = 1
        for gender in genders:
            button = ttk.Radiobutton(gender_frame, text=gender, variable=gender_var, value=gender)
            button.grid(row=0, column=column_counter)
            column_counter += 1
        style = ttk.Style()
        style.configure("TRadiobutton", font=('Helvetica', 12))

        race_var = tk.StringVar()
        tk.Label(personal_profile_frame, text="Race:", font=bold_label_font).grid(column=0, row=6, sticky="e", padx=padx, pady=pady)
        race_dropdown = ttk.Combobox(personal_profile_frame, values=races, font=normal_text_font, textvariable=race_var)
        race_dropdown.grid(column=1, row=6, sticky="w", padx=padx, pady=pady)

        religion_var = tk.StringVar()
        tk.Label(personal_profile_frame, text="Religion:", font=bold_label_font).grid(column=0, row=7, sticky="e", padx=padx, pady=pady)
        religion_dropdown = ttk.Combobox(personal_profile_frame, values=religions, font=normal_text_font, textvariable=religion_var)
        religion_dropdown.grid(column=1, row=7, sticky="w", padx=padx, pady=pady)

        language_var = tk.StringVar()
        tk.Label(personal_profile_frame, text="Language:", font=bold_label_font).grid(column=0, row=8, sticky="e", padx=padx, pady=pady)
        language_dropdown = ttk.Combobox(personal_profile_frame, values=languages, font=normal_text_font, textvariable=language_var)
        language_dropdown.grid(column=1, row=8, sticky="w", padx=padx, pady=pady)

        prior_convictions_var = tk.BooleanVar()
        tk.Label(personal_profile_frame, text="Prior Convictions:", font=bold_label_font).grid(column=0, row=9, sticky="e", padx=padx, pady=pady)
        prior_convictions_checkbox = ttk.Checkbutton(personal_profile_frame, variable=prior_convictions_var, onvalue=True, offvalue=False)
        prior_convictions_checkbox.grid(column=1, row=9, sticky="w", padx=padx, pady=pady)

        convicted_against_children_var = tk.BooleanVar()
        tk.Label(personal_profile_frame, text="Convicted of Crimes Against Children:", font=bold_label_font).grid(column=0, row=10, sticky="e", padx=padx, pady=pady)
        convicted_against_children_checkbox = ttk.Checkbutton(personal_profile_frame, variable=convicted_against_children_var, onvalue=True, offvalue=False)
        convicted_against_children_checkbox.grid(column=1, row=10, sticky="w", padx=padx, pady=pady)

        sex_offender = tk.BooleanVar()
        tk.Label(personal_profile_frame, text="Sexual Offender:", font=bold_label_font).grid(column=0, row=11, sticky="e", padx=padx, pady=pady)
        sex_offender_checkbox = ttk.Checkbutton(personal_profile_frame, variable=sex_offender, onvalue=True, offvalue=False)
        sex_offender_checkbox.grid(column=1, row=11, sticky="w", padx=padx, pady=pady)

        sex_predator = tk.BooleanVar()
        tk.Label(personal_profile_frame, text="Sexual Predator:", font=bold_label_font).grid(column=0, row=12, sticky="e", padx=padx, pady=pady)
        sex_predator_checkbox = ttk.Checkbutton(personal_profile_frame, variable=sex_predator, onvalue=True, offvalue=False)
        sex_predator_checkbox.grid(column=1, row=12, sticky="w", padx=padx, pady=pady)


        # Case Information Section
        case_information_frame = tk.LabelFrame(scrollable_frame, text="Case Specific Information")
        case_information_frame.grid(row=2, column=0, sticky='w')

        vic_status_var = tk.StringVar()
        tk.Label(case_information_frame, text="Victim Status:", font=bold_label_font).grid(column=0, row=0, sticky="w", padx=padx, pady=pady)
        status_dropdown = ttk.Combobox(case_information_frame, values=victim_statuses, font=normal_text_font, textvariable=vic_status_var, width=50)
        status_dropdown.grid(column=1, row=0, sticky="w", padx=padx, pady=pady)

        age_frame = tk.Frame(case_information_frame)
        age_frame.grid(row=1, column=0, columnspan=8, sticky='w')

        tk.Label(age_frame, text="Age at Time of Referral*:", font=bold_label_font).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        age_entry = tk.Entry(age_frame, font=normal_text_font, width=8)
        age_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        age_unit_var = tk.StringVar()
        age_unit_var.set("Years")
        age_unit_dropdown = ttk.Combobox(age_frame, values=age_units, font=normal_text_font, textvariable=age_unit_var)
        age_unit_dropdown.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Address Line 1:", font=bold_label_font).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        addr_line_1_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        addr_line_1_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Address Line 2:", font=bold_label_font).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        addr_line_2_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        addr_line_2_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="City:", font=bold_label_font).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        city_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        city_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="State:", font=bold_label_font).grid(row=5, column=0, padx=5, pady=5, sticky='w')
        state_var = tk.StringVar()
        state_dropdown = ttk.Combobox(case_information_frame, font=normal_text_font, width=50, values=states, textvariable=state_var)
        state_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Zip Code:", font=bold_label_font).grid(row=6, column=0, padx=5, pady=5, sticky='w')
        city_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        city_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Home Phone:", font=bold_label_font).grid(row=7, column=0, padx=5, pady=5, sticky='w')
        home_phone_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        home_phone_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Work Phone:", font=bold_label_font).grid(row=8, column=0, padx=5, pady=5, sticky='w')
        work_phone_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        work_phone_entry.grid(row=8, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Cell Phone:", font=bold_label_font).grid(row=9, column=0, padx=5, pady=5, sticky='w')
        cell_phone_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        cell_phone_entry.grid(row=9, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="School or Employer:", font=bold_label_font).grid(row=10, column=0, padx=5, pady=5, sticky='w')
        employer_entry = tk.Entry(case_information_frame, font=normal_text_font, width=50)
        employer_entry.grid(row=10, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Education Level:", font=bold_label_font).grid(row=11, column=0, padx=5, pady=5, sticky='w')
        education_level_var = tk.StringVar()
        education_level_dropdown = ttk.Combobox(case_information_frame, values=education_levels, textvariable=education_level_var, font=normal_text_font, width=50)
        education_level_dropdown.grid(row=11, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Marital Status:", font=bold_label_font).grid(row=12, column=0, padx=5, pady=5, sticky='w')
        marital_status_var = tk.StringVar()
        marital_status_dropdown = ttk.Combobox(case_information_frame, values=marital_statuses, textvariable=marital_status_var, font=normal_text_font, width=50)
        marital_status_dropdown.grid(row=12, column=1, padx=5, pady=5, sticky='w')

        tk.Label(case_information_frame, text="Income Level of Household:", font=bold_label_font).grid(row=13, column=0, padx=5, pady=5, sticky='w')
        income_level_var = tk.StringVar()
        income_level_dropdown = ttk.Combobox(case_information_frame, values=income_levels, textvariable=income_level_var, font=normal_text_font, width=50)
        income_level_dropdown.grid(row=13, column=1, padx=5, pady=5, sticky='w')


        referral_information_frame = tk.LabelFrame(scrollable_frame, text="Referral Information")
        referral_information_frame.grid(row=3, column=0, sticky='w')

        tk.Label(referral_information_frame, text="Date Received by CAC*", font=bold_label_font).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        received_date_entry = DateEntry(referral_information_frame, font=normal_text_font)
        received_date_entry.grid(row=0, column=1, padx=5, pady=5)

        def cancel():
            new_case_popup.destroy()

        def save_and_open():
            pass

        def add_another_person():
            pass

        def lookup_person():

            search_person_popup = tk.Toplevel(self)
            search_person_popup.title("Search Person")
            search_person_popup.geometry("1100x700")

            search_bar_frame = tk.Frame(search_person_popup)
            search_bar_frame.grid(row=0, column=0, padx=20, pady=20)

            tk.Label(search_bar_frame, text="Last Name", font=bold_label_font).grid(row=0, column=0, padx=5, pady=5)
            search_bar = tk.Entry(search_bar_frame, width=40)
            search_bar.grid(row=0, column=1, padx=padx, pady=pady)

            search_button = tk.Button(search_bar_frame, text="Search", command=lambda:search_by_last_name(search_bar.get()))
            search_button.grid(row=0, column=2, padx=padx, pady=pady)

            no_match_button = tk.Button(search_bar_frame, text="No Match Found", command=search_person_popup.destroy)
            no_match_button.grid(row=0, column=3, padx=padx, pady=pady)

            close_button = tk.Button(search_bar_frame, text="Close", command=search_person_popup.destroy)
            close_button.grid(row=0, column=4, padx=padx, pady=pady)

            filtered_people = []

            results_header_frame = tk.Frame(search_person_popup)
            results_header_frame.grid(row=1, column=0, sticky='w')

            tk.Label(results_header_frame, text="Select", font=bold_label_font, width=10).grid(row=0, column=0, padx=5, pady=5, sticky='w')
            tk.Label(results_header_frame, text="View", font=bold_label_font, width=10).grid(row=0, column=1, padx=5, pady=5, sticky='w')
            tk.Label(results_header_frame, text="Last Name", font=bold_label_font, width=20).grid(row=0, column=2, padx=5, pady=5, sticky='w')
            tk.Label(results_header_frame, text="First Name", font=bold_label_font, width=20).grid(row=0, column=3, padx=5, pady=5, sticky='w')
            tk.Label(results_header_frame, text="Middle Name", font=bold_label_font, width=20).grid(row=0, column=4, padx=5, pady=5, sticky='w')

            results_frame = tk.Frame(search_person_popup)
            results_frame.grid(row=2, column=0)

            def search_by_last_name(lname):
                try:
                    config = load_config(filename="database.ini")
                    conn = connect(config)
                    with conn.cursor() as cur:
                        cur.execute("SELECT * FROM person WHERE last_name~*\'{0}\' ORDER BY last_name FETCH FIRST 100 ROWS ONLY".format(lname))
                        row = cur.fetchone()
                        while row is not None:
                            filtered_people.append(row)
                            row = cur.fetchone()
                        show_people_by_last_name()
                except Exception as e:
                    messagebox.showinfo("Error", f"Error executing search: {e}")

            def show_people_by_last_name():
                results_frame = tk.Frame(search_person_popup)
                results_frame.grid(row=2, column=0, sticky='w')
                for i in range(len(filtered_people)):
                    tk.Button(results_frame, text="Select", command=lambda:select_person(filtered_people[i]), width=10).grid(row=i, column=0, padx=10, pady=5, sticky='w')
                    tk.Button(results_frame, text="View", command=lambda:view_person(filtered_people[i]), width=10).grid(row=i, column=1, padx=10, sticky='w')
                    tk.Label(results_frame, text=filtered_people[i][4], font=normal_text_font, width=20).grid(row=i, column=2, padx=5, pady=5, sticky='w')
                    tk.Label(results_frame, text=filtered_people[i][2], font=normal_text_font, width=20).grid(row=i, column=3, padx=5, pady=5, sticky='w')
                    tk.Label(results_frame, text=filtered_people[i][3], font=normal_text_font, width=20).grid(row=i, column=4, padx=5, pady=5, sticky='w')

            def view_person(patient):

                view_person_popup = tk.Toplevel(self)
                view_person_popup.title("View Person")
                view_person_popup.geometry("1100x700")

                profile_frame = tk.Frame(view_person_popup)
                profile_frame.grid(row=0, column=0)

                tk.Label(profile_frame, text="First Name:", font=bold_label_font).grid(column=0, row=0, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=patient[2]).grid(column=1, row=0, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Last Name:", font=bold_label_font).grid(column=0, row=1, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=patient[4]).grid(column=1, row=1, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Middle Name:", font=bold_label_font).grid(column=0, row=2, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=patient[3]).grid(column=1, row=2, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Date of Birth:", font=bold_label_font).grid(column=0, row=4, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=patient[6]).grid(column=1, row=4, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Race:", font=bold_label_font).grid(column=0, row=5, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=self.get_race(patient[9])).grid(column=1, row=5, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Gender:", font=bold_label_font).grid(column=0, row=6, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, text="Male" if patient[7] == 'M' else "Female", font=normal_text_font).grid(column=1, row=6, sticky='w', padx=padx, pady=pady)

                tk.Label(profile_frame, text="Religion:", font=bold_label_font).grid(column=0, row=7, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=self.get_religion(patient[10])).grid(column=1, row=7, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Language:", font=bold_label_font).grid(column=0, row=8, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, font=normal_text_font, text=self.get_language(patient[8])).grid(column=1, row=8, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Prior Convictions:", font=bold_label_font).grid(column=2, row=0, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, text="Yes" if patient[11] else "No", font=normal_text_font).grid(column=3, row=0, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Convicted of Crimes Against Children:", font=bold_label_font).grid(column=2, row=1, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, text="Yes" if patient[12] else "No", font=normal_text_font).grid(column=3, row=1, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Sexual Offender:", font=bold_label_font).grid(column=2, row=2, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, text="Yes" if patient[13] else "No", font=normal_text_font).grid(column=3, row=2, sticky="w", padx=padx, pady=pady)

                tk.Label(profile_frame, text="Sexual Predator:", font=bold_label_font).grid(column=2, row=3, sticky="e", padx=padx, pady=pady)
                tk.Label(profile_frame, text="Yes" if patient[14] else "No", font=normal_text_font).grid(column=3, row=3, sticky="w", padx=padx, pady=pady)

                # creates a listbox to display search results for cases
                tk.Label(profile_frame, text="Case ID\t\tRelationship to Victim\t\tRole\t\tAge\t\tSame Household?\t\tCustody?", font=bold_label_font).grid(column=0, row=10, columnspan=7, sticky="e", padx=padx, pady=pady)
                cases_list = tk.Listbox(profile_frame, width=entry_width * 4, height=10, font=normal_text_font)
                cases_list.grid(row=11, column=0, columnspan=5, padx=padx, pady=pady)

                # to search cases based on specific person
                def search_cases_by_patient(person_id):
                    global filtered_cases_2
                    config = load_config(filename="database.ini")
                    conn = connect(config)

                    search_query = self.search_entry.get().lower()
                    filtered_cases_2 = []

                    with conn.cursor() as cur:
                        cur.execute(f"SELECT * FROM case_person WHERE person_id={person_id} FETCH FIRST 100 ROWS ONLY".format(search_query))
                        row = cur.fetchone()

                        while row is not None:
                            filtered_cases_2.append(row)
                            row = cur.fetchone()

                    update_cases_list(filtered_cases_2)

                #update the patient list based on search 
                def update_cases_list(filtered_cases):
                    cases_list.delete(0, tk.END)
                    for case in filtered_cases:
                        # this might be the most scuffed line of code i've ever written but for some reason tabs aren't working so this is the only way to get the spacing to behave     -zac
                        cases_list.insert(tk.END, f"                {case[1]}                 {self.get_relationship(case[17])}                                                      {self.get_role(case[18])}                    {case[3]}                               {case[19]}")

                search_cases_by_patient(patient[1])

            def select_person(person):
                pass

        case_buttons_frame = tk.Frame(scrollable_frame)
        case_buttons_frame.grid(row=0, column=0, sticky='w')

        add_new_person_button = tk.Button(case_buttons_frame, text="Add Another Person", command=add_another_person)
        add_new_person_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        save_and_open_button = tk.Button(case_buttons_frame, text="Save and Open Case", command=save_and_open)
        save_and_open_button.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        cancel_button = tk.Button(case_buttons_frame, text="Cancel", command=cancel)
        cancel_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        lookup_person_button = tk.Button(case_buttons_frame, text="Lookup Person", command=lookup_person)
        lookup_person_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        
    # to filter patients based on search
    def search_patients(self, event=None):
        global filtered_patients
        config = load_config(filename="database.ini")
        conn = connect(config)

        search_query = self.search_entry.get().lower()
        filtered_patients = []

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM person WHERE CONCAT(first_name, \' \', middle_name, \' \', last_name)~*\'{0}\' OR CONCAT(first_name, \' \', last_name)~*\'{0}\' ORDER BY last_name FETCH FIRST 100 ROWS ONLY".format(search_query))
            row = cur.fetchone()

            while row is not None:
                filtered_patients.append(row)
                row = cur.fetchone()

        self.update_patient_list(filtered_patients)

    #update the patient list based on search 
    def update_patient_list(self, filtered_patients):
        self.patient_list.delete(0, tk.END)
        for patient in filtered_patients:
            self.patient_list.insert(tk.END, f"{patient[2]} {patient[3]} {patient[4]}")
        self.patient_list.bind("<Double-1>", self.on_patient_select_from_list)

    # callback function when a patient is selected from the list
    def on_patient_select_from_list(self, event):
        selected_index = self.patient_list.curselection()
        if selected_index:
            patient_index = selected_index[0]
            self.show_patient_details(filtered_patients[patient_index])

    # -------------------- Navigation Functions --------------------
    def show_lookup_page(self):
        self.controller.show_frame(lookup_interface)

    def show_general_tab(self):
        self.controller.show_frame(Generaltab_interface.GeneraltabInterface)

    def show_people_tab(self):
        self.controller.show_frame(people_interface.people_interface)

    def show_mh_basic(self):
        self.controller.show_frame(MH_basic_interface.MHBasicInterface)

    def show_mh_assessment(self):
        self.controller.show_frame(MH_assessment.MHassessment)

    def show_mh_treatment_plan(self):
        self.controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface)

    def show_va_tab(self):
        self.controller.show_frame(va_tab_interface.va_interface)

    def show_case_notes(self):
        self.controller.show_frame(case_notes.case_notes_interface)

