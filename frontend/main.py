import streamlit as st
import requests
import pandas as pd
import time
from typing import Dict, List, Optional
import os
from datetime import datetime

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Research Intelligence Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .status-running {
        color: #ff9800;
        font-weight: bold;
    }
    .status-completed {
        color: #4caf50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Predefined options for better UX
ORGANIZATIONS = [
    "Custom (type below)...",
    "Harvard University",
    "Stanford University",
    "MIT",
    "Yale University",
    "Princeton University",
    "Columbia University",
    "University of Chicago",
    "UC Berkeley",
    "University of Pennsylvania",
    "Duke University",
    "Goldman Sachs",
    "McKinsey & Company",
    "JP Morgan Chase",
    "Morgan Stanley",
    "Boston Consulting Group",
    "Deloitte",
    "Microsoft",
    "Amazon",
    "Google"
]

ROLE_TITLES = [
    "Custom (type below)...",
    "Chief Executive Officer",
    "Chief Financial Officer",
    "Chief Operating Officer",
    "Chief Technology Officer",
    "Chief Information Officer",
    "Chief Marketing Officer",
    "President",
    "Executive Vice President",
    "Vice President",
    "Provost",
    "Dean",
    "Chancellor",
    "Director"
]

SEARCH_PRESETS = {
    "University CFO Search": {
        "org_name": "Harvard University",
        "role_title": "Chief Financial Officer",
        "search_type": "Academic"
    },
    "Corporate Executive Search": {
        "org_name": "Goldman Sachs",
        "role_title": "Chief Executive Officer",
        "search_type": "Executive"
    },
    "Academic Leadership": {
        "org_name": "Stanford University",
        "role_title": "Provost",
        "search_type": "Academic"
    },
    "Tech Company CTO": {
        "org_name": "Microsoft",
        "role_title": "Chief Technology Officer",
        "search_type": "Executive"
    }
}

# Initialize session state
if 'run_id' not in st.session_state:
    st.session_state.run_id = None
if 'bios_data' not in st.session_state:
    st.session_state.bios_data = []
if 'jobs_data' not in st.session_state:
    st.session_state.jobs_data = []
if 'news_data' not in st.session_state:
    st.session_state.news_data = []
if 'workflow_status' not in st.session_state:
    st.session_state.workflow_status = None
if 'last_org' not in st.session_state:
    st.session_state.last_org = ""
if 'last_role' not in st.session_state:
    st.session_state.last_role = ""
if 'last_search_type' not in st.session_state:
    st.session_state.last_search_type = "Executive"
if 'use_dropdown_org' not in st.session_state:
    st.session_state.use_dropdown_org = True
if 'use_dropdown_role' not in st.session_state:
    st.session_state.use_dropdown_role = True

# Helper functions
def make_api_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Optional[Dict]:
    """Make API request to backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def fetch_bios(org_name: str, role_title: str) -> List[Dict]:
    """Fetch people bios from organization"""
    with st.spinner("Fetching bios from organization website..."):
        result = make_api_request("/bios", "POST", {
            "org_name": org_name,
            "role_title": role_title
        })
        if result and "bios" in result:
            return result["bios"]
        return []

def fetch_jobs(role_title: str, search_type: str) -> List[Dict]:
    """Fetch competing job searches"""
    with st.spinner("Fetching job postings..."):
        result = make_api_request("/jobs", "POST", {
            "role_title": role_title,
            "search_type": search_type
        })
        if result and "jobs" in result:
            return result["jobs"]
        return []

def fetch_news(org_name: str) -> List[Dict]:
    """Fetch and summarize news"""
    with st.spinner("Fetching news articles..."):
        result = make_api_request("/news", "POST", {
            "org_name": org_name
        })
        if result and "news" in result:
            return result["news"]
        return []

def trigger_workflow(org_name: str, role_title: str, search_type: str) -> Optional[str]:
    """Trigger complete workflow"""
    with st.spinner("Triggering complete workflow..."):
        result = make_api_request("/trigger", "POST", {
            "org_name": org_name,
            "role_title": role_title,
            "search_type": search_type
        })
        if result and "run_id" in result:
            return result["run_id"]
        return None

def get_workflow_status(run_id: str) -> Optional[Dict]:
    """Get status of workflow run"""
    result = make_api_request(f"/status/{run_id}")
    return result

def get_export_urls(run_id: str) -> Optional[Dict]:
    """Get export file URLs"""
    result = make_api_request(f"/exports/{run_id}")
    return result

# Main UI
st.markdown('<div class="main-header">🔍 Research Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Intelligence Gathering & Analysis</div>', unsafe_allow_html=True)

# Sidebar - Input Form
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Quick Presets
    with st.expander("🎯 Quick Presets", expanded=False):
        preset = st.selectbox(
            "Load a preset search",
            ["None"] + list(SEARCH_PRESETS.keys()),
            help="Select a pre-configured search to get started quickly"
        )
        if preset != "None" and st.button("Load Preset", use_container_width=True):
            preset_data = SEARCH_PRESETS[preset]
            st.session_state.last_org = preset_data["org_name"]
            st.session_state.last_role = preset_data["role_title"]
            st.session_state.last_search_type = preset_data["search_type"]
            st.rerun()
    
    st.divider()
    
    # Organization Name - Dropdown or Custom
    st.markdown("**Organization Name**")
    org_dropdown = st.selectbox(
        "Select organization",
        ORGANIZATIONS,
        index=0 if not st.session_state.last_org else (
            ORGANIZATIONS.index(st.session_state.last_org) 
            if st.session_state.last_org in ORGANIZATIONS 
            else 0
        ),
        label_visibility="collapsed",
        help="Select from list or choose 'Custom' to type your own"
    )
    
    if org_dropdown == "Custom (type below)...":
        org_name = st.text_input(
            "Custom organization name",
            value=st.session_state.last_org if st.session_state.last_org not in ORGANIZATIONS else "",
            placeholder="e.g., Your University Name",
            label_visibility="collapsed"
        )
    else:
        org_name = org_dropdown
    
    # Save last used
    if org_name:
        st.session_state.last_org = org_name
    
    st.markdown("---")
    
    # Role Title - Dropdown or Custom
    st.markdown("**Role Title**")
    role_dropdown = st.selectbox(
        "Select role",
        ROLE_TITLES,
        index=0 if not st.session_state.last_role else (
            ROLE_TITLES.index(st.session_state.last_role) 
            if st.session_state.last_role in ROLE_TITLES 
            else 0
        ),
        label_visibility="collapsed",
        help="Select from list or choose 'Custom' to type your own"
    )
    
    if role_dropdown == "Custom (type below)...":
        role_title = st.text_input(
            "Custom role title",
            value=st.session_state.last_role if st.session_state.last_role not in ROLE_TITLES else "",
            placeholder="e.g., Your Custom Role",
            label_visibility="collapsed"
        )
    else:
        role_title = role_dropdown
    
    # Save last used
    if role_title:
        st.session_state.last_role = role_title
    
    st.markdown("---")
    
    # Search Type
    search_type = st.selectbox(
        "Search Type",
        ["Executive", "Academic", "Research", "Administrative", "General"],
        index=["Executive", "Academic", "Research", "Administrative", "General"].index(
            st.session_state.last_search_type
        ) if st.session_state.last_search_type else 0,
        help="Type of search to perform"
    )
    
    # Save last used
    st.session_state.last_search_type = search_type
    
    st.divider()
    
    st.subheader("🎯 Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Fetch Bios", use_container_width=True, disabled=not org_name or not role_title, type="secondary"):
            st.session_state.bios_data = fetch_bios(org_name, role_title)
            if st.session_state.bios_data:
                st.success(f"✓ Fetched {len(st.session_state.bios_data)} bios")
            else:
                st.warning("No bios found")
    
    with col2:
        if st.button("💼 Fetch Jobs", use_container_width=True, disabled=not role_title, type="secondary"):
            st.session_state.jobs_data = fetch_jobs(role_title, search_type)
            if st.session_state.jobs_data:
                st.success(f"✓ Fetched {len(st.session_state.jobs_data)} jobs")
            else:
                st.warning("No jobs found")
    
    if st.button("📰 Fetch News", use_container_width=True, disabled=not org_name, type="secondary"):
        st.session_state.news_data = fetch_news(org_name)
        if st.session_state.news_data:
            st.success(f"✓ Fetched {len(st.session_state.news_data)} articles")
        else:
            st.warning("No news found")
    
    st.divider()
    
    if st.button("🚀 Trigger Complete Workflow", use_container_width=True, type="primary", disabled=not org_name or not role_title):
        run_id = trigger_workflow(org_name, role_title, search_type)
        if run_id:
            st.session_state.run_id = run_id
            st.success(f"✓ Workflow started! Run ID: {run_id[:8]}...")
        else:
            st.error("Failed to start workflow")
    
    # Clear button
    st.divider()
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.bios_data = []
        st.session_state.jobs_data = []
        st.session_state.news_data = []
        st.session_state.run_id = None
        st.success("✓ Cleared all data")
        st.rerun()

# Main content area
if st.session_state.run_id:
    st.header(f"📊 Workflow Status - Run ID: {st.session_state.run_id[:12]}...")
    
    # Auto-refresh status
    status_placeholder = st.empty()
    
    with status_placeholder.container():
        status = get_workflow_status(st.session_state.run_id)
        
        if status:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Overall Status", status.get("status", "Unknown").upper())
            with col2:
                st.metric("Bios Fetched", status.get("bios_count", 0))
            with col3:
                st.metric("Jobs Fetched", status.get("jobs_count", 0))
            with col4:
                st.metric("News Fetched", status.get("news_count", 0))
            
            # Module progress
            st.subheader("Module Progress")
            modules = status.get("modules", {})
            
            prog_col1, prog_col2, prog_col3 = st.columns(3)
            
            with prog_col1:
                bios_status = modules.get("bios", {}).get("status", "pending")
                st.markdown(f"**Bios Module:** {bios_status}")
                if bios_status == "completed":
                    st.progress(1.0)
                elif bios_status == "running":
                    st.progress(0.5)
                else:
                    st.progress(0.0)
            
            with prog_col2:
                jobs_status = modules.get("jobs", {}).get("status", "pending")
                st.markdown(f"**Jobs Module:** {jobs_status}")
                if jobs_status == "completed":
                    st.progress(1.0)
                elif jobs_status == "running":
                    st.progress(0.5)
                else:
                    st.progress(0.0)
            
            with prog_col3:
                news_status = modules.get("news", {}).get("status", "pending")
                st.markdown(f"**News Module:** {news_status}")
                if news_status == "completed":
                    st.progress(1.0)
                elif news_status == "running":
                    st.progress(0.5)
                else:
                    st.progress(0.0)
            
            # Auto-refresh if workflow is still running
            if status.get("status") in ["pending", "running"]:
                time.sleep(2)  # Wait 2 seconds before auto-refresh
                st.rerun()
            
            # Export section and fetch data when completed
            if status.get("status") == "completed":
                st.success("✅ Workflow completed successfully!")
                
                # Automatically fetch all workflow data in a single API call
                if not st.session_state.bios_data and not st.session_state.jobs_data and not st.session_state.news_data:
                    with st.spinner("Loading workflow data..."):
                        # Use the new endpoint to get all data at once
                        result = make_api_request(f"/workflows/{st.session_state.run_id}/data", "GET")
                        if result and "data" in result:
                            workflow_data = result["data"]
                            
                            # Update session state with all data
                            if workflow_data.get("bios"):
                                st.session_state.bios_data = workflow_data["bios"]
                            if workflow_data.get("jobs"):
                                st.session_state.jobs_data = workflow_data["jobs"]
                            if workflow_data.get("news"):
                                st.session_state.news_data = workflow_data["news"]
                            
                            st.success("✨ Data loaded successfully! Check the tabs below.")
                
                st.info("💡 **Tip:** Scroll down to see the data in the tabs below!")
                
                if st.button("📥 Get Export Files"):
                    exports = get_export_urls(st.session_state.run_id)
                    if exports and "urls" in exports:
                        st.subheader("Download Files")
                        for file_type, url in exports["urls"].items():
                            st.markdown(f"[Download {file_type.upper()}]({url})")

st.divider()

# Tabs for data display
tab1, tab2, tab3 = st.tabs(["👥 People Bios", "💼 Job Postings", "📰 News Articles"])

with tab1:
    st.subheader("People Bios")
    if st.session_state.bios_data:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Bios", len(st.session_state.bios_data))
        with col2:
            orgs = set(bio.get('organization', 'Unknown') for bio in st.session_state.bios_data)
            st.metric("Organizations", len(orgs))
        with col3:
            avg_tenure = sum(int(bio.get('tenure', '0 years').split()[0]) for bio in st.session_state.bios_data) / len(st.session_state.bios_data)
            st.metric("Avg Tenure", f"{avg_tenure:.1f} years")
        
        st.divider()
        
        df_bios = pd.DataFrame(st.session_state.bios_data)
        
        # Filter options
        with st.expander("🔍 Filter Options", expanded=False):
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                if 'organization' in df_bios.columns:
                    orgs_filter = st.multiselect(
                        "Filter by Organization",
                        options=df_bios['organization'].unique().tolist(),
                        default=None
                    )
                    if orgs_filter:
                        df_bios = df_bios[df_bios['organization'].isin(orgs_filter)]
            
            with filter_col2:
                if 'title' in df_bios.columns:
                    title_filter = st.multiselect(
                        "Filter by Title",
                        options=df_bios['title'].unique().tolist(),
                        default=None
                    )
                    if title_filter:
                        df_bios = df_bios[df_bios['title'].isin(title_filter)]
        
        # Display options
        display_mode = st.radio(
            "Display Mode",
            ["Table View", "Card View"],
            horizontal=True,
            help="Choose how to display the data"
        )
        
        if display_mode == "Table View":
            # Allow inline editing
            edited_bios = st.data_editor(
                df_bios,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "headshot": st.column_config.ImageColumn("Photo", width="small"),
                    "bio_short": st.column_config.TextColumn("Short Bio", width="medium"),
                    "bio_long": st.column_config.TextColumn("Full Bio", width="large"),
                }
            )
        else:
            # Card view
            for idx, bio in enumerate(st.session_state.bios_data):
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if bio.get('headshot'):
                            st.image(bio['headshot'], width=100)
                    with col2:
                        st.markdown(f"### {bio.get('name', 'Unknown')}")
                        st.markdown(f"**{bio.get('title', 'N/A')}** at {bio.get('organization', 'N/A')}")
                        st.markdown(f"⏱️ Tenure: {bio.get('tenure', 'N/A')}")
                        if bio.get('bio_short'):
                            st.markdown(bio['bio_short'])
                        with st.expander("View Full Bio"):
                            st.markdown(bio.get('bio_long', 'No detailed bio available'))
                            if bio.get('education'):
                                st.markdown("**Education:**")
                                for edu in bio.get('education', []):
                                    st.markdown(f"- {edu}")
                    st.divider()
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            csv_bios = df_bios.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_bios,
                file_name=f"bios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("Email functionality coming soon!")
    else:
        st.info("📋 No bios data available. Use the sidebar to fetch bios or trigger a complete workflow.")
        st.markdown("**Tip:** Try using one of the Quick Presets for a fast start!")

with tab2:
    st.subheader("Job Postings")
    if st.session_state.jobs_data:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Jobs", len(st.session_state.jobs_data))
        with col2:
            orgs = set(job.get('organization', 'Unknown') for job in st.session_state.jobs_data)
            st.metric("Organizations", len(orgs))
        with col3:
            boards = set(job.get('job_board', 'Unknown') for job in st.session_state.jobs_data)
            st.metric("Job Boards", len(boards))
        with col4:
            locations = set(job.get('location', 'Unknown') for job in st.session_state.jobs_data)
            st.metric("Locations", len(locations))
        
        st.divider()
        
        df_jobs = pd.DataFrame(st.session_state.jobs_data)
        
        # Filter options
        with st.expander("🔍 Filter Options", expanded=False):
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            with filter_col1:
                if 'organization' in df_jobs.columns:
                    orgs_filter = st.multiselect(
                        "Filter by Organization",
                        options=df_jobs['organization'].unique().tolist(),
                        default=None
                    )
                    if orgs_filter:
                        df_jobs = df_jobs[df_jobs['organization'].isin(orgs_filter)]
            
            with filter_col2:
                if 'location' in df_jobs.columns:
                    loc_filter = st.multiselect(
                        "Filter by Location",
                        options=df_jobs['location'].unique().tolist(),
                        default=None
                    )
                    if loc_filter:
                        df_jobs = df_jobs[df_jobs['location'].isin(loc_filter)]
            
            with filter_col3:
                if 'job_board' in df_jobs.columns:
                    board_filter = st.multiselect(
                        "Filter by Job Board",
                        options=df_jobs['job_board'].unique().tolist(),
                        default=None
                    )
                    if board_filter:
                        df_jobs = df_jobs[df_jobs['job_board'].isin(board_filter)]
        
        # Allow inline editing
        edited_jobs = st.data_editor(
            df_jobs,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "url": st.column_config.LinkColumn("Job Link"),
                "description": st.column_config.TextColumn("Description", width="large"),
            }
        )
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            csv_jobs = df_jobs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_jobs,
                file_name=f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            if st.button("📧 Email Report", use_container_width=True, key="email_jobs"):
                st.info("Email functionality coming soon!")
    else:
        st.info("💼 No job postings available. Use the sidebar to fetch jobs or trigger a complete workflow.")
        st.markdown("**Tip:** Select a role title from the dropdown to get started!")

with tab3:
    st.subheader("News Articles")
    if st.session_state.news_data:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Articles", len(st.session_state.news_data))
        with col2:
            categories = set(article.get('category', 'Unknown') for article in st.session_state.news_data)
            st.metric("Categories", len(categories))
        with col3:
            sources = set(article.get('source', 'Unknown') for article in st.session_state.news_data)
            st.metric("Sources", len(sources))
        
        st.divider()
        
        df_news = pd.DataFrame(st.session_state.news_data)
        
        # Filter options
        with st.expander("🔍 Filter Options", expanded=False):
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                if 'category' in df_news.columns:
                    cat_filter = st.multiselect(
                        "Filter by Category",
                        options=df_news['category'].unique().tolist(),
                        default=None
                    )
                    if cat_filter:
                        df_news = df_news[df_news['category'].isin(cat_filter)]
            
            with filter_col2:
                if 'source' in df_news.columns:
                    source_filter = st.multiselect(
                        "Filter by Source",
                        options=df_news['source'].unique().tolist(),
                        default=None
                    )
                    if source_filter:
                        df_news = df_news[df_news['source'].isin(source_filter)]
        
        # Display mode
        display_mode = st.radio(
            "Display Mode",
            ["Table View", "Article View"],
            horizontal=True,
            help="Choose how to display the news",
            key="news_display"
        )
        
        if display_mode == "Table View":
            # Allow inline editing
            edited_news = st.data_editor(
                df_news,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "url": st.column_config.LinkColumn("Article Link"),
                    "summary": st.column_config.TextColumn("Summary", width="large"),
                }
            )
        else:
            # Article view
            for idx, article in enumerate(st.session_state.news_data):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"### [{article.get('title', 'Untitled')}]({article.get('url', '#')})")
                    with col2:
                        category_color = {
                            'Leadership Change': '🟦',
                            'Financial': '🟩',
                            'Scandal': '🟥',
                            'Achievement': '🟨',
                            'Partnership': '🟪'
                        }
                        cat = article.get('category', 'General')
                        st.markdown(f"{category_color.get(cat, '⬜')} {cat}")
                    
                    st.markdown(f"**{article.get('source', 'Unknown Source')}** • {article.get('published_date', 'Date unknown')}")
                    st.markdown(article.get('summary', 'No summary available'))
                    
                    if article.get('tags'):
                        tags_str = " ".join([f"`{tag}`" for tag in article.get('tags', [])])
                        st.markdown(f"**Tags:** {tags_str}")
                    
                    st.divider()
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            csv_news = df_news.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_news,
                file_name=f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            if st.button("📧 Email Report", use_container_width=True, key="email_news"):
                st.info("Email functionality coming soon!")
    else:
        st.info("📰 No news articles available. Use the sidebar to fetch news or trigger a complete workflow.")
        st.markdown("**Tip:** Enter an organization name to search for related news!")

# Footer
st.divider()
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.caption("Research Intelligence Platform v1.0 | POC")
with col2:
    if st.session_state.bios_data or st.session_state.jobs_data or st.session_state.news_data:
        total_records = len(st.session_state.bios_data) + len(st.session_state.jobs_data) + len(st.session_state.news_data)
        st.caption(f"📊 Total Records: {total_records}")
with col3:
    if st.button("ℹ️ Help"):
        st.info("""
        **Quick Start Guide:**
        1. Select or enter an organization and role
        2. Choose a search type
        3. Click a fetch button or trigger workflow
        4. Review and edit data in tabs
        5. Download as CSV
        
        **Tips:**
        - Use Quick Presets for common searches
        - Filter data using the filter options
        - Switch between table and card views
        - Your last search is saved automatically
        """)
