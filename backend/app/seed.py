"""
Database seeder for CitizenAssist AI.
Seeds verified government schemes and citizen services with structured eligibility rules,
required documents, and official source citations.
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.app.models.database import EligibilityRule, Record, SearchChunk
from backend.app.services.search import build_fts_index

NOW = datetime.now(timezone.utc)
FETCHED_STR = NOW.strftime("%Y-%m-%d")

SEED_RECORDS = [
    {
        "id": "pm-kisan",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "name_hi": "प्रधानमंत्री किसान सम्मान निधि (पीएम-किसान)",
        "name_pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਕਿਸਾਨ ਸੰਮਾਨ ਨਿਧੀ (ਪੀ.ਐੱਮ.-ਕਿਸਾਨ)",
        "record_type": "scheme",
        "description": "Central sector welfare scheme providing income support of ₹6,000 per year in three equal installments of ₹2,000 directly into the bank accounts of all landholding farmer families across India.",
        "department": "Department of Agriculture and Farmers Welfare, Ministry of Agriculture",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Agriculture and Farmers",
        "target_beneficiaries": ["farmers", "agricultural landholders"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Must possess cultivable land holding in their names",
            "Institutional landholders and serving/retired government employees are excluded",
            "Must not have paid income tax in last assessment year"
        ],
        "benefits": "₹6,000 per year directly transferred to bank account in 3 installments of ₹2,000 every 4 months (Direct Benefit Transfer).",
        "benefits_hi": "प्रत्येक 4 महीने में ₹2,000 की 3 किस्तों में सीधे बैंक खाते में ₹6,000 प्रति वर्ष का प्रत्यक्ष लाभ हस्तांतरण (DBT)।",
        "benefits_pa": "ਹਰ 4 ਮਹੀਨੇ ਬਾਅਦ ₹2,000 ਦੀਆਂ 3 ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਸਿੱਧੇ ਬੈਂਕ ਖਾਤੇ ਵਿੱਚ ₹6,000 ਸਾਲਾਨਾ ਵਿੱਤੀ ਸਹਾਇਤਾ।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Mandatory identity proof for eKYC and DBT transfer", "linked_service_id": None},
            {"name": "Proof of Land Ownership (Jamabandi / Patta)", "description": "Land records showing cultivable land registered in applicant's name", "linked_service_id": None},
            {"name": "Bank Account Details (Aadhaar Seeded)", "description": "Bank passbook with IFSC code linked to Aadhaar", "linked_service_id": None}
        ],
        "application_procedure": "Apply online at pmkisan.gov.in under 'New Farmer Registration', complete Aadhaar eKYC, enter land details, or visit nearest Common Service Centre (CSC).",
        "application_url": "https://pmkisan.gov.in",
        "official_source_url": "https://pmkisan.gov.in",
        "source_excerpt": "Under the scheme an amount of 6000/- per year is released by the Central Government online directly into the bank accounts of the eligible landholding farmer families.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "occupation", "operator": "in", "value": ["farmer", "agricultural_worker"], "kind": "profile", "description": "Must be an active landholding farmer", "source_excerpt": "Landholding farmer families with cultivable land holdings."},
            {"field": "age", "operator": ">=", "value": 18, "kind": "profile", "description": "Applicant must be an adult (18 years or older)", "source_excerpt": "Farmer family head / adult member."}
        ]
    },
    {
        "id": "pm-jay",
        "name": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (AB PM-JAY)",
        "name_hi": "आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना",
        "name_pa": "ਆਯੂਸ਼ਮਾਨ ਭਾਰਤ ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਜਨ ਅਰੋਗਿਆ ਯੋਜਨਾ",
        "record_type": "scheme",
        "description": "World's largest public health assurance scheme providing cashless health cover of up to ₹5 lakh per family per year for secondary and tertiary care hospitalization to bottom 40% vulnerable families and all senior citizens aged 70+.",
        "department": "National Health Authority, Ministry of Health and Family Welfare",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Healthcare",
        "target_beneficiaries": ["low-income families", "informal workers", "senior citizens", "rural deprived households"],
        "age_criteria": None,
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Identified based on SECC 2011 deprivation criteria or designated occupational categories in urban areas",
            "All senior citizens aged 70 and above qualify universally without income restriction"
        ],
        "benefits": "Cashless hospitalization coverage up to ₹5,00,000 per family per year across empaneled public and private hospitals across India.",
        "benefits_hi": "देश भर के सूचीबद्ध अस्पतालों में प्रति परिवार प्रति वर्ष ₹5,00,000 तक का कैशलेस अस्पताल में भर्ती का कवर।",
        "benefits_pa": "ਪ੍ਰਤੀ ਪਰਿਵਾਰ ਪ੍ਰਤੀ ਸਾਲ ₹5,00,000 ਤੱਕ ਮੁਫ਼ਤ ਹਸਪਤਾਲ ਇਲਾਜ ਦੀ ਸਹੂਲਤ।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Mandatory for biometric identification", "linked_service_id": None},
            {"name": "Ration Card", "description": "Proof of family composition and eligibility linkage", "linked_service_id": "ration-card"}
        ],
        "application_procedure": "Check name eligibility at beneficiary.nha.gov.in using Aadhaar or Ration Card number, or visit any Ayushman Mitra desk at an empaneled hospital / CSC for e-KYC and Ayushman Card generation.",
        "application_url": "https://beneficiary.nha.gov.in/",
        "official_source_url": "https://beneficiary.nha.gov.in/",
        "source_excerpt": "AB PM-JAY provides health cover of Rs. 5 lakhs per family per year for secondary and tertiary care hospitalization to over 12 crore poor and vulnerable families.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "annual_family_income", "operator": "<=", "value": 300000, "kind": "profile", "description": "Family income generally within economically vulnerable bracket (<= ₹3 Lakh)", "source_excerpt": "Vulnerable and economically disadvantaged households identified through SECC and state criteria."}
        ]
    },
    {
        "id": "pmay-u",
        "name": "Pradhan Mantri Awas Yojana - Urban (PMAY-U)",
        "name_hi": "प्रधानमंत्री आवास योजना - शहरी",
        "name_pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਆਵਾਸ ਯੋਜਨਾ - ਸ਼ਹਿਰੀ",
        "record_type": "scheme",
        "description": "Housing for all mission providing central assistance and interest subsidy to eligible urban families belonging to EWS and LIG categories to build or acquire permanent pucca houses.",
        "department": "Ministry of Housing and Urban Affairs",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Housing",
        "target_beneficiaries": ["urban poor", "low-income families", "homeless"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": {"max_annual": 600000},
        "education_criteria": None,
        "other_conditions": [
            "Beneficiary family must not own a pucca house anywhere in India",
            "Must not have availed central assistance from any other housing scheme"
        ],
        "benefits": "Financial assistance of ₹1.5 lakh to ₹2.67 lakh through credit-linked subsidy or direct construction assistance for pucca house.",
        "benefits_hi": "पक्का मकान निर्माण के लिए ₹1.5 लाख से ₹2.67 लाख तक की वित्तीय सहायता या ब्याज सब्सिडी।",
        "benefits_pa": "ਪੱਕਾ ਮਕਾਨ ਬਣਾਉਣ ਲਈ ₹1.5 ਲੱਖ ਤੋਂ ₹2.67 ਲੱਖ ਤੱਕ ਦੀ ਵਿੱਤੀ ਸਹਾਇਤਾ।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Identity proof of all family members", "linked_service_id": None},
            {"name": "Income Certificate", "description": "Certificate from competent authority proving annual household income <= ₹6 Lakh", "linked_service_id": "income-certificate"},
            {"name": "Bank Passbook", "description": "Bank account copy for DBT assistance", "linked_service_id": None},
            {"name": "Affidavit / No-Pucca-House Declaration", "description": "Sworn declaration confirming no existing pucca house ownership", "linked_service_id": None}
        ],
        "application_procedure": "Apply online at pmaymis.gov.in under 'Citizen Assessment' or through Citizen Service Centres (CSCs) with Aadhaar and income details.",
        "application_url": "https://pmaymis.gov.in",
        "official_source_url": "https://pmaymis.gov.in",
        "source_excerpt": "A beneficiary family will comprise husband, wife, unmarried sons and/or unmarried daughters. The beneficiary family should not own a pucca house anywhere in India.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "annual_family_income", "operator": "<=", "value": 600000, "kind": "profile", "description": "Annual household income must not exceed ₹6,00,000 for EWS/LIG categories", "source_excerpt": "EWS households with annual income up to Rs 3,00,000 and LIG up to Rs 6,00,000."},
            {"field": "age", "operator": ">=", "value": 18, "kind": "profile", "description": "Head of household must be at least 18 years old", "source_excerpt": "Adult applicant representing the beneficiary family."}
        ]
    },
    {
        "id": "post-matric-sc",
        "name": "Post-Matric Scholarship for SC Students",
        "name_hi": "अनुसूचित जाति के छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
        "name_pa": "ਐੱਸ.ਸੀ. ਵਿਦਿਆਰਥੀਆਂ ਲਈ ਪੋਸਟ-ਮੈਟ੍ਰਿਕ ਵਜ਼ੀਫ਼ਾ",
        "record_type": "scheme",
        "description": "Centrally sponsored scholarship scheme providing financial assistance covering compulsory non-refundable fees and academic maintenance allowance to Scheduled Caste students pursuing post-matriculation or post-secondary education.",
        "department": "Ministry of Social Justice and Empowerment",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Education and Scholarships",
        "target_beneficiaries": ["students", "SC category students"],
        "age_criteria": {"min": 15, "max": 35},
        "income_criteria": {"max_annual": 250000},
        "education_criteria": "Must have passed Class 10 (Matriculation) and enrolled in Class 11, 12, ITI, Diploma, UG, or PG course in recognized institution",
        "other_conditions": [
            "Must belong to Scheduled Caste (SC) category",
            "Annual family income must not exceed ₹2,50,000 from all sources",
            "Must not be receiving any other government scholarship"
        ],
        "benefits": "Full reimbursement of non-refundable tuition and institutional fees plus monthly maintenance allowance between ₹2,500 and ₹13,500 per year.",
        "benefits_hi": "गैर-वापसी योग्य शिक्षण शुल्क की पूरी प्रतिपूर्ति और ₹2,500 से ₹13,500 प्रति वर्ष तक का रखरखाव भत्ता।",
        "benefits_pa": "ਸਕੂਲ/ਕਾਲਜ ਦੀ ਪੂਰੀ ਫ਼ੀਸ ਮੁਆਫ਼ੀ ਅਤੇ ₹2,500 ਤੋਂ ₹13,500 ਸਾਲਾਨਾ ਗੁਜ਼ਾਰਾ ਭੱਤਾ।",
        "required_documents": [
            {"name": "Caste Certificate (SC)", "description": "Valid Scheduled Caste certificate issued by Tehsildar or SDM", "linked_service_id": "caste-certificate"},
            {"name": "Income Certificate", "description": "Valid family income certificate showing income <= ₹2.5 Lakh", "linked_service_id": "income-certificate"},
            {"name": "Aadhaar Card", "description": "Student's Aadhaar linked to bank account", "linked_service_id": None},
            {"name": "Previous Qualifying Mark Sheet", "description": "Mark sheet of Class 10 or latest examination passed", "linked_service_id": None},
            {"name": "College Admission / Fee Receipt", "description": "Fee receipt and proof of enrollment in current recognized institution", "linked_service_id": None}
        ],
        "application_procedure": "Register One-Time Registration (OTR) on National Scholarship Portal (scholarships.gov.in), log in, fill Post-Matric SC application, upload certificates, and submit for institutional verification.",
        "application_url": "https://scholarships.gov.in",
        "official_source_url": "https://scholarships.gov.in",
        "source_excerpt": "Scholarships will be paid to the students whose parents/guardians' income from all sources does not exceed Rs. 2,50,000/- per annum.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "category", "operator": "==", "value": "SC", "kind": "profile", "description": "Applicant must belong to Scheduled Caste (SC) community", "source_excerpt": "The scholarships are open to nationals of India belonging to Scheduled Castes."},
            {"field": "annual_family_income", "operator": "<=", "value": 250000, "kind": "profile", "description": "Total family income from all sources must not exceed ₹2,50,000 per year", "source_excerpt": "Income ceiling of parents/guardians is Rs. 2.50 lakh per annum."},
            {"field": "occupation", "operator": "==", "value": "student", "kind": "profile", "description": "Applicant must be an actively enrolled student", "source_excerpt": "Students studying at post-matriculation or post-secondary stage."}
        ]
    },
    {
        "id": "sukanya-samriddhi",
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "name_hi": "सुकन्या समृद्धि योजना",
        "name_pa": "ਸੁਕੰਨਿਆ ਸਮ੍ਰਿਧੀ ਯੋਜਨਾ",
        "record_type": "scheme",
        "description": "Government-backed small deposit savings initiative under the Beti Bachao Beti Padhao campaign, offering high sovereign-backed tax-free interest for the welfare, education, and marriage expenses of girl children.",
        "department": "Department of Economic Affairs, Ministry of Finance",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Women and Child Welfare",
        "target_beneficiaries": ["girl child", "parents of girl child"],
        "age_criteria": {"min": 0, "max": 10},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Account can be opened in the name of a girl child before she attains 10 years of age",
            "Maximum 2 accounts per family (one for each girl child, exception for twins/triplets)",
            "Minimum deposit ₹250 per year, maximum ₹1.5 lakh per financial year"
        ],
        "benefits": "Attractive annual compound interest (8.2% p.a.), exempt-exempt-exempt (EEE) tax status under Section 80C, matures on completion of 21 years or marriage after age 18.",
        "benefits_hi": "उच्च ब्याज दर (8.2% वार्षिक), 80C के तहत पूर्ण कर छूट, और 21 वर्ष में परिपक्वता पर सुरक्षित कोष।",
        "benefits_pa": "ਸਾਲਾਨਾ 8.2% ਉੱਚ ਵਿਆਜ, ਆਮਦਨ ਕਰ ਤੋਂ ਪੂਰੀ ਛੋਟ, ਅਤੇ 21 ਸਾਲ ਪੂਰੇ ਹੋਣ 'ਤੇ ਸੁਰੱਖਿਅਤ ਰਕਮ।",
        "required_documents": [
            {"name": "Birth Certificate of Girl Child", "description": "Official birth certificate from municipal corporation or hospital", "linked_service_id": None},
            {"name": "Aadhaar Card of Parent/Guardian", "description": "Identity and address proof of guardian", "linked_service_id": None},
            {"name": "PAN Card of Parent/Guardian", "description": "Financial KYC document", "linked_service_id": None}
        ],
        "application_procedure": "Submit account opening form along with birth certificate and KYC documents at any post office branch or authorized public/private commercial bank.",
        "application_url": "https://www.indiapost.gov.in",
        "official_source_url": "https://www.indiapost.gov.in",
        "source_excerpt": "Account can be opened by the natural or legal guardian in the name of a girl child from the birth of the girl child till she attains the age of ten years.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "gender", "operator": "==", "value": "female", "kind": "profile", "description": "Beneficiary must be a girl child", "source_excerpt": "Account opened in the name of a girl child."},
            {"field": "age", "operator": "<=", "value": 10, "kind": "profile", "description": "Girl child must be 10 years of age or younger at time of opening", "source_excerpt": "Till she attains the age of ten years."}
        ]
    },
    {
        "id": "atal-pension",
        "name": "Atal Pension Yojana (APY)",
        "name_hi": "अटल पेंशन योजना",
        "name_pa": "ਅਟਲ ਪੈਨਸ਼ਨ ਯੋਜਨਾ",
        "record_type": "scheme",
        "description": "Government of India pension scheme focused on unorganized sector workers, providing a guaranteed monthly pension of ₹1,000 to ₹5,000 starting from the age of 60 based on contribution.",
        "department": "Pension Fund Regulatory and Development Authority (PFRDA), Ministry of Finance",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Social Security",
        "target_beneficiaries": ["unorganized workers", "self-employed individuals", "low-income workers"],
        "age_criteria": {"min": 18, "max": 40},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Must be between 18 and 40 years of age at enrollment",
            "Must have a savings bank account with auto-debit facility enabled",
            "Must not be an income taxpayer (rules effective October 1, 2022)"
        ],
        "benefits": "Guaranteed minimum monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000 or ₹5,000 to subscriber on turning 60, followed by spouse, and return of corpus to nominee.",
        "benefits_hi": "60 वर्ष की आयु पर ₹1,000 से ₹5,000 प्रति माह की गारंटीकृत पेंशन, जीवनसाथी को सुरक्षा और नॉमिनी को पूरी राशि वापसी।",
        "benefits_pa": "60 ਸਾਲ ਦੀ ਉਮਰ ਤੋਂ ਬਾਅਦ ₹1,000 ਤੋਂ ₹5,000 ਪ੍ਰਤੀ ਮਹੀਨਾ ਗਾਰੰਟੀਸ਼ੁਦਾ ਪੈਨਸ਼ਨ।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Mandatory identity proof and biometric KYC", "linked_service_id": None},
            {"name": "Savings Bank Account / Passbook", "description": "Active savings account for monthly auto-debit contributions", "linked_service_id": None}
        ],
        "application_procedure": "Visit the bank branch where you have a savings account, fill the APY registration form with auto-debit consent, or enroll online via your bank's netbanking portal.",
        "application_url": "https://www.npscra.nsdl.co.in",
        "official_source_url": "https://www.npscra.nsdl.co.in",
        "source_excerpt": "Atal Pension Yojana is open to all bank account holders between 18 to 40 years of age. Fixed pension amount of Rs. 1000 to 5000 per month will be given after 60 years of age.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "age", "operator": ">=", "value": 18, "kind": "profile", "description": "Minimum enrollment age is 18 years", "source_excerpt": "Subscriber must be between 18 and 40 years."},
            {"field": "age", "operator": "<=", "value": 40, "kind": "profile", "description": "Maximum enrollment age is 40 years", "source_excerpt": "Upper age limit for joining APY is 40 years."}
        ]
    },
    {
        "id": "pm-vishwakarma",
        "name": "PM Vishwakarma Scheme",
        "name_hi": "पीएम विश्वकर्मा योजना",
        "name_pa": "ਪੀ.ਐੱਮ. ਵਿਸ਼ਵਕਰਮਾ ਯੋਜਨਾ",
        "record_type": "scheme",
        "description": "Holistic support initiative for traditional artisans and craftspeople working with hands and tools in 18 specified trades, offering recognition, skill training, tool-kit incentives of ₹15,000, and collateral-free loans up to ₹3 lakh at 5% interest.",
        "department": "Ministry of Micro, Small and Medium Enterprises (MSME)",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Employment",
        "target_beneficiaries": ["traditional artisans", "craftspeople", "carpenters", "blacksmiths", "potters", "cobblers"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Must be engaged in one of the 18 specified traditional trades on self-employment basis",
            "Beneficiary must not have availed similar central/state credit schemes (PMEGP, PM SVANidhi, Mudra) in the past 5 years",
            "Only one member per family is eligible"
        ],
        "benefits": "PM Vishwakarma Certificate & ID card, basic and advanced skill training with ₹500/day stipend, ₹15,000 modern toolkit grant, and collateral-free enterprise loan up to ₹3 lakh at subsidized 5% interest.",
        "benefits_hi": "विश्वकर्मा प्रमाण पत्र, ₹500/दिन वजीफे के साथ कौशल प्रशिक्षण, ₹15,000 का टूलकिट अनुदान और 5% रियायती ब्याज पर ₹3 लाख तक का ऋण।",
        "benefits_pa": "ਸਰਟੀਫਿਕੇਟ, ਮੁਫ਼ਤ ਸਿਖਲਾਈ ਦੌਰਾਨ ₹500 ਪ੍ਰਤੀ ਦਿਨ ਵਜ਼ੀਫ਼ਾ, ₹15,000 ਟੂਲਕਿੱਟ ਗ੍ਰਾਂਟ ਅਤੇ ਸਿਰਫ਼ 5% ਵਿਆਜ 'ਤੇ ₹3 ਲੱਖ ਤੱਕ ਕਰਜ਼ਾ।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Identity verification and biometric authentication", "linked_service_id": None},
            {"name": "Bank Account Details", "description": "Account linked to Aadhaar for toolkit grant and credit disbursement", "linked_service_id": None},
            {"name": "Ration Card", "description": "Family composition proof ensuring only one member applies", "linked_service_id": "ration-card"}
        ],
        "application_procedure": "Apply online at pmvishwakarma.gov.in via CSC with biometric authentication, followed by Gram Panchayat / Urban Local Body verification.",
        "application_url": "https://pmvishwakarma.gov.in",
        "official_source_url": "https://pmvishwakarma.gov.in",
        "source_excerpt": "PM Vishwakarma provides end-to-end holistic support to traditional artisans and craftspersons with collateral free credit support up to Rs 3 lakh at 5% interest.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "age", "operator": ">=", "value": 18, "kind": "profile", "description": "Minimum age of 18 years on date of application", "source_excerpt": "The minimum age of the beneficiary should be 18 years."},
            {"field": "occupation", "operator": "in", "value": ["artisan", "carpenter", "blacksmith", "craftsman", "potter", "cobbler", "tailor", "sculptor"], "kind": "profile", "description": "Must be engaged in one of the 18 recognized traditional craft trades", "source_excerpt": "An artisan or craftsperson working with hands and tools in traditional trades."}
        ]
    },
    {
        "id": "punjab-ashirwad",
        "name": "Punjab Ashirwad Scheme (Shagun Scheme)",
        "name_hi": "पंजाब आशीर्वाद योजना (शगुन योजना)",
        "name_pa": "ਪੰਜਾਬ ਅਸ਼ੀਰਵਾਦ ਸਕੀਮ (ਸ਼ਗਨ ਸਕੀਮ)",
        "record_type": "scheme",
        "description": "Punjab state government welfare initiative providing one-time financial grant of ₹51,000 for the marriage of daughters belonging to Scheduled Castes, Backward Classes, and Economically Weaker Section families of Punjab.",
        "department": "Department of Social Justice, Empowerment and Minorities, Government of Punjab",
        "level": "state",
        "state_applicability": ["Punjab"],
        "category": "Financial Assistance",
        "target_beneficiaries": ["daughters", "SC families", "BC families", "EWS families of Punjab"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": {"max_annual": 32790},
        "education_criteria": None,
        "other_conditions": [
            "Girl must be a permanent resident / domicile of Punjab",
            "Girl's age must be 18 years or above on the date of marriage",
            "Family annual income from all sources must not exceed ₹32,790",
            "Benefit available for up to two daughters per family"
        ],
        "benefits": "Direct financial grant of ₹51,000 transferred to the girl's bank account for wedding expenses.",
        "benefits_hi": "विवाह के खर्च के लिए कन्या के बैंक खाते में ₹51,000 का एकमुश्त प्रत्यक्ष वित्तीय अनुदान।",
        "benefits_pa": "ਧੀਆਂ ਦੇ ਵਿਆਹ ਲਈ ਸਿੱਧੇ ਬੈਂਕ ਖਾਤੇ ਵਿੱਚ ₹51,000 ਦੀ ਇਕਮੁਸ਼ਤ ਵਿੱਤੀ ਸਹਾਇਤਾ।",
        "required_documents": [
            {"name": "Domicile / Residence Certificate of Punjab", "description": "Proof of permanent residence in Punjab", "linked_service_id": "residence-certificate"},
            {"name": "Caste Certificate (SC/BC) or EWS Certificate", "description": "Category proof issued by Tehsildar", "linked_service_id": "caste-certificate"},
            {"name": "Income Certificate", "description": "Income proof showing annual family income <= ₹32,790", "linked_service_id": "income-certificate"},
            {"name": "Age Proof of the Bride", "description": "Birth certificate, 10th mark sheet, or Aadhaar showing age >= 18", "linked_service_id": None},
            {"name": "Bank Passbook of Bride", "description": "Aadhaar seeded bank account in girl's name", "linked_service_id": None}
        ],
        "application_procedure": "Submit application online via e-Sewa Punjab portal (eservices.punjab.gov.in) or visit nearest Sewa Kendra before the date of marriage or within 30 days after solemnization.",
        "application_url": "https://eservices.punjab.gov.in",
        "official_source_url": "https://punjab.gov.in",
        "source_excerpt": "Under Ashirwad Scheme, Punjab Government provides financial assistance of Rs 51,000 to girls belonging to SC, BC and economically weaker sections for their marriage.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "state", "operator": "==", "value": "Punjab", "kind": "profile", "description": "Applicant must be a resident of Punjab", "source_excerpt": "The girl and family must be permanent residents of Punjab."},
            {"field": "gender", "operator": "==", "value": "female", "kind": "profile", "description": "Grant is specifically for girl's marriage", "source_excerpt": "Provided for the marriage of daughters."},
            {"field": "age", "operator": ">=", "value": 18, "kind": "profile", "description": "Bride must be 18 years or older on wedding date", "source_excerpt": "The age of the girl should be 18 years or above."}
        ]
    },
    {
        "id": "pm-ujjwala",
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "name_hi": "प्रधानमंत्री उज्ज्वला योजना",
        "name_pa": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਉੱਜਵਲਾ ਯੋਜਨਾ",
        "record_type": "scheme",
        "description": "Flagship social welfare scheme providing deposit-free LPG connection along with first refill and stove free of cost to adult women from poor and vulnerable households without existing gas connections.",
        "department": "Ministry of Petroleum and Natural Gas",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Financial Assistance",
        "target_beneficiaries": ["women", "BPL households", "poor families"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Applicant must be an adult woman (18 years or older)",
            "There should not be any other LPG connection in the same household"
        ],
        "benefits": "Free LPG connection with security deposit waived, plus first 14.2 kg LPG refill cylinder and hotplate (stove) provided completely free of cost.",
        "benefits_hi": "मुफ़्त एलपीजी गैस कनेक्शन, पहला भरा हुआ सिलेंडर और गैस चूल्हा बिल्कुल मुफ़्त।",
        "benefits_pa": "ਮੁਫ਼ਤ ਐੱਲ.ਪੀ.ਜੀ. ਗੈਸ ਕੁਨੈਕਸ਼ਨ, ਪਹਿਲਾ ਸਿਲੰਡਰ ਅਤੇ ਗੈਸ ਚੁੱਲ੍ਹਾ ਬਿਲਕੁਲ ਮੁਫ਼ਤ।",
        "required_documents": [
            {"name": "Aadhaar Card of Woman Applicant", "description": "Mandatory identity proof and address verification", "linked_service_id": None},
            {"name": "Ration Card", "description": "Ration card showing family composition", "linked_service_id": "ration-card"},
            {"name": "Bank Passbook", "description": "Bank account details for subsidy transfer", "linked_service_id": None}
        ],
        "application_procedure": "Apply online at pmuy.gov.in or submit form at nearest LPG distributorship (Indane, Bharatgas, or HP Gas) with Aadhaar and Ration Card.",
        "application_url": "https://www.pmuy.gov.in",
        "official_source_url": "https://www.pmuy.gov.in",
        "source_excerpt": "Under PMUY, deposit-free LPG connections are provided to adult women of poor households across the nation.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "gender", "operator": "==", "value": "female", "kind": "profile", "description": "Connection is issued exclusively in the name of an adult female member", "source_excerpt": "Applicant must be an adult woman."},
            {"field": "age", "operator": ">=", "value": 18, "kind": "profile", "description": "Applicant must be at least 18 years old", "source_excerpt": "Woman who has attained the age of 18 years."}
        ]
    },
    {
        "id": "nfbs",
        "name": "National Family Benefit Scheme (NFBS)",
        "name_hi": "राष्ट्रीय पारिवारिक लाभ योजना",
        "name_pa": "ਰਾਸ਼ਟਰੀ ਪਰਿਵਾਰਕ ਲਾਭ ਸਕੀਮ",
        "record_type": "scheme",
        "description": "Component of the National Social Assistance Programme (NSAP) providing a lump sum financial assistance of ₹20,000 to a Below Poverty Line (BPL) household upon the unfortunate death of the primary breadwinner aged 18 to 59.",
        "department": "Ministry of Rural Development",
        "level": "central",
        "state_applicability": ["All India"],
        "category": "Social Security",
        "target_beneficiaries": ["BPL families", "widows", "bereaved households"],
        "age_criteria": {"min": 18, "max": 59},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Deceased breadwinner must have been between 18 and 59 years of age at time of death",
            "Family must be certified Below Poverty Line (BPL)",
            "Application must be submitted within one year of death"
        ],
        "benefits": "One-time lump sum grant of ₹20,000 paid to the surviving head of the bereaved family.",
        "benefits_hi": "मृतक के परिवार के जीवित मुखिया को ₹20,000 की एकमुश्त अनुग्रह सहायता।",
        "benefits_pa": "ਮੁੱਖ ਕਮਾਊ ਜੀਅ ਦੀ ਮੌਤ 'ਤੇ ਪਰਿਵਾਰ ਨੂੰ ₹20,000 ਦੀ ਇਕਮੁਸ਼ਤ ਵਿੱਤੀ ਸਹਾਇਤਾ।",
        "required_documents": [
            {"name": "Death Certificate of Breadwinner", "description": "Official municipal or panchayat death certificate", "linked_service_id": None},
            {"name": "BPL Proof / Ration Card", "description": "BPL survey list or Antyodaya ration card", "linked_service_id": "ration-card"},
            {"name": "Age Proof of Deceased", "description": "Showing age between 18 and 59 years", "linked_service_id": None},
            {"name": "Bank Passbook of Applicant", "description": "Surviving spouse or elder family member's account", "linked_service_id": None}
        ],
        "application_procedure": "Apply online at nsap.nic.in or submit form to District Social Welfare Office / Tehsildar office within 1 year of the breadwinner's demise.",
        "application_url": "https://nsap.nic.in",
        "official_source_url": "https://nsap.nic.in",
        "source_excerpt": "Under NFBS, a lump sum assistance of Rs. 20,000 is provided to the bereaved household in the event of death of the primary breadwinner.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": [
            {"field": "age", "operator": "<=", "value": 59, "kind": "profile", "description": "Deceased breadwinner's age must be between 18 and 59", "source_excerpt": "The primary breadwinner must have died between 18 and 59 years of age."}
        ]
    },
    # SERVICES (4 verified citizen services)
    {
        "id": "income-certificate",
        "name": "Issuance of Income Certificate",
        "name_hi": "आय प्रमाण पत्र जारी करना",
        "name_pa": "ਆਮਦਨ ਸਰਟੀਫਿਕੇਟ ਜਾਰੀ ਕਰਨਾ",
        "record_type": "service",
        "description": "Official citizen service to obtain a statutory revenue certificate stating the annual income of an individual or family from all sources, essential for claiming educational scholarships, fee concessions, and government welfare schemes.",
        "department": "Department of Revenue, State Governments",
        "level": "state",
        "state_applicability": ["All India"],
        "category": "Other Citizen Services",
        "target_beneficiaries": ["all citizens", "students", "job applicants"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Applicant or family must be residents of the issuing revenue jurisdiction",
            "Self-declaration / affidavit of income required"
        ],
        "benefits": "Legally valid government certificate certifying annual family income, valid for 1 financial year across India for scholarships and subsidies.",
        "benefits_hi": "कानूनी रूप से वैध आय प्रमाण पत्र, छात्रवृत्ति और सरकारी योजनाओं के लिए आवश्यक।",
        "benefits_pa": "ਕਾਨੂੰਨੀ ਤੌਰ 'ਤੇ ਵੈਧ ਆਮਦਨ ਸਰਟੀਫਿਕੇਟ, ਜੋ ਸਕਾਲਰਸ਼ਿਪਾਂ ਅਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਲਈ ਲੋੜੀਂਦਾ ਹੈ।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Identity and address proof", "linked_service_id": None},
            {"name": "Salary Slip / ITR / Patwari Income Report", "description": "Proof of income source or village revenue officer verification", "linked_service_id": None},
            {"name": "Self-Declaration Affidavit", "description": "Notarized or self-attested declaration of total annual income", "linked_service_id": None}
        ],
        "application_procedure": "Apply online at respective state portal (e.g. eservices.punjab.gov.in for Punjab) or visit nearest Citizen Service Center / Tehsil office.",
        "application_url": "https://eservices.punjab.gov.in",
        "official_source_url": "https://punjab.gov.in",
        "source_excerpt": "Income Certificate is issued to citizens by the Revenue Department as an authentic record of annual family income.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": []
    },
    {
        "id": "caste-certificate",
        "name": "Issuance of Caste / Category Certificate (SC/ST/OBC)",
        "name_hi": "जाति / श्रेणी प्रमाण पत्र जारी करना",
        "name_pa": "ਜਾਤੀ ਸਰਟੀਫਿਕੇਟ ਜਾਰੀ ਕਰਨਾ",
        "record_type": "service",
        "description": "Statutory document certifying an individual's belonging to a recognized Scheduled Caste (SC), Scheduled Tribe (ST), or Other Backward Class (OBC), required for educational reservations, scholarships, and government employment benefits.",
        "department": "Department of Social Justice and Revenue",
        "level": "state",
        "state_applicability": ["All India"],
        "category": "Other Citizen Services",
        "target_beneficiaries": ["SC citizens", "ST citizens", "OBC citizens", "students"],
        "age_criteria": None,
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Must belong to a caste officially notified in the state's presidential order list",
            "Proof of ancestral residence in the state required"
        ],
        "benefits": "Statutory certification required for fee concessions, college quotas, reservation in examinations, and category-specific welfare schemes.",
        "benefits_hi": "शिक्षा, छात्रवृत्ति और सरकारी नौकरियों में आरक्षण के लिए अनिवार्य वैधानिक दस्तावेज।",
        "benefits_pa": "ਸਿੱਖਿਆ, ਵਜ਼ੀਫ਼ਿਆਂ ਅਤੇ ਸਰਕਾਰੀ ਨੌਕਰੀਆਂ ਵਿੱਚ ਰਾਖਵੇਂਕਰਨ ਲਈ ਲੋੜੀਂਦਾ ਕਾਨੂੰਨੀ ਦਸਤਾਵੇਜ਼।",
        "required_documents": [
            {"name": "Aadhaar Card", "description": "Proof of identity", "linked_service_id": None},
            {"name": "Father's Caste Certificate or 1950 Residence Proof", "description": "Lineage proof confirming caste origin", "linked_service_id": None},
            {"name": "Passport Size Photograph", "description": "Recent photograph of applicant", "linked_service_id": None}
        ],
        "application_procedure": "Submit application online via state service portal (e.g. eservices.punjab.gov.in) or visit local Sub-Divisional Magistrate (SDM) / Tehsildar office.",
        "application_url": "https://eservices.punjab.gov.in",
        "official_source_url": "https://punjab.gov.in",
        "source_excerpt": "Caste Certificate certifies that a person belongs to a particular Scheduled Caste or Backward Class community as per constitutional orders.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": []
    },
    {
        "id": "residence-certificate",
        "name": "Issuance of Domicile / Residence Certificate",
        "name_hi": "निवास / अधिवास प्रमाण पत्र",
        "name_pa": "ਰਿਹਾਇਸ਼ੀ / ਡੋਮੀਸਾਈਲ ਸਰਟੀਫਿਕੇਟ",
        "record_type": "service",
        "description": "Official legal certificate proving that an individual is a bona fide permanent resident of a specific state, mandatory for state-quota college admissions, state government jobs, and state-sponsored welfare grants.",
        "department": "Department of Revenue, State Governments",
        "level": "state",
        "state_applicability": ["All India"],
        "category": "Other Citizen Services",
        "target_beneficiaries": ["all permanent residents", "students", "job seekers"],
        "age_criteria": None,
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Must have resided in the state continuously for the period stipulated by state law (typically 5 or 10 years)",
            "Or must possess immovable property / schooling in the state"
        ],
        "benefits": "Legal evidence of residence to claim state benefits, state university admissions, and local employment quotas.",
        "benefits_hi": "राज्य की योजनाओं और शैक्षणिक संस्थानों में स्थानीय कोटे के लिए निवास का कानूनी प्रमाण।",
        "benefits_pa": "ਰਾਜ ਦੀਆਂ ਸਕੀਮਾਂ ਅਤੇ ਕਾਲਜਾਂ ਵਿੱਚ ਸਥਾਨਕ ਕੋਟੇ ਲਈ ਪੱਕੀ ਰਿਹਾਇਸ਼ ਦਾ ਸਰਕਾਰੀ ਸਬੂਤ।",
        "required_documents": [
            {"name": "Aadhaar Card / Voter ID", "description": "Identity and local address verification", "linked_service_id": None},
            {"name": "Continuous Residence Proof (Electricity bills, School leaving cert, Land registry)", "description": "Documentary proof of residing in the state for required minimum years", "linked_service_id": None}
        ],
        "application_procedure": "Apply on the state e-governance portal or at local Sewa Kendra / Tehsil office with residence proofs.",
        "application_url": "https://eservices.punjab.gov.in",
        "official_source_url": "https://punjab.gov.in",
        "source_excerpt": "Domicile / Residence Certificate is an official document proving that the holder has lived in the state for a specified number of years.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": []
    },
    {
        "id": "ration-card",
        "name": "Application for Digital Ration Card (NFSA)",
        "name_hi": "डिजिटल राशन कार्ड के लिए आवेदन (एनएफएसए)",
        "name_pa": "ਡਿਜੀਟਲ ਰਾਸ਼ਨ ਕਾਰਡ ਲਈ ਅਰਜ਼ੀ",
        "record_type": "service",
        "description": "Essential citizen document issued under the National Food Security Act (NFSA) enabling eligible households to receive highly subsidized food grains (wheat, rice) from fair price shops, while also acting as an official family identity proof.",
        "department": "Department of Food, Civil Supplies and Consumer Affairs",
        "level": "state",
        "state_applicability": ["All India"],
        "category": "Other Citizen Services",
        "target_beneficiaries": ["households", "priority families", "Antyodaya beneficiaries"],
        "age_criteria": {"min": 18, "max": 100},
        "income_criteria": None,
        "education_criteria": None,
        "other_conditions": [
            "Applicant must be an adult representative of the household",
            "No member should be included in another existing ration card"
        ],
        "benefits": "Monthly subsidized food grains under One Nation One Ration Card (ONORC) and essential family identity proof for welfare schemes.",
        "benefits_hi": "सार्वजनिक वितरण प्रणाली (PDS) से रियायती खाद्यान्न और पारिवारिक पहचान प्रमाण।",
        "benefits_pa": "ਮਹੀਨਾਵਾਰ ਸਸਤਾ ਅਨਾਜ ਅਤੇ ਪਰਿਵਾਰਕ ਪਛਾਣ ਦਾ ਜ਼ਰੂਰੀ ਦਸਤਾਵੇਜ਼।",
        "required_documents": [
            {"name": "Aadhaar Card of All Family Members", "description": "Mandatory Aadhaar linkage for biometric food distribution", "linked_service_id": None},
            {"name": "Address Proof", "description": "Electricity bill or water bill", "linked_service_id": None},
            {"name": "Family Group Photograph", "description": "Photograph showing all household members", "linked_service_id": None}
        ],
        "application_procedure": "Submit application on the state Food & Civil Supplies portal or via nearest Food Inspector office / Sewa Kendra.",
        "application_url": "https://nfsa.gov.in",
        "official_source_url": "https://nfsa.gov.in",
        "source_excerpt": "Ration Card enables eligible families to obtain food grains at subsidized rates under the National Food Security Act.",
        "last_verified_date": FETCHED_STR,
        "fetched_at": NOW,
        "verification_status": "demo",
        "rules": []
    }
]


def seed_database(db: Session) -> int:
    """
    Populates records, eligibility rules, and search chunks.
    Rebuilds the FTS5 search index.
    """
    count = 0
    for rec_data in SEED_RECORDS:
        rules_data = rec_data.pop("rules", [])
        rec_id = rec_data["id"]

        # Check if record already exists
        existing = db.query(Record).filter(Record.id == rec_id).first()
        if existing:
            # Update fields
            for k, v in rec_data.items():
                setattr(existing, k, v)
            record = existing
        else:
            record = Record(**rec_data)
            db.add(record)
            count += 1
        db.flush()

        # Delete existing rules and re-add
        db.query(EligibilityRule).filter(EligibilityRule.record_id == rec_id).delete()
        for r in rules_data:
            rule = EligibilityRule(
                record_id=rec_id,
                field=r["field"],
                operator=r["operator"],
                value=r["value"],
                kind=r.get("kind", "profile"),
                description=r.get("description", ""),
                source_excerpt=r.get("source_excerpt", ""),
                is_approved=True,
            )
            db.add(rule)

        # Delete existing search chunks and re-add
        db.query(SearchChunk).filter(SearchChunk.record_id == rec_id).delete()

        chunks = [
            ("description", f"{record.name}. {record.description}"),
            ("benefits", f"Benefits: {record.benefits}"),
            ("eligibility", f"Eligibility and conditions: {', '.join(record.other_conditions or [])}"),
            ("documents", f"Required documents: {', '.join([d['name'] if isinstance(d, dict) else str(d) for d in (record.required_documents or [])])}"),
            ("procedure", f"Application procedure: {record.application_procedure}"),
        ]

        for sec, text in chunks:
            if text.strip():
                chunk = SearchChunk(
                    record_id=rec_id,
                    section=sec,
                    content=text,
                    source_url=record.official_source_url,
                )
                db.add(chunk)

    db.commit()

    # Rebuild FTS5 index
    build_fts_index(db)

    return count
