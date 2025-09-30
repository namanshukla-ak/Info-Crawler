"""
Synthetic data generator for POC testing
Generates realistic fake data for bios, jobs, and news
"""
from faker import Faker
import random
from typing import List, Dict
from datetime import datetime, timedelta

fake = Faker()

# Predefined data pools for realistic generation
UNIVERSITIES = [
    "Harvard University", "Stanford University", "MIT", "Yale University",
    "Princeton University", "Columbia University", "University of Chicago",
    "UC Berkeley", "University of Pennsylvania", "Duke University",
    "Northwestern University", "Johns Hopkins University", "Dartmouth College",
    "Cornell University", "Brown University", "Vanderbilt University",
    "Rice University", "Notre Dame University", "Georgetown University"
]

COMPANIES = [
    "Goldman Sachs", "McKinsey & Company", "Boston Consulting Group",
    "Bain & Company", "JP Morgan Chase", "Morgan Stanley", "Deloitte",
    "PwC", "EY", "KPMG", "Accenture", "IBM", "Microsoft", "Amazon",
    "Google", "Meta", "Apple", "Tesla", "SpaceX", "Salesforce"
]

EXECUTIVE_TITLES = [
    "Chief Executive Officer", "Chief Financial Officer", "Chief Operating Officer",
    "Chief Technology Officer", "Chief Information Officer", "Chief Marketing Officer",
    "Chief Human Resources Officer", "Chief Strategy Officer", "Chief Legal Officer",
    "President", "Executive Vice President", "Senior Vice President",
    "Vice President of Operations", "Vice President of Finance"
]

ACADEMIC_TITLES = [
    "President", "Provost", "Dean of Faculty", "Dean of Students",
    "Vice President for Academic Affairs", "Vice President for Research",
    "Vice President for Finance", "Chancellor", "Rector",
    "Chief Academic Officer", "Chief Financial Officer"
]

JOB_BOARDS = [
    "LinkedIn", "Indeed", "Glassdoor", "HigherEdJobs", "Chronicle Vitae",
    "Academic Keys", "InsideHigherEd", "Monster", "CareerBuilder"
]

NEWS_SOURCES = [
    "The Chronicle of Higher Education", "Inside Higher Ed", "Forbes",
    "Bloomberg", "Wall Street Journal", "Financial Times", "Reuters",
    "Associated Press", "The New York Times", "Washington Post"
]

NEWS_CATEGORIES = [
    "Leadership Change", "Organizational Development", "Financial",
    "Scandal", "General", "Achievement", "Partnership", "Expansion"
]

LOCATIONS = [
    "New York, NY", "Boston, MA", "San Francisco, CA", "Chicago, IL",
    "Washington, DC", "Los Angeles, CA", "Seattle, WA", "Austin, TX",
    "Philadelphia, PA", "Atlanta, GA", "Denver, CO", "Miami, FL"
]


def generate_person_bio(org_name: str = None, role_title: str = None) -> Dict:
    """
    Generate a realistic person bio
    
    Args:
        org_name: Organization name (optional)
        role_title: Role title (optional)
        
    Returns:
        Bio dictionary
    """
    # Determine organization type
    is_academic = org_name and "university" in org_name.lower() if org_name else random.choice([True, False])
    
    # Select appropriate title
    if role_title:
        title = role_title
    elif is_academic:
        title = random.choice(ACADEMIC_TITLES)
    else:
        title = random.choice(EXECUTIVE_TITLES)
    
    # Select organization
    if not org_name:
        org_name = random.choice(UNIVERSITIES if is_academic else COMPANIES)
    
    # Generate person details
    name = fake.name()
    tenure_years = random.randint(1, 15)
    
    # Generate education background
    degrees = []
    for _ in range(random.randint(2, 4)):
        degree = random.choice(["BA", "BS", "MA", "MS", "MBA", "PhD", "JD", "MD"])
        field = random.choice([
            "Economics", "Business Administration", "Finance", "Computer Science",
            "Engineering", "Political Science", "Mathematics", "Physics", "Law",
            "Medicine", "Education", "Public Policy"
        ])
        university = random.choice(UNIVERSITIES)
        degrees.append(f"{degree} in {field} from {university}")
    
    # Generate career highlights
    previous_roles = []
    for _ in range(random.randint(2, 4)):
        prev_org = random.choice(UNIVERSITIES if is_academic else COMPANIES)
        prev_title = random.choice(ACADEMIC_TITLES if is_academic else EXECUTIVE_TITLES)
        years = random.randint(2, 10)
        previous_roles.append(f"{prev_title} at {prev_org} ({years} years)")
    
    # Generate bio
    bio_short = f"{name} serves as {title} at {org_name}, bringing over {tenure_years + 10} years of leadership experience in {'higher education' if is_academic else 'corporate management'}."
    
    bio_long = f"""{name} is the {title} at {org_name}, where {'they have' if tenure_years > 1 else 'they recently began'} leading the institution's strategic initiatives and operational excellence.

Education: {'; '.join(degrees[:2])}

Prior to joining {org_name}, {name.split()[0]} held several key leadership positions including {previous_roles[0]} and {previous_roles[1] if len(previous_roles) > 1 else 'various senior roles'}.

{name.split()[0]} has been recognized for {'innovative approaches to academic administration' if is_academic else 'driving organizational transformation and financial performance'}. {'They serve' if random.choice([True, False]) else 'They have served'} on multiple boards and advisory committees, contributing expertise in {'educational leadership' if is_academic else 'business strategy'} and governance.

Notable achievements include {'increasing research funding by ' + str(random.randint(20, 50)) + '%' if is_academic else 'growing revenue by ' + str(random.randint(15, 45)) + '%'}, {'improving student outcomes' if is_academic else 'expanding market presence'}, and fostering a culture of {'academic excellence' if is_academic else 'innovation and collaboration'}.
"""
    
    return {
        "name": name,
        "title": title,
        "organization": org_name,
        "bio_short": bio_short,
        "bio_long": bio_long,
        "headshot": f"https://i.pravatar.cc/150?u={fake.uuid4()}",
        "tenure": f"{tenure_years} years",
        "email": fake.email(),
        "education": degrees[:2],
        "previous_positions": previous_roles[:3]
    }


