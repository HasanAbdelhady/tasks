# Task Tracker (مُتتبع المهام)

A real-time task management system designed for tracking tasks and subtasks among team members. Features time-sensitive task management, progress tracking, and a full Arabic interface.

## Features

- **Real-time Task Monitoring**: Live updates every 5 seconds showing task progress and remaining time
- **Role-based Access**: Separate interfaces for administrators and team members
- **Daily Task Management**: Reset and start fresh tasks each day
- **Progress History**: Track and view historical progress data
- **Time-sensitive Tasks**: Visual indicators for deadlines and expired tasks
- **Multi-language Support**: Full Arabic interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation

1. Clone the repository: `bash
git clone https://github.com/HasanAbdelhady/tasks.git
cd task-tracker   `

2. Create and activate a virtual environment: ```bash

   # On Windows

   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux

   python -m venv venv
   source venv/bin/activate ```

3. Install dependencies: `bash
pip install -r requirements.txt   `

4. Apply database migrations: `bash
python manage.py migrate   `

## Initial Setup

1. Create an admin user: `bash
python manage.py createsuperuser   `

2. Generate sample tasks (optional): `bash
python manage.py create_sample_tasks   `

3. Start the development server: `bash
python manage.py runserver   `

4. Access the application:
   - Admin dashboard: http://localhost:8000/admin-dashboard/
   - Team member view: http://localhost:8000/assignee-view/

## Usage Guide

### Administrator Features

1. **Dashboard Access**

   - View all active tasks
   - Monitor team members' progress
   - See real-time completion status

2. **Daily Task Management**

   - Click "بدء يوم جديد من المهام" to:
     - Reset all tasks
     - Update deadlines
     - Store previous day's progress

3. **Progress Monitoring**
   - View daily progress history
   - Track completion rates
   - Monitor individual performance

### Team Member Features

1. **Task Selection**

   - Choose from available tasks
   - View task deadlines
   - See expired task indicators

2. **Task Progress**
   - Mark subtasks as complete
   - Track remaining time
   - Switch between tasks

## Project Structure

task_tracker/
├── tasks/
│ ├── management/
│ │ └── commands/
│ │ ├── create_sample_tasks.py
│ │ └── delete_all_tasks.py
│ ├── models.py
│ └── views.py
└── templates/
├── admin_dashboard.html
├── all_users.html
├── assignee_view.html
└── base.html

## Development Commands

- Create sample tasks:

  ```bash
  python manage.py create_sample_tasks
  ```

- Delete all tasks:
  ```bash
  python manage.py delete_all_tasks
  ```

## Technical Details

- **Task Updates**: Automatic page refresh every 5 seconds
- **Task Deadlines**: Calculated based on task ID (10-120 minutes)
- **Progress Storage**: Automatically saved when starting new day
- **Database Models**:
  - Task: Main task container
  - Subtask: Individual task components
  - DailyProgress: Historical tracking

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
