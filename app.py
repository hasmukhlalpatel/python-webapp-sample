from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "task": "Learn Python", "completed": True, "created": "2024-01-15"},
    {"id": 2, "task": "Build Flask app", "completed": False, "created": "2024-01-16"},
    {"id": 3, "task": "Deploy to Azure", "completed": False, "created": "2024-01-17"}
]

@app.route('/')
def home():
    """Home page with welcome message"""
    return render_template('index.html', 
                         app_name="Python Sample App",
                         timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify({"tasks": tasks})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Task description required"}), 400
    
    new_task = {
        "id": max([t["id"] for t in tasks]) + 1 if tasks else 1,
        "task": data['task'],
        "completed": False,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    tasks.append(new_task)
    
    logger.info(f"Created new task: {new_task['task']}")
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    if 'completed' in data:
        task['completed'] = data['completed']
    if 'task' in data:
        task['task'] = data['task']
    
    logger.info(f"Updated task {task_id}")
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    logger.info(f"Deleted task {task_id}")
    return jsonify({"message": "Task deleted successfully"})

@app.route('/info')
def app_info():
    """Display app information and environment"""
    env_vars = {
        "PORT": os.getenv("PORT", "5000"),
        "PYTHONPATH": os.getenv("PYTHONPATH", "Not set"),
        "WEBSITE_SITE_NAME": os.getenv("WEBSITE_SITE_NAME", "Local"),
        "WEBSITE_RESOURCE_GROUP": os.getenv("WEBSITE_RESOURCE_GROUP", "Not set")
    }
    
    return render_template('info.html', 
                         env_vars=env_vars,
                         python_version=os.sys.version)

@app.route('/tasks')
def tasks_page():
    """Tasks management page"""
    return render_template('tasks.html', tasks=tasks)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)