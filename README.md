# Structura CEMS - Construction Engineering Management System

A comprehensive web-based Construction Engineering Management System built with **Python Streamlit** and **SQLite**, designed to streamline project management, defect tracking, RFI management, and team collaboration.

## Features

### 📊 Dashboard
- Real-time KPIs: Active Projects, Open RFIs, Critical Defects, Site Attendance
- Progress tracking with planned vs. actual charts
- Recent activity feed
- Quick defect overview

### 📐 Architect Hub
- BIM Model Viewer integration (placeholder for IFC viewer)
- Drawing annotation tools
- Revision upload functionality
- Pending RFI tracking

### 👷 Engineer Panel
- Structural compliance tracking
- Rebar and formwork inspections
- Material reconciliation
- NCR (Non-Conformance Report) management

### 🔧 Site Worker Portal
- Assigned tasks management
- Daily safety briefing checklist
- Task status tracking
- Priority-based task organization

### 🐛 Defects & Quality Control
- Comprehensive defect lifecycle tracker
- Severity classification (Critical, Major, Minor)
- Defect status management
- New defect reporting form
- Defect statistics and summary

### 💬 RFI & Decisions Management
- Request for Information (RFI) tracking
- RFI status management (Pending, Resolved)
- Meeting decisions logging
- Decision approval workflow

### 📦 Materials & Procurement
- Inventory tracking
- Material usage monitoring
- Low stock alerts
- Budget vs. Actual spending
- Material procurement management

## Project Structure

```
structura_cems_streamlit/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite database management
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project:**
   ```bash
   cd structura_cems_streamlit
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Database

The application uses **SQLite** for data persistence. The database file `structura_cems.db` is automatically created on first run.

### Database Tables

- **projects**: Active construction projects
- **rfis**: Request for Information records
- **defects**: Quality defects and issues
- **materials**: Inventory and material tracking
- **budget**: Project budget allocation and spending
- **activities**: Activity logs and recent actions
- **decisions**: Meeting decisions and approvals
- **worker_tasks**: Worker assignments and tasks

### Sample Data

The application automatically seeds the database with sample data on first run, including:
- 2 active projects
- Multiple RFIs in various states
- Defects with different severity levels
- Material inventory
- Budget allocations
- Recent activities
- Meeting decisions
- Worker tasks

## User Roles

The system is designed for multiple user roles:

- **Project Director**: Overall project oversight (Alex Rivera)
- **Architect**: Design and BIM management
- **Civil Engineer**: Structural compliance and material coordination
- **Site Worker**: Daily tasks and safety compliance
- **Quality Manager**: Defect tracking and management

## Navigation

Use the sidebar to navigate between different sections:
- 📊 Dashboard
- 📐 Architect Hub
- 👷 Engineer Panel
- 🔧 Site Worker
- 🐛 Defects & Quality
- 💬 RFI & Decisions
- 📦 Materials & Budget

## Features in Detail

### Dashboard
- Displays key performance indicators
- Shows project progress trends
- Lists recent activities
- Quick access to critical defects

### Defect Management
- Create new defect reports
- Track defect status
- Assign defects to team members
- Categorize by severity
- View defect statistics

### RFI Management
- Create and track RFIs
- Update RFI status
- Log meeting decisions
- Maintain decision history

### Material Tracking
- Monitor material usage
- Track inventory levels
- Alert on low stock
- Budget tracking and reporting

## Customization

### Adding New Features

1. **Add new database tables** in `database.py`:
   - Define table schema in `init_database()`
   - Add helper functions for CRUD operations

2. **Create new pages** in `app.py`:
   - Add new render function
   - Add to `page_functions` dictionary
   - Add navigation button in sidebar

3. **Update styling**:
   - Modify CSS in the `st.markdown()` section
   - Use existing badge and card classes
   - Maintain color scheme consistency

### Database Modifications

To add new fields to existing tables:
1. Modify the CREATE TABLE statements in `database.py`
2. Delete `structura_cems.db` to reset
3. Restart the application

## Troubleshooting

### Database Issues
- **"Database is locked"**: Ensure only one instance is running
- **"Table already exists"**: Delete `structura_cems.db` and restart

### Display Issues
- **Charts not showing**: Ensure Plotly is installed (`pip install plotly`)
- **Styling not applied**: Clear browser cache and refresh

### Performance
- For large datasets, consider adding pagination
- Implement database indexing on frequently queried columns

## Future Enhancements

- User authentication and role-based access control
- File upload for BIM models and drawings
- Email notifications for RFI updates
- Advanced reporting and analytics
- Mobile app version
- Real-time collaboration features
- Integration with external APIs

## Support

For issues or feature requests, please refer to the project documentation or contact the development team.

## License

This project is proprietary and confidential.

---

**Version**: 2.0  
**Last Updated**: 2026-04-24  
**Status**: Production Ready
