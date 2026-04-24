'''
Survey response recode mappings.

Structure:
    SURVEY_RECODES[question_text] = {original_response: recoded_code, ...}

Questions where the source shows "No change" are included as identity
mappings so downstream code can treat every question the same way.
'''

SURVEY_RECODES = {

    # -------------------------------------------------------------------
    # Question 1
    # -------------------------------------------------------------------
    "What are the biggest challenges facing households in your community today?": {
        # Pre-listed options
        "Paying for housing (rent, utilities, mortgage, taxes)": "Housing Cost",
        "Covering basic expenses (groceries, gas, emergencies)": "Cost of Basics",
        "Getting enough food": "Food Access",
        "Finding affordable healthcare": "Healthcare Cost",
        "Mental health challenges (like anxiety, depression)": "Mental Health",
        "Behavioral health challenges (like substance use or addiction)": "Behavioral Health",
        "Child care that is affordable and available": "Affordable Child Care Access",
        "Caring for aging parents or relatives": "Affordable Elder Care Access",
        "Getting to work, school, or appointments (transportation)": "Transportation",
        "Jobs with low pay or no benefits": "Low Wages",
        "Lack of stable jobs with career growth": "Job Instability",
        "Feeling isolated or not connected to community": "Social Isolation",
        "Access to college or training after high school": "Education Access",
        "Impact of flooding and other extreme weather": "Climate Impacts",

        # Write-in responses
        "Finding affordable housing": "Affordable Housing Availability",
        "Language barriers": "Language Access",
        "Domestic violence": "Domestic Violence",
        "High taxes": "Rising Taxes",
        "Political division": "Political Division",
        "ICE": "Immigration Enforcement",
        "Welfare dependence": "Welfare Dependence",
        "Lack of in-home support": "Lack of in Home Support",
        "Gas mileage / fuel costs": "Gas Costs",
        "Rising rents": "Rent Increases",
        "None": "None",
        "Other": "Other",
    },

    # -------------------------------------------------------------------
    # Question 2
    # -------------------------------------------------------------------
    "If an unexpected expense of $400 came up, would you be able to pay it?": {
        "Maybe, with difficulty": "Below ALICE",
        "No": "Below ALICE",
        "Yes": "Above ALICE",
    },

    "Are you part of a community whose voice you feel is not being heard?": {
        "Maybe": "Unheard",
        "No": "Heard",
        "Yes": "Unheard",
    },

    # -------------------------------------------------------------------
    # Question 3
    # -------------------------------------------------------------------
    "What is your primary relationship with United Way of Southern Maine (UWSM)?": {
        "Formerly Involved": "Formerly Connected",
        "I am closely connected (I am a UWSM volunteer, staff, or partner organization)": "Closely Connected",
        "I am moderately connected (For example, I occasionally volunteer and/or donate to UWSM)": "Moderately Connected",
        "I am not connected with United Way": "Not Connected",
    },

    #-------------------------------------------------------------------
    # Question 4
    #-------------------------------------------------------------------
    "How would you consider getting involved locally to be part of the solution?": {
        "Donating money to United Way of Southern Maine": "Donate",
        "Helping connect people to services or resources": "Connect",
        "Speaking up or helping spread the word about important issues": "Speak Up",
        "Joining a group that solves community issues": "Join Group",
        "Sharing my story or experiences to help others understand": "Share Story",
        "Volunteering my time or skills in local programs": "Volunteer",
    },

    #--------------------------------------------------------------------
    # Question 5
    #--------------------------------------------------------------------

    "Which bills or everyday expenses are the hardest for your household to afford?": {
        "Credit Card or Loan Payments": "Credit Card or Loan Payments",
        "Groceries/Food": "Groceries/Food",
        "Medical bills/Healthcare Costs": "Medical bills/Healthcare Costs",
        "Housing costs (e.g., rent, mortgage)": "Housing costs (rent, mortgage)",
        "Childcare or School-Related Expenses": "Childcare or School-Related Expenses",
        "Insurance Premiums (Health, Car, Home, etc)": "Insurance Premiums (Health, Car, Home, etc)",
        "Phone or Internet Service": "Phone or Internet Service",
        "Utilities (e.g., electricity, water, gas)": "Utilities (e.g., electricity, water, gas)",
        "Transportation (e.g., car payments, gas, car repairs or public transport)":
            "Transportation (e.g., car payments, gas, car repairs or public transport)",
    },

    #--------------------------------------------------------------------
    # Question 6
    #--------------------------------------------------------------------
    "Are you currently employed?": {
        "No": "Not Employed",
        "Yes": "Employed",
    },

    #--------------------------------------------------------------------
    # Question 7
    #--------------------------------------------------------------------

    "What type of employment?": {
        "32 hours": "Full-Time - 1 Job",
        "a mixture of part time and self-employed": "Other",
        "Freelance/contract": "Other",
        "Full-time hours (40 or more) working for more than one employer": "Full-Time - Multiple Jobs",
        "Full-time hours (40 or more) working for one employer": "Full-Time - 1 Job",
        "I am election clerk working 3 times a year": "Other",
        "Part-time hours (29 or less)": "Part-Time",
        "Per diem": "Per Diem",
        "Self employed": "Self Employed",
    },

    #--------------------------------------------------------------------
    # Question 8
    #--------------------------------------------------------------------

    "What's getting in the way of being able to cover expenses?": {
        # Pre-listed options
        "I don't have reliable transportation": "Lack of Reliable Transportation",
        "I'm caring for a family member": "Family Care Responsibilities",
        "I have health issues or a disability": "Health Issues or Disability",
        "I don't have time to go back to school or get more training": "Lack of Time for Training/Education",
        "I don't have the skills or training needed for a better-paying job": "Lack of Skills or Training",
        "I've been turned away from jobs because of my background": "Turned Away",
        "I don't have affordable child care": "Lack of Affordable Child Care",
        "I'm not sure what opportunities are available": "Unaware of or Limited Job Opportunities",

        # Write-in responses (source shows these as already-categorized
        # values with no further recode, so identity mapping is used).
        "Age-Related Employment Barriers": "Age-Related Employment Barriers",
        "Insufficient Income / Fixed Income": "Insufficient Income / Fixed Income",
        "High Cost of Living": "High Cost of Living",
        "Retirement Challenges": "Retirement Challenges",
        "Debt / Cash Flow Issues": "Debt / Cash Flow Issues",
        "Financially Stable / Doing Well": "Financially Stable / Doing Well",
    },

    #--------------------------------------------------------------------
    # Question 9
    #--------------------------------------------------------------------

    "What supports would be most helpful for you?": {
        # Pre-listed options
        "Help with food or groceries": "Food",
        "Help affording healthcare or mental health support": "Health/Mental Health",
        "Help with transportation (gas, car repair, bus passes, etc.)": "Transportation",
        "Help with job training or education": "Job Training/Education",
        "Help managing debt or improving credit": "Debt/Credit",
        "Employment navigation": "Employment",
        "Rental assistance": "Rental Assistance",
        "Help navigating programs like SNAP, TANF": "SNAP/TANF Navigation",

        # Write-in responses (identity mappings).
        "Increased Income": "Increased Income",
        "Taxes": "Taxes",
        "Home Ownership": "Home Ownership",
    },

    #--------------------------------------------------------------------
    # Question 10 
    #--------------------------------------------------------------------

    "Where would you like to be in 5 years?": {
        "Desire to be financially stable, meet expenses, reduce debt, or build savings.": "Financial Stability",
        "Goals related to having stable work, better income, job satisfaction, or career advancement.": "Employment & Income",
        "Aspirations related to education, training, or starting/running a business.": "Education & Entrepreneurship",
        "Desire for stable housing or homeownership.": "Housing Stability",
        "Desire for improved physical or mental health.": "Health & Wellbeing",
        "Aspirations related to family wellbeing, relationships, or overall life stability.": "Family & Life Stability",
        "Minimal expectations, uncertainty, or vague responses.": "Basic Survival",
        "Plans or hopes to retire or remain comfortably retired.": "Retirement Security",
        "Desire for more time with family or loved ones.": "Family Time",
        "Desire to remain living independently in one's home as they age.": "Age in Place",
        "Minimal expectations or survival-oriented outlook.": "Basic Survival",
        "Aspirations related to fairness, dignity, or societal conditions.": "Civic & Social",
        "Response does not clearly indicate a specific goal or aspiration.": "UNCLEAR",
    },

    #--------------------------------------------------------------------
    # Question 11 (Merge with 4)
    #--------------------------------------------------------------------
    "How would you like to be part of creating change in your community?": {
        "Donating money to United Way of Southern Maine": "Donate",
        "Helping connect people to services or resources": "Connect",
        "Speaking up or helping spread the word about important issues": "Speak Up",
        "Joining a group that solves community issues": "Join Group",
        "Sharing my story or experiences to help others understand": "Share Story",
        "Volunteering my time or skills in local programs": "Volunteer",
    },
}


def recode(question: str, response: str) -> str:
    """
    Look up the recoded value for a given question/response.
    Returns the original response if no mapping exists (safe fallback).
    """
    mapping = SURVEY_RECODES.get(question, {})
    return mapping.get(response, response)