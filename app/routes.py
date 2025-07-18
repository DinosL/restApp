from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
from app.db import db
from datetime import datetime, timezone

app_bp = Blueprint("tasks", __name__)

@app_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": t.id,
            "description": t.description,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "is_completed": t.is_completed,
            "created_at": t.created_at.isoformat()
        } for t in tasks
    ]), 200

@app_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get("description"):
        return jsonify({"msg": "Description is required"}), 400

    try:
        due_date = datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
    except ValueError:
        return jsonify({"msg": "Invalid due_date format. Use ISO 8601."}), 400

    task = Task(
        description=data["description"],
        due_date=due_date,
        is_completed=data.get("is_completed", False),
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({
        "id": task.id,
        "description": task.description,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "is_completed": task.is_completed,
        "created_at": task.created_at.isoformat()
    }), 201

@app_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    data = request.get_json()
    if "description" in data:
        task.description = data["description"]

    if "due_date" in data:
        try:
            task.due_date = datetime.fromisoformat(data["due_date"]) if data["due_date"] else None
        except ValueError:
            return jsonify({"msg": "Invalid due_date format"}), 400

    if "is_completed" in data:
        task.is_completed = data["is_completed"]

    db.session.commit()
    return jsonify({"msg": "Task updated"}), 200

@app_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task deleted"}), 200
