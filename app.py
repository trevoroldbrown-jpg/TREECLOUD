import json
import os
import subprocess
import sys
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
APPROVALS_FILE = 'approvals.json'
INTERESTS_FILE = 'interests.json'
DATA_FILE = 'data.json'

def init_approvals_file():
    if not os.path.exists(APPROVALS_FILE):
        with open(APPROVALS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

@app.route('/')
def serve_ui():
    return send_file('index.html')

@app.route('/data.json')
def serve_data():
    return send_file('data.json')

@app.route('/api/spark', methods=['POST'])
def spark_idea():
    data = request.json
    init_approvals_file()
    with open(APPROVALS_FILE, 'r', encoding='utf-8') as f:
        try:
            approvals = json.load(f)
        except json.JSONDecodeError:
            approvals = []
            
    if any(item.get('title') == data.get('title') for item in approvals):
        return jsonify({"status": "already_exists", "message": "You already sparked this idea!"})
        
    data['processed'] = False
    approvals.append(data)
    with open(APPROVALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(approvals, f, indent=4)
        
    return jsonify({"status": "success", "message": "Idea sparked and saved!"})

@app.route('/api/interests', methods=['GET'])
def get_interests():
    try:
        if not os.path.exists(INTERESTS_FILE):
            return jsonify([])
        with open(INTERESTS_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/interests', methods=['POST'])
def set_interests():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Expected a JSON array of interest strings"}), 400
    with open(INTERESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return jsonify({"status": "success", "interests": data})

@app.route('/api/refresh-feed', methods=['POST'])
def refresh_feed():
    try:
        result = subprocess.run(
            [sys.executable, 'watcher.py'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            # Read the freshly updated data
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return jsonify({
                    "status": "success",
                    "message": f"Feed refreshed! Found {len(data.get('items', []))} items.",
                    "last_updated": data.get('last_updated'),
                    "item_count": len(data.get('items', []))
                })
            return jsonify({"status": "success", "message": "Feed refreshed."})
        else:
            return jsonify({
                "status": "error",
                "message": result.stderr or "watcher.py exited with an error."
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Refresh timed out after 60s."}), 504
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Treecloud Hub Backend at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
