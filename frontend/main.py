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
    
    org_name = st.text_input(
        "Organization Name",
        placeholder="e.g., Harvard University",
        help="Name of the organization to research"
    )
    
    role_title = st.text_input(
        "Role Title",
        placeholder="e.g., Chief Financial Officer",
        help="Job title/role to search for"
    )
    
    search_type = st.selectbox(
        "Search Type",
        ["Executive", "Academic", "Research", "Administrative", "General"],
        help="Type of search to perform"
    )
    
    st.divider()
    
    st.subheader("🎯 Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Fetch Bios", use_container_width=True, disabled=not org_name or not role_title):
            st.session_state.bios_data = fetch_bios(org_name, role_title)
            if st.session_state.bios_data:
                st.success(f"✓ Fetched {len(st.session_state.bios_data)} bios")
            else:
                st.warning("No bios found")
    
    with col2:
        if st.button("💼 Fetch Jobs", use_container_width=True, disabled=not role_title):
            st.session_state.jobs_data = fetch_jobs(role_title, search_type)
            if st.session_state.jobs_data:
                st.success(f"✓ Fetched {len(st.session_state.jobs_data)} jobs")
            else:
                st.warning("No jobs found")
    
    if st.button("📰 Fetch News", use_container_width=True, disabled=not org_name):
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
            
            # Export section
            if status.get("status") == "completed":
                st.success("✅ Workflow completed successfully!")
                
                if st.button("📥 Get Export Files"):
                    exports = get_export_urls(st.session_state.run_id)
                    if exports and "urls" in exports:
                        st.subheader("Download Files")
                        for file_type, url in exports["urls"].items():
                            st.markdown(f"[Download {file_type.upper()}]({url})")
        
        # Auto-refresh button
        if status and status.get("status") in ["pending", "running"]:
            if st.button("🔄 Refresh Status"):
                st.rerun()

st.divider()

# Tabs for data display
tab1, tab2, tab3 = st.tabs(["👥 People Bios", "💼 Job Postings", "📰 News Articles"])

with tab1:
    st.subheader("People Bios")
    if st.session_state.bios_data:
        df_bios = pd.DataFrame(st.session_state.bios_data)
        
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
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            csv_bios = edited_bios.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_bios,
                file_name=f"bios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No bios data available. Use the sidebar to fetch bios.")

with tab2:
    st.subheader("Job Postings")
    if st.session_state.jobs_data:
        df_jobs = pd.DataFrame(st.session_state.jobs_data)
        
        # Allow inline editing
        edited_jobs = st.data_editor(
            df_jobs,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            csv_jobs = edited_jobs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_jobs,
                file_name=f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No job postings available. Use the sidebar to fetch jobs.")

with tab3:
    st.subheader("News Articles")
    if st.session_state.news_data:
        df_news = pd.DataFrame(st.session_state.news_data)
        
        # Allow inline editing
        edited_news = st.data_editor(
            df_news,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "summary": st.column_config.TextColumn("Summary", width="large"),
                "tags": st.column_config.ListColumn("Tags"),
            }
        )
        
        # Export button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            csv_news = edited_news.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_news,
                file_name=f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("No news articles available. Use the sidebar to fetch news.")

# Footer
st.divider()
st.caption("Research Intelligence Platform v1.0 | POC")