def generate_job_posting(role_title: str = None, search_type: str = "General") -> Dict:
    """
    Generate a realistic job posting
    
    Args:
        role_title: Job title (optional)
        search_type: Type of search (Executive, Academic, etc.)
        
    Returns:
        Job posting dictionary
    """
    is_academic = search_type == "Academic"
    
    # Select title
    if role_title:
        title = role_title
    elif is_academic:
        title = random.choice(ACADEMIC_TITLES)
    else:
        title = random.choice(EXECUTIVE_TITLES)
    
    # Select organization
    org = random.choice(UNIVERSITIES if is_academic else COMPANIES)
    
    # Generate posting details
    posted_days_ago = random.randint(1, 60)
    posted_date = (datetime.now() - timedelta(days=posted_days_ago)).isoformat()
    
    salary_min = random.randint(120, 250) * 1000
    salary_max = salary_min + random.randint(50, 150) * 1000
    salary_range = f"${salary_min:,} - ${salary_max:,}"
    
    # Generate description
    requirements = []
    for _ in range(random.randint(5, 8)):
        req = random.choice([
            f"{random.randint(10, 20)}+ years of leadership experience",
            "Proven track record of strategic planning and execution",
            "Strong financial acumen and budget management skills",
            "Excellent communication and interpersonal skills",
            "Experience managing large, diverse teams",
            "Advanced degree (Master's or PhD) required",
            "Experience in higher education administration" if is_academic else "Corporate leadership experience",
            "Change management expertise",
            "Board-level presentation experience"
        ])
        if req not in requirements:
            requirements.append(req)
    
    responsibilities = []
    for _ in range(random.randint(4, 7)):
        resp = random.choice([
            "Lead strategic planning and institutional development",
            "Oversee financial operations and resource allocation",
            "Build and maintain relationships with key stakeholders",
            "Drive organizational excellence and innovation",
            "Ensure compliance with regulatory requirements",
            "Develop and mentor senior leadership team",
            "Represent the organization to external constituencies",
            "Foster a culture of collaboration and accountability"
        ])
        if resp not in responsibilities:
            responsibilities.append(resp)
    
    description = f"""
{org} is seeking an exceptional leader to serve as {title}.

Key Responsibilities:
{chr(10).join([f'• {r}' for r in responsibilities])}

Qualifications:
{chr(10).join([f'• {r}' for r in requirements])}

About {org}:
{org} is a {'leading institution of higher education' if is_academic else 'premier organization'} committed to {'academic excellence and student success' if is_academic else 'innovation and market leadership'}.
"""
    
    return {
        "title": title,
        "organization": org,
        "location": random.choice(LOCATIONS),
        "posted_date": posted_date,
        "salary_range": salary_range,
        "job_board": random.choice(JOB_BOARDS),
        "url": f"https://{random.choice(JOB_BOARDS).lower().replace(' ', '')}.com/jobs/{fake.uuid4()}",
        "description": description.strip(),
        "employment_type": random.choice(["Full-time", "Full-time, Executive"]),
        "application_deadline": (datetime.now() + timedelta(days=random.randint(30, 90))).isoformat()
    }


