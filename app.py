import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from database import *

# Page configuration
st.set_page_config(
    page_title="Structura CEMS - Construction Management System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_database()
seed_sample_data()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = None
if 'edit_data' not in st.session_state:
    st.session_state.edit_data = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.875rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-critical { background: #fee; color: #c00; }
    .badge-major { background: #fef3c7; color: #92400e; }
    .badge-minor { background: #dbeafe; color: #1e40af; }
    .badge-open { background: #fed7aa; color: #9b3412; }
    .badge-resolved { background: #d1fae5; color: #065f46; }
    .badge-in-progress { background: #e0e7ff; color: #3730a3; }
    
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #5a67d8;
        transform: translateY(-1px);
    }
    
    div[data-testid="stForm"] {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    
    .user-info {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============ AUTHENTICATION PAGES ============
def login_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🏗️ Structura CEMS</h1>
        <p>Construction Engineering Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.markdown("### 🔐 Login")
                username = st.text_input("Username or Email", placeholder="Enter your username or email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col1, col2 = st.columns(2)
                with col1:
                    login_btn = st.form_submit_button("Login", use_container_width=True)
                with col2:
                    if st.form_submit_button("Sign Up", use_container_width=True):
                        st.session_state.show_signup = True
                        st.rerun()
                
                if login_btn:
                    if username and password:
                        user = authenticate_user(username, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = dict(user)
                            add_activity("User Login", f"User {user['username']} logged in", user['role'], user['full_name'])
                            st.success(f"Welcome back, {user['full_name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.warning("Please enter both username and password")
    
    if st.session_state.show_signup:
        signup_page()

def signup_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>📝 Create New Account</h1>
        <p>Join Structura CEMS</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("signup_form"):
                st.markdown("### 👤 Personal Information")
                full_name = st.text_input("Full Name*", placeholder="Enter your full name")
                email = st.text_input("Email*", placeholder="your@email.com")
                
                st.markdown("### 🔐 Account Information")
                username = st.text_input("Username*", placeholder="Choose a username")
                password = st.text_input("Password*", type="password", placeholder="Choose a password")
                confirm_password = st.text_input("Confirm Password*", type="password", placeholder="Confirm your password")
                
                st.markdown("### 💼 Professional Information")
                role = st.selectbox("Role", ["viewer", "architect", "engineer", "worker", "project_manager"])
                department = st.selectbox("Department", ["Management", "Design", "Structural", "Construction", "Quality Control", "Safety"])
                
                col1, col2 = st.columns(2)
                with col1:
                    signup_btn = st.form_submit_button("Create Account", use_container_width=True)
                with col2:
                    if st.form_submit_button("Back to Login", use_container_width=True):
                        st.session_state.show_signup = False
                        st.rerun()
                
                if signup_btn:
                    if not all([full_name, email, username, password, confirm_password]):
                        st.error("Please fill in all required fields (*)")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(username, email, password, full_name, role, department)
                        if success:
                            st.success("Account created successfully! Please login.")
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error(message)

def logout():
    if st.session_state.user:
        add_activity("User Logout", f"User {st.session_state.user['username']} logged out", 
                    st.session_state.user['role'], st.session_state.user['full_name'])
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.current_page = 'Dashboard'
    st.rerun()

# ============ USER PROFILE PAGE ============
def profile_page():
    st.markdown('<div class="main-header"><h1>👤 My Profile</h1><p>Manage your account settings</p></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="user-info">
            <h3>{user['full_name']}</h3>
            <p>@{user['username']}</p>
            <p><strong>Role:</strong> {user['role'].replace('_', ' ').title()}</p>
            <p><strong>Department:</strong> {user['department']}</p>
            <p><strong>Email:</strong> {user['email']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        tab1, tab2 = st.tabs(["📝 Edit Profile", "🔒 Change Password"])
        
        with tab1:
            with st.form("edit_profile_form"):
                full_name = st.text_input("Full Name", value=user['full_name'])
                email = st.text_input("Email", value=user['email'])
                department = st.text_input("Department", value=user['department'])
                
                if st.form_submit_button("Update Profile"):
                    update_user_profile(user['id'], full_name, email, department)
                    st.session_state.user['full_name'] = full_name
                    st.session_state.user['email'] = email
                    st.session_state.user['department'] = department
                    st.success("Profile updated successfully!")
                    st.rerun()
        
        with tab2:
            with st.form("change_password_form"):
                old_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Change Password"):
                    if not all([old_password, new_password, confirm_password]):
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = change_password(user['id'], old_password, new_password)
                        if success:
                            st.success(message)
                            st.balloons()
                        else:
                            st.error(message)

# ============ ADMIN PANEL ============
def admin_panel():
    st.markdown('<div class="main-header"><h1>⚙️ Admin Panel</h1><p>User management and system settings</p></div>', unsafe_allow_html=True)
    
    if st.session_state.user['role'] != 'admin':
        st.error("You don't have permission to access this page.")
        return
    
    tab1, tab2 = st.tabs(["👥 User Management", "📊 System Stats"])
    
    with tab1:
        st.markdown('<div class="section-title">All Users</div>', unsafe_allow_html=True)
        
        users = get_all_users()
        
        for user in users:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 1.5, 1])
                
                with col1:
                    st.markdown(f"**{user['full_name']}**")
                    st.caption(f"@{user['username']}")
                
                with col2:
                    st.caption(user['email'])
                    st.caption(f"Role: {user['role']}")
                
                with col3:
                    st.caption(f"Dept: {user['department']}")
                
                with col4:
                    status = "🟢 Active" if user['is_active'] else "🔴 Inactive"
                    st.caption(status)
                    if user['last_login']:
                        st.caption(f"Last login: {user['last_login'][:10]}")
                
                with col5:
                    if user['id'] != st.session_state.user['id']:
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("🔧", key=f"toggle_{user['id']}"):
                                update_user_status(user['id'], 0 if user['is_active'] else 1)
                                st.rerun()
                        with col_b:
                            if st.button("🗑️", key=f"delete_{user['id']}"):
                                delete_user(user['id'])
                                st.rerun()
                
                st.divider()
    
    with tab2:
        stats = get_dashboard_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", stats['total_users'])
        with col2:
            st.metric("Active Projects", stats['active_projects'])
        with col3:
            st.metric("Total Budget", f"${stats['total_budget']:,.0f}")

# ============ DASHBOARD ============
def render_dashboard():
    st.markdown('<div class="main-header"><h1>📊 Project Dashboard</h1><p>Real-time project insights and metrics</p></div>', unsafe_allow_html=True)
    
    stats = get_dashboard_stats()
    
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div>🏢</div>
            <div class="metric-value">{stats['active_projects']}</div>
            <div class="metric-label">Active Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div>📋</div>
            <div class="metric-value">{stats['open_rfis']}</div>
            <div class="metric-label">Open RFIs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div>⚠️</div>
            <div class="metric-value">{stats['critical_defects']}</div>
            <div class="metric-label">Critical Defects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div>✅</div>
            <div class="metric-value">{stats['pending_tasks']}</div>
            <div class="metric-label">Pending Tasks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div>👥</div>
            <div class="metric-value">{stats['total_users']}</div>
            <div class="metric-label">Team Members</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Budget Summary
    budget_items = get_budget_summary()
    if budget_items:
        total_allocated = sum(item['budget_allocated'] for item in budget_items)
        total_spent = sum(item['amount_spent'] for item in budget_items)
        percent_spent = (total_spent / total_allocated * 100) if total_allocated > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Budget", f"${total_allocated:,.0f}")
        with col2:
            st.metric("Total Spent", f"${total_spent:,.0f}")
        with col3:
            st.metric("Budget Used", f"{percent_spent:.0f}%")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">📈 Progress Trend</div>', unsafe_allow_html=True)
        progress_data = get_progress_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=progress_data['weeks'],
            y=progress_data['planned'],
            mode='lines+markers',
            name='Planned',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=progress_data['weeks'],
            y=progress_data['actual'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='#48bb78', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(height=350, hovermode='x unified', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-title">💰 Budget Allocation</div>', unsafe_allow_html=True)
        if budget_items:
            budget_df = pd.DataFrame([
                {'Category': item['category'], 'Allocated': item['budget_allocated'], 'Spent': item['amount_spent']}
                for item in budget_items
            ])
            fig = go.Figure(data=[
                go.Bar(name='Allocated', x=budget_df['Category'], y=budget_df['Allocated'], marker_color='#667eea'),
                go.Bar(name='Spent', x=budget_df['Category'], y=budget_df['Spent'], marker_color='#48bb78')
            ])
            fig.update_layout(barmode='group', height=350, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity
    st.markdown('<div class="section-title">📝 Recent Activity</div>', unsafe_allow_html=True)
    activities = get_recent_activities()
    for activity in activities:
        st.info(f"**{activity['activity_type']}** - {activity['description']}  \n*by {activity['user_name']} ({activity['user_role']})*")

# ============ PROJECTS CRUD ============
def render_projects():
    st.markdown('<div class="main-header"><h1>🏗️ Project Management</h1><p>Create, update, and manage construction projects</p></div>', unsafe_allow_html=True)
    
    # Add Project Form
    with st.expander("➕ Add New Project", expanded=False):
        with st.form("add_project_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Project Name*", placeholder="Enter project name")
                location = st.text_input("Location", placeholder="City, District")
            with col2:
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
            
            if st.form_submit_button("Create Project"):
                if name:
                    add_project(name, location, start_date.isoformat(), end_date.isoformat(), st.session_state.user['username'])
                    add_activity("Project Created", f"New project '{name}' created", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success(f"✅ Project '{name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Project name is required")
    
    # Projects List
    st.markdown('<div class="section-title">📋 All Projects</div>', unsafe_allow_html=True)
    
    projects = get_all_projects()
    
    if projects:
        for project in projects:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{project['name']}**")
                    st.caption(project['location'] or "No location set")
                
                with col2:
                    st.progress(project['progress'] / 100, text=f"{project['progress']}% Complete")
                
                with col3:
                    status_color = "green" if project['status'] == 'Active' else "orange"
                    st.markdown(f"<span class='badge' style='background:#{status_color}20; color:{status_color}'>{project['status']}</span>", unsafe_allow_html=True)
                
                with col4:
                    if st.button("✏️ Edit", key=f"edit_project_{project['id']}"):
                        st.session_state.edit_mode = ('project', dict(project))
                        st.rerun()
                
                with col5:
                    if st.button("🗑️ Delete", key=f"delete_project_{project['id']}"):
                        delete_project(project['id'])
                        add_activity("Project Deleted", f"Project '{project['name']}' deleted", st.session_state.user['role'], st.session_state.user['full_name'])
                        st.warning(f"⚠️ Project '{project['name']}' deleted")
                        st.rerun()
                
                st.divider()
    
    # Edit Modal
    if st.session_state.edit_mode and st.session_state.edit_mode[0] == 'project':
        project = st.session_state.edit_mode[1]
        st.markdown("---")
        st.subheader(f"✏️ Edit Project: {project['name']}")
        
        with st.form("edit_project_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_name = st.text_input("Project Name", value=project['name'])
                edit_location = st.text_input("Location", value=project['location'] or "")
            with col2:
                edit_status = st.selectbox("Status", ["Active", "Planning", "Completed", "On Hold"], index=["Active", "Planning", "Completed", "On Hold"].index(project['status']))
                edit_progress = st.slider("Progress (%)", 0, 100, project['progress'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Changes"):
                    update_project(project['id'], edit_name, edit_location, edit_status, edit_progress)
                    add_activity("Project Updated", f"Project '{edit_name}' updated", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success("✅ Project updated successfully!")
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.edit_mode = None
                    st.rerun()

# ============ DEFECTS CRUD ============
def render_defects():
    st.markdown('<div class="main-header"><h1>🐛 Defect Management</h1><p>Track and resolve quality issues</p></div>', unsafe_allow_html=True)
    
    # Statistics
    defects = get_all_defects()
    critical_count = sum(1 for d in defects if d['severity'] == 'Critical' and d['status'] != 'Resolved')
    open_count = sum(1 for d in defects if d['status'] not in ['Resolved', 'Closed'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open Defects", open_count)
    with col2:
        st.metric("Critical Issues", critical_count, delta="Urgent")
    with col3:
        st.metric("Total Defects", len(defects))
    
    # Add Defect Form
    with st.expander("➕ Report New Defect", expanded=False):
        with st.form("add_defect_form"):
            col1, col2 = st.columns(2)
            with col1:
                defect_id = st.text_input("Defect ID*", placeholder="D-XXX")
                location = st.text_input("Location*", placeholder="e.g., Floor 2, Column B3")
                severity = st.selectbox("Severity*", ["Minor", "Major", "Critical"])
            with col2:
                category = st.selectbox("Category", ["Structural", "Architectural", "MEP", "Safety", "Quality"])
                assigned_to = st.text_input("Assigned To", placeholder="Team member name")
            
            description = st.text_area("Description*", placeholder="Describe the defect in detail")
            
            if st.form_submit_button("Submit Defect Report"):
                if defect_id and location and description:
                    success = add_defect(defect_id, location, severity, category, description, st.session_state.user['full_name'], assigned_to)
                    if success:
                        add_activity("Defect Reported", f"Defect {defect_id}: {description[:50]}", st.session_state.user['role'], st.session_state.user['full_name'])
                        st.success(f"✅ Defect {defect_id} reported successfully!")
                        st.rerun()
                    else:
                        st.error(f"Defect ID {defect_id} already exists!")
                else:
                    st.error("Please fill in all required fields (*)")
    
    # Defects Table
    st.markdown('<div class="section-title">📋 Defect Register</div>', unsafe_allow_html=True)
    
    if defects:
        for defect in defects:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 1, 1.5, 1])
                
                with col1:
                    st.markdown(f"**{defect['defect_id']}**")
                    st.caption(defect['location'])
                
                with col2:
                    st.markdown(defect['description'][:60] + "..." if len(defect['description']) > 60 else defect['description'])
                
                with col3:
                    severity_class = f"badge-{defect['severity'].lower()}"
                    st.markdown(f"<span class='badge {severity_class}'>{defect['severity']}</span>", unsafe_allow_html=True)
                    st.caption(defect['category'])
                
                with col4:
                    status_class = defect['status'].lower().replace(' ', '-')
                    st.markdown(f"<span class='badge badge-{status_class}'>{defect['status']}</span>", unsafe_allow_html=True)
                    if defect['assigned_to']:
                        st.caption(f"To: {defect['assigned_to']}")
                
                with col5:
                    if st.button("✏️ Edit", key=f"edit_defect_{defect['defect_id']}"):
                        st.session_state.edit_mode = ('defect', dict(defect))
                        st.rerun()
                    if st.button("🗑️ Delete", key=f"delete_defect_{defect['defect_id']}"):
                        delete_defect(defect['defect_id'])
                        st.success(f"✅ Defect {defect['defect_id']} deleted")
                        st.rerun()
                
                st.divider()
    
    # Edit Modal
    if st.session_state.edit_mode and st.session_state.edit_mode[0] == 'defect':
        defect = st.session_state.edit_mode[1]
        st.markdown("---")
        st.subheader(f"✏️ Edit Defect: {defect['defect_id']}")
        
        with st.form("edit_defect_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_location = st.text_input("Location", value=defect['location'])
                edit_severity = st.selectbox("Severity", ["Minor", "Major", "Critical"], index=["Minor", "Major", "Critical"].index(defect['severity']))
                edit_category = st.selectbox("Category", ["Structural", "Architectural", "MEP", "Safety", "Quality"], index=["Structural", "Architectural", "MEP", "Safety", "Quality"].index(defect['category']))
            with col2:
                edit_status = st.selectbox("Status", ["Open", "In Progress", "Verified", "Resolved", "Closed"], index=["Open", "In Progress", "Verified", "Resolved", "Closed"].index(defect['status']))
                edit_assigned_to = st.text_input("Assigned To", value=defect['assigned_to'] or "")
                edit_resolution = st.text_area("Resolution Notes", value=defect['resolution_notes'] or "")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Changes"):
                    update_defect(defect['defect_id'], edit_location, edit_severity, edit_category, edit_status, edit_assigned_to, edit_resolution)
                    add_activity("Defect Updated", f"Defect {defect['defect_id']} status changed to {edit_status}", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success("✅ Defect updated successfully!")
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.edit_mode = None
                    st.rerun()

# ============ RFIS CRUD ============
def render_rfis():
    st.markdown('<div class="main-header"><h1>💬 RFI Management</h1><p>Request for Information tracking and responses</p></div>', unsafe_allow_html=True)
    
    rfis = get_all_rfis()
    open_count = sum(1 for r in rfis if r['status'] == 'Open')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Open RFIs", open_count)
    with col2:
        st.metric("Total RFIs", len(rfis))
    
    # Add RFI Form
    with st.expander("➕ Create New RFI", expanded=False):
        with st.form("add_rfi_form"):
            col1, col2 = st.columns(2)
            with col1:
                rfi_number = st.text_input("RFI Number*", placeholder="RFI-XXX")
                title = st.text_input("Title*", placeholder="Brief title")
                category = st.selectbox("Category", ["Technical", "Structural", "Architectural", "Materials", "Safety"])
            with col2:
                priority = st.selectbox("Priority", ["Normal", "High", "Critical"])
                assigned_to = st.text_input("Assigned To", placeholder="Department or person")
            
            description = st.text_area("Description*", placeholder="Detailed RFI description")
            
            if st.form_submit_button("Submit RFI"):
                if rfi_number and title and description:
                    success = add_rfi(rfi_number, title, description, category, priority, assigned_to, st.session_state.user['username'])
                    if success:
                        add_activity("RFI Created", f"RFI {rfi_number}: {title}", st.session_state.user['role'], st.session_state.user['full_name'])
                        st.success(f"✅ RFI {rfi_number} created successfully!")
                        st.rerun()
                    else:
                        st.error(f"RFI number {rfi_number} already exists!")
                else:
                    st.error("Please fill in all required fields (*)")
    
    # RFIs List
    st.markdown('<div class="section-title">📋 RFI Register</div>', unsafe_allow_html=True)
    
    if rfis:
        for rfi in rfis:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 1.2, 1.3, 1])
                
                with col1:
                    st.markdown(f"**{rfi['rfi_number']}**")
                    st.caption(rfi['category'])
                
                with col2:
                    st.markdown(f"**{rfi['title']}**")
                    st.caption(rfi['description'][:60] + "..." if len(rfi['description']) > 60 else rfi['description'])
                
                with col3:
                    priority_colors = {"Critical": "#dc2626", "High": "#f59e0b", "Normal": "#10b981"}
                    st.markdown(f"<span style='color:{priority_colors.get(rfi['priority'], '#666')}'>⚡ {rfi['priority']}</span>", unsafe_allow_html=True)
                    st.caption(f"To: {rfi['assigned_to']}")
                
                with col4:
                    status_class = rfi['status'].lower().replace(' ', '-')
                    st.markdown(f"<span class='badge badge-{status_class}'>{rfi['status']}</span>", unsafe_allow_html=True)
                
                with col5:
                    if st.button("✏️ Edit", key=f"edit_rfi_{rfi['id']}"):
                        st.session_state.edit_mode = ('rfi', dict(rfi))
                        st.rerun()
                    if st.button("🗑️ Delete", key=f"delete_rfi_{rfi['id']}"):
                        delete_rfi(rfi['id'])
                        st.success(f"✅ RFI {rfi['rfi_number']} deleted")
                        st.rerun()
                
                st.divider()
    
    # Edit Modal
    if st.session_state.edit_mode and st.session_state.edit_mode[0] == 'rfi':
        rfi = st.session_state.edit_mode[1]
        st.markdown("---")
        st.subheader(f"✏️ Edit RFI: {rfi['rfi_number']}")
        
        with st.form("edit_rfi_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_title = st.text_input("Title", value=rfi['title'])
                edit_category = st.selectbox("Category", ["Technical", "Structural", "Architectural", "Materials", "Safety"], index=["Technical", "Structural", "Architectural", "Materials", "Safety"].index(rfi['category']))
                edit_priority = st.selectbox("Priority", ["Normal", "High", "Critical"], index=["Normal", "High", "Critical"].index(rfi['priority']))
            with col2:
                edit_status = st.selectbox("Status", ["Open", "In Review", "Answered", "Closed"], index=["Open", "In Review", "Answered", "Closed"].index(rfi['status']))
                edit_assigned_to = st.text_input("Assigned To", value=rfi['assigned_to'] or "")
            
            edit_description = st.text_area("Description", value=rfi['description'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save Changes"):
                    update_rfi(rfi['id'], edit_title, edit_description, edit_category, edit_priority, edit_status, edit_assigned_to)
                    add_activity("RFI Updated", f"RFI {rfi['rfi_number']} updated", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success("✅ RFI updated successfully!")
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.edit_mode = None
                    st.rerun()

# ============ MATERIALS CRUD ============
def render_materials():
    st.markdown('<div class="main-header"><h1>📦 Inventory Management</h1><p>Track materials, usage, and procurement</p></div>', unsafe_allow_html=True)
    
    materials = get_all_materials()
    
    # Summary
    total_value = sum((m['quantity_estimated'] or 0) * (m['unit_price'] or 0) for m in materials)
    low_stock = sum(1 for m in materials if m['status'] == 'Low stock')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Materials", len(materials))
    with col2:
        st.metric("Low Stock Items", low_stock, delta="Need reorder" if low_stock > 0 else None)
    with col3:
        st.metric("Inventory Value", f"${total_value:,.0f}")
    
    # Add Material Form
    with st.expander("➕ Add New Material", expanded=False):
        with st.form("add_material_form"):
            col1, col2 = st.columns(2)
            with col1:
                material_name = st.text_input("Material Name*", placeholder="e.g., Portland Cement")
                category = st.text_input("Category*", placeholder="e.g., Concrete")
                quantity_estimated = st.number_input("Estimated Quantity*", min_value=0.0, step=100.0)
            with col2:
                unit = st.text_input("Unit*", placeholder="e.g., tons, m³, bags")
                unit_price = st.number_input("Unit Price ($)", min_value=0.0, step=10.0)
                supplier = st.text_input("Supplier", placeholder="Supplier name")
            
            if st.form_submit_button("Add Material"):
                if material_name and category and quantity_estimated > 0 and unit:
                    add_material(material_name, category, quantity_estimated, unit, unit_price, supplier)
                    add_activity("Material Added", f"New material: {material_name}", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success(f"✅ Material '{material_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")
    
    # Materials List
    st.markdown('<div class="section-title">📋 Material Inventory</div>', unsafe_allow_html=True)
    
    if materials:
        for material in materials:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 1.5, 1])
                
                with col1:
                    st.markdown(f"**{material['material_name']}**")
                    st.caption(material['category'])
                
                with col2:
                    used_percent = (material['quantity_used'] / material['quantity_estimated'] * 100) if material['quantity_estimated'] > 0 else 0
                    st.progress(min(used_percent / 100, 1.0), text=f"{material['quantity_used']:.0f} / {material['quantity_estimated']:.0f} {material['unit']}")
                
                with col3:
                    if material['unit_price']:
                        st.markdown(f"**${material['unit_price']:.2f}** per {material['unit']}")
                    st.caption(material['supplier'] or "No supplier")
                
                with col4:
                    status_color = "red" if material['status'] == 'Low stock' else "green"
                    st.markdown(f"<span class='badge' style='background:#{status_color}20; color:{status_color}'>{material['status']}</span>", unsafe_allow_html=True)
                
                with col5:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📦", key=f"usage_{material['id']}"):
                            st.session_state.edit_mode = ('usage', dict(material))
                    with col_b:
                        if st.button("🗑️", key=f"delete_material_{material['id']}"):
                            delete_material(material['id'])
                            st.rerun()
                
                st.divider()
    
    # Usage Update Modal
    if st.session_state.edit_mode and st.session_state.edit_mode[0] == 'usage':
        material = st.session_state.edit_mode[1]
        st.markdown("---")
        with st.form("update_usage_form"):
            st.subheader(f"Update Usage: {material['material_name']}")
            quantity = st.number_input(f"Additional Quantity Used ({material['unit']})", min_value=0.0, step=10.0)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update Usage"):
                    update_material_usage(material['id'], quantity)
                    add_activity("Material Usage Updated", f"Used {quantity} {material['unit']} of {material['material_name']}", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success("✅ Usage updated successfully!")
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.edit_mode = None
                    st.rerun()

# ============ TASKS CRUD ============
def render_tasks():
    st.markdown('<div class="main-header"><h1>✅ Task Management</h1><p>Assign and track project tasks</p></div>', unsafe_allow_html=True)
    
    tasks = get_all_tasks()
    pending_count = sum(1 for t in tasks if t['status'] == 'Pending')
    completed_count = sum(1 for t in tasks if t['status'] == 'Completed')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pending Tasks", pending_count)
    with col2:
        st.metric("Completed Tasks", completed_count)
    with col3:
        st.metric("Total Tasks", len(tasks))
    
    # Add Task Form
    with st.expander("➕ Create New Task", expanded=False):
        with st.form("add_task_form"):
            col1, col2 = st.columns(2)
            with col1:
                task_id = st.text_input("Task ID*", placeholder="TASK-XXX")
                title = st.text_input("Title*", placeholder="Task title")
                priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"])
            with col2:
                assigned_to = st.text_input("Assigned To*", placeholder="Person or team")
                due_date = st.date_input("Due Date")
            
            description = st.text_area("Description*", placeholder="Task details")
            
            if st.form_submit_button("Create Task"):
                if task_id and title and description and assigned_to:
                    success = add_task(task_id, title, description, priority, assigned_to, st.session_state.user['username'], due_date.isoformat())
                    if success:
                        add_activity("Task Created", f"Task {task_id}: {title}", st.session_state.user['role'], st.session_state.user['full_name'])
                        st.success(f"✅ Task {task_id} created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Task ID {task_id} already exists!")
                else:
                    st.error("Please fill in all required fields (*)")
    
    # Tasks List
    st.markdown('<div class="section-title">📋 Task List</div>', unsafe_allow_html=True)
    
    if tasks:
        for task in tasks:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 1.5, 1.5, 1])
                
                with col1:
                    st.markdown(f"**{task['task_id']}**")
                    priority_colors = {"Critical": "#dc2626", "High": "#f59e0b", "Normal": "#10b981", "Low": "#6b7280"}
                    st.markdown(f"<span style='color:{priority_colors.get(task['priority'], '#666')}'>⚡ {task['priority']}</span>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{task['title']}**")
                    st.caption(task['description'][:60] + "..." if len(task['description']) > 60 else task['description'])
                
                with col3:
                    st.caption(f"Assigned to: {task['assigned_to']}")
                    if task['due_date']:
                        st.caption(f"Due: {task['due_date']}")
                
                with col4:
                    status_color = {
                        "Pending": "#f59e0b",
                        "In Progress": "#3b82f6",
                        "Completed": "#10b981"
                    }.get(task['status'], "#6b7280")
                    st.markdown(f"<span class='badge' style='background:{status_color}20; color:{status_color}'>{task['status']}</span>", unsafe_allow_html=True)
                
                with col5:
                    if st.button("✏️ Edit", key=f"edit_task_{task['task_id']}"):
                        st.session_state.edit_mode = ('task', dict(task))
                        st.rerun()
                    if st.button("🗑️ Delete", key=f"delete_task_{task['task_id']}"):
                        delete_task(task['task_id'])
                        st.rerun()
                
                st.divider()
    
    # Edit Modal
    if st.session_state.edit_mode and st.session_state.edit_mode[0] == 'task':
        task = st.session_state.edit_mode[1]
        st.markdown("---")
        st.subheader(f"✏️ Edit Task: {task['task_id']}")
        
        with st.form("edit_task_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_title = st.text_input("Title", value=task['title'])
                edit_priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"], index=["Low", "Normal", "High", "Critical"].index(task['priority']))
                edit_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(task['status']))
            with col2:
                edit_assigned_to = st.text_input("Assigned To", value=task['assigned_to'])
                edit_due_date = st.date_input("Due Date", value=datetime.strptime(task['due_date'], "%Y-%m-%d").date() if task['due_date'] else datetime.now())
            
            edit_description = st.text_area("Description", value=task['description'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save Changes"):
                    update_task(task['task_id'], edit_title, edit_description, edit_status, edit_priority, edit_assigned_to, edit_due_date.isoformat())
                    add_activity("Task Updated", f"Task {task['task_id']} status: {edit_status}", st.session_state.user['role'], st.session_state.user['full_name'])
                    st.success("✅ Task updated!")
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.edit_mode = None
                    st.rerun()

# ============ DECISIONS CRUD ============
def render_decisions():
    st.markdown('<div class="main-header"><h1>⚖️ Decisions Register</h1><p>Track project decisions and approvals</p></div>', unsafe_allow_html=True)
    
    decisions = get_all_decisions()
    
    # Add Decision Form
    with st.expander("➕ Log New Decision", expanded=False):
        with st.form("add_decision_form"):
            col1, col2 = st.columns(2)
            with col1:
                decision_id = st.text_input("Decision ID*", placeholder="DEC-XXX")
                title = st.text_input("Title*", placeholder="Decision title")
                decision_maker = st.text_input("Decision Maker*", placeholder="Person or committee")
            with col2:
                effective_date = st.date_input("Effective Date")
                status = st.selectbox("Status", ["Pending", "Approved", "Rejected", "Deferred"])
            
            description = st.text_area("Description*", placeholder="Decision details and rationale")
            
            if st.form_submit_button("Log Decision"):
                if decision_id and title and description and decision_maker:
                    success = add_decision(decision_id, title, description, decision_maker, effective_date.isoformat())
                    if success:
                        add_activity("Decision Logged", f"Decision {decision_id}: {title}", st.session_state.user['role'], st.session_state.user['full_name'])
                        st.success(f"✅ Decision {decision_id} logged successfully!")
                        st.rerun()
                    else:
                        st.error(f"Decision ID {decision_id} already exists!")
                else:
                    st.error("Please fill in all required fields (*)")
    
    # Decisions List
    st.markdown('<div class="section-title">📋 Decisions Log</div>', unsafe_allow_html=True)
    
    if decisions:
        for decision in decisions:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 1.5, 1.5, 1])
                
                with col1:
                    st.markdown(f"**{decision['decision_id']}**")
                    st.caption(f"By: {decision['decision_maker']}")
                
                with col2:
                    st.markdown(f"**{decision['title']}**")
                    st.caption(decision['description'][:80] + "..." if len(decision['description']) > 80 else decision['description'])
                
                with col3:
                    if decision['effective_date']:
                        st.caption(f"Effective: {decision['effective_date']}")
                
                with col4:
                    status_color = {
                        "Approved": "#10b981",
                        "Pending": "#f59e0b",
                        "Rejected": "#dc2626",
                        "Deferred": "#6b7280"
                    }.get(decision['status'], "#6b7280")
                    st.markdown(f"<span class='badge' style='background:{status_color}20; color:{status_color}'>{decision['status']}</span>", unsafe_allow_html=True)
                
                with col5:
                    if st.button("✏️ Edit", key=f"edit_decision_{decision['decision_id']}"):
                        st.session_state.edit_mode = ('decision', dict(decision))
                        st.rerun()
                    if st.button("🗑️ Delete", key=f"delete_decision_{decision['decision_id']}"):
                        delete_decision(decision['decision_id'])
                        st.rerun()
                
                st.divider()
    
    # Edit Modal
    if st.session_state.edit_mode and st.session_state.edit_mode[0] == 'decision':
        decision = st.session_state.edit_mode[1]
        st.markdown("---")
        st.subheader(f"✏️ Edit Decision: {decision['decision_id']}")
        
        with st.form("edit_decision_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_title = st.text_input("Title", value=decision['title'])
                edit_decision_maker = st.text_input("Decision Maker", value=decision['decision_maker'])
                edit_status = st.selectbox("Status", ["Pending", "Approved", "Rejected", "Deferred"], index=["Pending", "Approved", "Rejected", "Deferred"].index(decision['status']))
            with col2:
                edit_effective_date = st.date_input("Effective Date", value=datetime.strptime(decision['effective_date'], "%Y-%m-%d").date() if decision['effective_date'] else datetime.now())
            
            edit_description = st.text_area("Description", value=decision['description'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save Changes"):
                    update_decision(decision['decision_id'], edit_title, edit_description, edit_status, edit_decision_maker, edit_effective_date.isoformat())
                    st.success("✅ Decision updated!")
                    st.session_state.edit_mode = None
                    st.rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.edit_mode = None
                    st.rerun()

# ============ MAIN APP ============
def main_app():
    # Sidebar Navigation
    with st.sidebar:
        # User info
        if st.session_state.user:
            st.markdown(f"""
            <div class="user-info">
                <strong>👋 {st.session_state.user['full_name']}</strong><br>
                <small>@{st.session_state.user['username']}<br>
                {st.session_state.user['role'].replace('_', ' ').title()}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("## 🏗️ Structura CEMS")
        st.caption("Construction Engineering Management System")
        st.divider()
        
        pages = {
            "📊 Dashboard": "Dashboard",
            "🏗️ Projects": "Projects",
            "🐛 Defects": "Defects",
            "💬 RFIs": "RFIs",
            "📦 Materials": "Materials",
            "✅ Tasks": "Tasks",
            "⚖️ Decisions": "Decisions",
            "👤 My Profile": "Profile"
        }
        
        # Add Admin Panel for admin users
        if st.session_state.user and st.session_state.user['role'] == 'admin':
            pages["⚙️ Admin Panel"] = "Admin"
        
        for icon, page in pages.items():
            if st.button(icon, use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page
                st.session_state.edit_mode = None
                st.rerun()
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.caption("v3.0 | Production Ready")
    
    # Page Router
    if st.session_state.current_page == "Dashboard":
        render_dashboard()
    elif st.session_state.current_page == "Projects":
        render_projects()
    elif st.session_state.current_page == "Defects":
        render_defects()
    elif st.session_state.current_page == "RFIs":
        render_rfis()
    elif st.session_state.current_page == "Materials":
        render_materials()
    elif st.session_state.current_page == "Tasks":
        render_tasks()
    elif st.session_state.current_page == "Decisions":
        render_decisions()
    elif st.session_state.current_page == "Profile":
        profile_page()
    elif st.session_state.current_page == "Admin":
        admin_panel()

# ============ APP ENTRY POINT ============
if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()
else:
    main_app()