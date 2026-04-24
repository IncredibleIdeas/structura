import sqlite3
from datetime import datetime
import hashlib
import os

DB_PATH = "structura_cems.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'viewer',
            department TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'Active',
            progress INTEGER DEFAULT 0,
            start_date TEXT,
            end_date TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # RFI (Request for Information) table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rfis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rfi_number TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'Technical',
            priority TEXT DEFAULT 'Normal',
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Defects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            defect_id TEXT UNIQUE NOT NULL,
            location TEXT NOT NULL,
            severity TEXT DEFAULT 'Minor',
            category TEXT DEFAULT 'Quality',
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            description TEXT,
            reported_by TEXT,
            resolution_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP
        )
    ''')
    
    # Materials/Inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_name TEXT NOT NULL,
            category TEXT,
            quantity_used REAL DEFAULT 0,
            quantity_estimated REAL DEFAULT 0,
            unit TEXT,
            unit_price REAL DEFAULT 0,
            supplier TEXT,
            status TEXT DEFAULT 'In Stock',
            reorder_level REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Budget table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            budget_allocated REAL DEFAULT 0,
            amount_spent REAL DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Activities/Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            description TEXT,
            user_role TEXT,
            user_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Decisions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            decision_maker TEXT,
            effective_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            priority TEXT DEFAULT 'Normal',
            assigned_to TEXT,
            assigned_by TEXT,
            due_date TEXT,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Session table for tracking logged in users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_token TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_sample_data():
    """Seed database with sample data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Create admin user
        admin_password = hash_password("admin123")
        cursor.execute("""INSERT INTO users (username, email, password_hash, full_name, role, department, is_active) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       ("admin", "admin@structura.com", admin_password, "System Administrator", "admin", "Management", 1))
        
        # Create sample users
        users = [
            ("john.architect", "john@structura.com", hash_password("arch123"), "John Smith", "architect", "Design", 1),
            ("jane.engineer", "jane@structura.com", hash_password("eng123"), "Jane Wilson", "engineer", "Structural", 1),
            ("mike.worker", "mike@structura.com", hash_password("work123"), "Mike Johnson", "worker", "Construction", 1),
            ("sarah.pm", "sarah@structura.com", hash_password("pm123"), "Sarah Chen", "project_manager", "Management", 1)
        ]
        
        for user in users:
            cursor.execute("""INSERT INTO users (username, email, password_hash, full_name, role, department, is_active) 
                              VALUES (?, ?, ?, ?, ?, ?, ?)""", user)
    
    # Check if projects exist
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        # Sample projects
        projects = [
            ("Downtown Commercial Complex", "Downtown", "Active", 65, "2024-01-15", "2025-06-30", "admin"),
            ("Residential Tower A", "North District", "Active", 45, "2024-03-01", "2025-08-31", "admin"),
            ("Industrial Park Phase 1", "East Industrial Zone", "Planning", 15, "2024-06-01", "2026-01-31", "admin")
        ]
        for proj in projects:
            cursor.execute("""INSERT INTO projects (name, location, status, progress, start_date, end_date, created_by) 
                              VALUES (?, ?, ?, ?, ?, ?, ?)""", proj)
    
    # Check if RFIs exist
    cursor.execute("SELECT COUNT(*) FROM rfis")
    if cursor.fetchone()[0] == 0:
        # Sample RFIs
        rfis = [
            ("RFI-001", "Window detail conflict", "Clarification on flashing dimension for curtain wall installation", "Technical", "High", "Open", "Structural Engineer", "john.architect"),
            ("RFI-002", "Column reinforcement", "Alternative bar size approval for seismic zone", "Structural", "Critical", "In Review", "Project Manager", "jane.engineer"),
            ("RFI-003", "Material substitution request", "Request to substitute specified flooring material", "Materials", "Normal", "Open", "Interior Designer", "sarah.pm")
        ]
        for rfi in rfis:
            try:
                cursor.execute("""INSERT INTO rfis (rfi_number, title, description, category, priority, status, assigned_to, created_by) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", rfi)
            except sqlite3.IntegrityError:
                pass  # Skip if already exists
    
    # Check if defects exist
    cursor.execute("SELECT COUNT(*) FROM defects")
    if cursor.fetchone()[0] == 0:
        # Sample Defects
        defects = [
            ("D-001", "Roof waterproofing", "Critical", "Structural", "In Progress", "Subcontractor A", "Waterproofing membrane failure at seam joints", "Site Inspector"),
            ("D-002", "East staircase", "Major", "Architectural", "Open", "Site Crew", "Staircase alignment off by 15mm at landing", "Quality Control"),
            ("D-003", "HVAC ductwork", "Minor", "MEP", "Verified", "MEP Contractor", "Duct insulation missing in section B2", "Site Inspector"),
            ("D-004", "Foundation column", "Critical", "Structural", "Open", "Engineer", "Concrete strength below specification", "Quality Control")
        ]
        for defect in defects:
            try:
                cursor.execute("""INSERT INTO defects (defect_id, location, severity, category, status, assigned_to, description, reported_by) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", defect)
            except sqlite3.IntegrityError:
                pass
    
    # Check if materials exist
    cursor.execute("SELECT COUNT(*) FROM materials")
    if cursor.fetchone()[0] == 0:
        # Sample Materials
        materials = [
            ("Portland Cement", "Concrete", 214, 900, "tons", 120, "Cement Co.", "Low stock", 50),
            ("Structural Steel", "Steel", 84, 112, "tons", 850, "Steel Corp", "Sufficient", 20),
            ("Rebar 16mm", "Steel", 45, 80, "tons", 780, "Steel Corp", "Sufficient", 15),
            ("Ready-Mix Concrete", "Concrete", 430, 500, "m³", 110, "Concrete Supply Ltd", "Low stock", 100),
            ("Glass Panels", "Facade", 120, 200, "units", 450, "Glass Tech", "In Stock", 30)
        ]
        for mat in materials:
            cursor.execute("""INSERT INTO materials (material_name, category, quantity_used, quantity_estimated, unit, unit_price, supplier, status, reorder_level) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", mat)
    
    # Check if budget exists
    cursor.execute("SELECT COUNT(*) FROM budget")
    if cursor.fetchone()[0] == 0:
        # Sample Budget
        budget_items = [
            ("Labor", 550000, 445000, "Includes overtime and benefits"),
            ("Materials", 850000, 720000, "Steel, concrete, finishing materials"),
            ("Equipment", 300000, 275000, "Cranes, excavators, trucks"),
            ("Subcontractors", 400000, 180000, "Electrical, plumbing, HVAC"),
            ("Permits & Fees", 50000, 48000, "Building permits and inspections")
        ]
        for budget in budget_items:
            cursor.execute("""INSERT INTO budget (category, budget_allocated, amount_spent, notes) 
                              VALUES (?, ?, ?, ?)""", budget)
    
    # Check if activities exist
    cursor.execute("SELECT COUNT(*) FROM activities")
    if cursor.fetchone()[0] == 0:
        # Sample Activities
        activities = [
            ("Drawing Update", "Architect released structural revision Rev 05", "Architect", "John Smith"),
            ("Defect Report", "Critical defect reported on foundation column", "Inspector", "Mike Johnson"),
            ("RFI Response", "RFI-001 response provided with clarification", "Engineer", "Jane Wilson"),
            ("Material Delivery", "Steel shipment arrived on site", "Logistics", "Sarah Chen"),
            ("Safety Meeting", "Weekly safety briefing conducted", "Safety Officer", "Lisa Wong")
        ]
        for activity in activities:
            cursor.execute("""INSERT INTO activities (activity_type, description, user_role, user_name) 
                              VALUES (?, ?, ?, ?)""", activity)
    
    # Check if decisions exist
    cursor.execute("SELECT COUNT(*) FROM decisions")
    if cursor.fetchone()[0] == 0:
        # Sample Decisions
        decisions = [
            ("DEC-001", "Relocate HVAC duct", "Approved relocation of main duct to accommodate structural beam", "Architect", "2024-04-15", "Approved"),
            ("DEC-002", "Change fire-rated door spec", "Upgrade to 90-minute rating for all exit doors", "Fire Safety Engineer", "2024-04-20", "Approved"),
            ("DEC-003", "Material substitution approval", "Approved alternative flooring material meeting specs", "Project Manager", "2024-04-25", "Pending")
        ]
        for decision in decisions:
            try:
                cursor.execute("""INSERT INTO decisions (decision_id, title, description, decision_maker, effective_date, status) 
                                  VALUES (?, ?, ?, ?, ?, ?)""", decision)
            except sqlite3.IntegrityError:
                pass
    
    # Check if tasks exist
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        # Sample Tasks
        tasks = [
            ("TASK-001", "Complete foundation inspection", "Inspect all foundation columns before concrete pour", "Completed", "High", "Site Engineer", "Project Manager", "2024-04-30"),
            ("TASK-002", "RFI response for window detail", "Provide detailed drawing for window flashing", "In Progress", "High", "Architect", "Project Manager", "2024-05-05"),
            ("TASK-003", "Material order for steel", "Place order for additional structural steel", "Pending", "Normal", "Procurement", "Site Manager", "2024-05-10"),
            ("TASK-004", "Safety audit", "Conduct monthly site safety audit", "Pending", "Critical", "Safety Officer", "Project Director", "2024-05-07")
        ]
        for task in tasks:
            try:
                cursor.execute("""INSERT INTO tasks (task_id, title, description, status, priority, assigned_to, assigned_by, due_date) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", task)
            except sqlite3.IntegrityError:
                pass
    
    conn.commit()
    conn.close()

# ============ AUTHENTICATION FUNCTIONS ============
def authenticate_user(username, password):
    """Authenticate user credentials"""
    conn = get_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute("""SELECT id, username, full_name, email, role, department, is_active 
                      FROM users 
                      WHERE (username=? OR email=?) AND password_hash=? AND is_active=1""",
                   (username, username, password_hash))
    user = cursor.fetchone()
    
    if user:
        # Update last login
        cursor.execute("UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE id=?", (user['id'],))
        conn.commit()
    
    conn.close()
    return user

def register_user(username, email, password, full_name, role, department):
    """Register a new user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""INSERT INTO users (username, email, password_hash, full_name, role, department, is_active) 
                          VALUES (?, ?, ?, ?, ?, ?, 1)""",
                       (username, email, password_hash, full_name, role, department))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError as e:
        conn.close()
        if "username" in str(e):
            return False, "Username already exists"
        elif "email" in str(e):
            return False, "Email already exists"
        return False, "Registration failed"

def get_user_by_id(user_id):
    """Get user information by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, email, role, department FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, full_name, email, department):
    """Update user profile"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET full_name=?, email=?, department=? WHERE id=?", 
                   (full_name, email, department, user_id))
    conn.commit()
    conn.close()

def change_password(user_id, old_password, new_password):
    """Change user password"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verify old password
    old_hash = hash_password(old_password)
    cursor.execute("SELECT id FROM users WHERE id=? AND password_hash=?", (user_id, old_hash))
    if not cursor.fetchone():
        conn.close()
        return False, "Current password is incorrect"
    
    # Update to new password
    new_hash = hash_password(new_password)
    cursor.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, user_id))
    conn.commit()
    conn.close()
    return True, "Password changed successfully"

# ============ PROJECTS CRUD ============
def get_all_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    conn.close()
    return projects

def add_project(name, location, start_date, end_date, created_by):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO projects (name, location, status, progress, start_date, end_date, created_by) 
                      VALUES (?, ?, 'Active', 0, ?, ?, ?)""",
                   (name, location, start_date, end_date, created_by))
    conn.commit()
    conn.close()

def update_project(project_id, name, location, status, progress):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE projects 
                      SET name=?, location=?, status=?, progress=?, updated_at=CURRENT_TIMESTAMP 
                      WHERE id=?""",
                   (name, location, status, progress, project_id))
    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()

# ============ DEFECTS CRUD ============
def get_all_defects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM defects ORDER BY created_at DESC")
    defects = cursor.fetchall()
    conn.close()
    return defects

def get_defect_by_id(defect_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM defects WHERE defect_id=?", (defect_id,))
    defect = cursor.fetchone()
    conn.close()
    return defect

def add_defect(defect_id, location, severity, category, description, reported_by, assigned_to):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO defects (defect_id, location, severity, category, description, reported_by, assigned_to, status) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, 'Open')""",
                       (defect_id, location, severity, category, description, reported_by, assigned_to))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def update_defect(defect_id, location, severity, category, status, assigned_to, resolution_notes):
    conn = get_connection()
    cursor = conn.cursor()
    resolved_at = datetime.now().isoformat() if status == 'Resolved' else None
    cursor.execute("""UPDATE defects 
                      SET location=?, severity=?, category=?, status=?, assigned_to=?, resolution_notes=?, 
                          updated_at=CURRENT_TIMESTAMP, resolved_at=COALESCE(?, resolved_at)
                      WHERE defect_id=?""",
                   (location, severity, category, status, assigned_to, resolution_notes, resolved_at, defect_id))
    conn.commit()
    conn.close()

def delete_defect(defect_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM defects WHERE defect_id=?", (defect_id,))
    conn.commit()
    conn.close()

# ============ RFIS CRUD ============
def get_all_rfis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rfis ORDER BY created_at DESC")
    rfis = cursor.fetchall()
    conn.close()
    return rfis

def add_rfi(rfi_number, title, description, category, priority, assigned_to, created_by):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO rfis (rfi_number, title, description, category, priority, assigned_to, created_by, status) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, 'Open')""",
                       (rfi_number, title, description, category, priority, assigned_to, created_by))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def update_rfi(rfi_id, title, description, category, priority, status, assigned_to):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE rfis 
                      SET title=?, description=?, category=?, priority=?, status=?, assigned_to=?, updated_at=CURRENT_TIMESTAMP 
                      WHERE id=?""",
                   (title, description, category, priority, status, assigned_to, rfi_id))
    conn.commit()
    conn.close()

def delete_rfi(rfi_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rfis WHERE id=?", (rfi_id,))
    conn.commit()
    conn.close()

# ============ MATERIALS CRUD ============
def get_all_materials():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materials ORDER BY created_at DESC")
    materials = cursor.fetchall()
    conn.close()
    return materials

def add_material(material_name, category, quantity_estimated, unit, unit_price, supplier):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO materials (material_name, category, quantity_estimated, unit, unit_price, supplier, status) 
                      VALUES (?, ?, ?, ?, ?, ?, 'In Stock')""",
                   (material_name, category, quantity_estimated, unit, unit_price, supplier))
    conn.commit()
    conn.close()

def update_material(material_id, material_name, category, quantity_estimated, unit, unit_price, supplier, status, reorder_level):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE materials 
                      SET material_name=?, category=?, quantity_estimated=?, unit=?, unit_price=?, supplier=?, status=?, reorder_level=?, updated_at=CURRENT_TIMESTAMP 
                      WHERE id=?""",
                   (material_name, category, quantity_estimated, unit, unit_price, supplier, status, reorder_level, material_id))
    conn.commit()
    conn.close()

def update_material_usage(material_id, quantity_used):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE materials SET quantity_used=quantity_used+?, updated_at=CURRENT_TIMESTAMP WHERE id=?", 
                   (quantity_used, material_id))
    conn.commit()
    conn.close()

def delete_material(material_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materials WHERE id=?", (material_id,))
    conn.commit()
    conn.close()

# ============ TASKS CRUD ============
def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(task_id, title, description, priority, assigned_to, assigned_by, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO tasks (task_id, title, description, priority, assigned_to, assigned_by, due_date, status) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')""",
                       (task_id, title, description, priority, assigned_to, assigned_by, due_date))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def update_task(task_id, title, description, status, priority, assigned_to, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    completed_at = datetime.now().isoformat() if status == 'Completed' else None
    cursor.execute("""UPDATE tasks 
                      SET title=?, description=?, status=?, priority=?, assigned_to=?, due_date=?, 
                          updated_at=CURRENT_TIMESTAMP, completed_at=COALESCE(?, completed_at)
                      WHERE task_id=?""",
                   (title, description, status, priority, assigned_to, due_date, completed_at, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
    conn.commit()
    conn.close()

# ============ DECISIONS CRUD ============
def get_all_decisions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM decisions ORDER BY created_at DESC")
    decisions = cursor.fetchall()
    conn.close()
    return decisions

def add_decision(decision_id, title, description, decision_maker, effective_date):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO decisions (decision_id, title, description, decision_maker, effective_date, status) 
                          VALUES (?, ?, ?, ?, ?, 'Pending')""",
                       (decision_id, title, description, decision_maker, effective_date))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def update_decision(decision_id, title, description, status, decision_maker, effective_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE decisions 
                      SET title=?, description=?, status=?, decision_maker=?, effective_date=?, updated_at=CURRENT_TIMESTAMP 
                      WHERE decision_id=?""",
                   (title, description, status, decision_maker, effective_date, decision_id))
    conn.commit()
    conn.close()

def delete_decision(decision_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM decisions WHERE decision_id=?", (decision_id,))
    conn.commit()
    conn.close()

# ============ DASHBOARD & UTILITIES ============
def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Active'")
    active_projects = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM rfis WHERE status='Open'")
    open_rfis = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM defects WHERE severity='Critical' AND status != 'Resolved'")
    critical_defects = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'")
    pending_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(budget_allocated) as total_budget, SUM(amount_spent) as total_spent FROM budget")
    budget_data = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    conn.close()
    return {
        "active_projects": active_projects,
        "open_rfis": open_rfis,
        "critical_defects": critical_defects,
        "pending_tasks": pending_tasks,
        "total_budget": budget_data[0] or 0,
        "total_spent": budget_data[1] or 0,
        "total_users": total_users
    }

def get_progress_data():
    return {
        "weeks": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
        "planned": [15, 30, 45, 60, 75, 90],
        "actual": [14, 28, 43, 58, 72, 85]
    }

def get_recent_activities(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities ORDER BY created_at DESC LIMIT ?", (limit,))
    activities = cursor.fetchall()
    conn.close()
    return activities

def add_activity(activity_type, description, user_role, user_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO activities (activity_type, description, user_role, user_name) 
                      VALUES (?, ?, ?, ?)""",
                   (activity_type, description, user_role, user_name))
    conn.commit()
    conn.close()

def get_budget_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, budget_allocated, amount_spent FROM budget")
    budget_items = cursor.fetchall()
    conn.close()
    return budget_items

def get_all_users():
    """Get all users for admin panel"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, full_name, role, department, is_active, last_login, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_status(user_id, is_active):
    """Activate or deactivate a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_active=? WHERE id=?", (is_active, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Delete a user"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()