def generate_news_article(org_name: str = None) -> Dict:
    """
    Generate a realistic news article
    
    Args:
        org_name: Organization name (optional)
        
    Returns:
        News article dictionary
    """
    if not org_name:
        org_name = random.choice(UNIVERSITIES + COMPANIES)
    
    category = random.choice(NEWS_CATEGORIES)
    
    # Generate title based on category
    title_templates = {
        "Leadership Change": [
            f"{org_name} Appoints New {random.choice(EXECUTIVE_TITLES)}",
            f"{org_name} Announces Leadership Transition",
            f"New {random.choice(EXECUTIVE_TITLES)} Named at {org_name}"
        ],
        "Financial": [
            f"{org_name} Reports Strong Financial Performance",
            f"{org_name} Secures ${random.randint(10, 500)}M in Funding",
            f"{org_name} Announces Budget Expansion"
        ],
        "Organizational Development": [
            f"{org_name} Launches Strategic Initiative",
            f"{org_name} Expands Operations",
            f"{org_name} Announces Organizational Restructuring"
        ],
        "Scandal": [
            f"{org_name} Faces Investigation",
            f"Controversy Surrounds {org_name} Leadership",
            f"{org_name} Responds to Allegations"
        ],
        "Achievement": [
            f"{org_name} Receives Prestigious Recognition",
            f"{org_name} Achieves Milestone",
            f"{org_name} Ranks Among Top Organizations"
        ],
        "Partnership": [
            f"{org_name} Announces Strategic Partnership",
            f"{org_name} Collaborates with Leading Organization",
            f"{org_name} Forms Alliance"
        ]
    }
    
    title = random.choice(title_templates.get(category, [f"Breaking News: {org_name}"]))
    
    # Generate article content
    published_days_ago = random.randint(1, 90)
    published_date = (datetime.now() - timedelta(days=published_days_ago)).isoformat()
    
    # Generate summary (2-3 sentences)
    summaries = {
        "Leadership Change": f"{org_name} has announced the appointment of a new senior executive to lead key strategic initiatives. The transition comes as part of the organization's long-term succession planning.",
        "Financial": f"{org_name} reported strong financial results for the fiscal year, exceeding expectations. The organization announced plans to reinvest in strategic priorities and infrastructure.",
        "Organizational Development": f"{org_name} unveiled a comprehensive plan to enhance organizational capabilities and expand its impact. The initiative includes investments in technology, personnel, and infrastructure.",
        "Scandal": f"{org_name} is addressing recent allegations and has launched an internal investigation. Leadership has committed to transparency and corrective measures.",
        "Achievement": f"{org_name} has been recognized for outstanding performance and innovation. The accolade reflects years of dedication to excellence and impact.",
        "Partnership": f"{org_name} has entered into a strategic partnership to enhance capabilities and reach. The collaboration will benefit multiple stakeholders and advance shared goals."
    }
    
    summary = summaries.get(category, f"{org_name} made significant announcements regarding organizational developments. The news has garnered attention from stakeholders and industry observers.")
    
    # Generate tags
    tag_pool = {
        "Leadership Change": ["leadership", "appointments", "executive", "transition"],
        "Financial": ["finance", "budget", "funding", "revenue"],
        "Organizational Development": ["strategy", "growth", "expansion", "development"],
        "Scandal": ["investigation", "controversy", "governance", "accountability"],
        "Achievement": ["recognition", "awards", "achievement", "excellence"],
        "Partnership": ["partnership", "collaboration", "alliance", "cooperation"]
    }
    
    tags = random.sample(tag_pool.get(category, ["news", "update"]), k=min(3, len(tag_pool.get(category, []))))
    tags.append(category.lower().replace(" ", "_"))
    
    return {
        "title": title,
        "source": random.choice(NEWS_SOURCES),
        "published_date": published_date,
        "url": f"https://{fake.domain_name()}/news/{fake.uuid4()}",
        "summary": summary,
        "category": category,
        "tags": tags,
        "author": fake.name(),
        "read_time": f"{random.randint(2, 8)} min read"
    }


def generate_bios(org_name: str, role_title: str, count: int = 8) -> List[Dict]:
    """Generate multiple person bios"""
    return [generate_person_bio(org_name, role_title) for _ in range(count)]


def generate_jobs(role_title: str, search_type: str, count: int = 15) -> List[Dict]:
    """Generate multiple job postings"""
    return [generate_job_posting(role_title, search_type) for _ in range(count)]


def generate_news(org_name: str, count: int = 12) -> List[Dict]:
    """Generate multiple news articles"""
    return [generate_news_article(org_name) for _ in range(count)]
