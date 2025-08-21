#!/usr/bin/env python3
"""
Budget Management API Endpoints
REST API for managing user budgets and viewing usage statistics
"""

from flask import Flask, request, jsonify
import os
from budget_manager import BudgetManager

app = Flask(__name__)
budget_manager = BudgetManager(os.getenv("DATABASE_URL"))

@app.route('/budget/users', methods=['POST'])
def create_user_budget():
    """Create or update user budget"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        daily_limit = float(data.get('daily_limit', 10.0))
        monthly_limit = float(data.get('monthly_limit', 100.0))
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        success = budget_manager.create_user_budget(user_id, daily_limit, monthly_limit)
        
        if success:
            return jsonify({
                "success": True,
                "message": f"Budget created for user {user_id}",
                "user_id": user_id,
                "daily_limit": daily_limit,
                "monthly_limit": monthly_limit
            })
        else:
            return jsonify({"error": "Failed to create budget"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/budget/users/<user_id>', methods=['GET'])
def get_user_budget(user_id):
    """Get user budget and usage statistics"""
    try:
        stats = budget_manager.get_user_stats(user_id)
        
        if "error" in stats:
            return jsonify(stats), 404
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/budget/users/<user_id>/check', methods=['POST'])
def check_user_budget(user_id):
    """Check if user can make a request within budget"""
    try:
        data = request.get_json()
        model = data.get('model', 'chatgpt-4o-latest')
        estimated_tokens = int(data.get('estimated_tokens', 1000))
        
        budget_check = budget_manager.check_user_budget(user_id, model, estimated_tokens)
        
        return jsonify(budget_check)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/budget/users/<user_id>/usage', methods=['POST'])
def track_user_usage(user_id):
    """Track user usage (called after request completion)"""
    try:
        data = request.get_json()
        model = data.get('model')
        input_tokens = int(data.get('input_tokens', 0))
        output_tokens = int(data.get('output_tokens', 0))
        
        if not model:
            return jsonify({"error": "model is required"}), 400
        
        cost = budget_manager.track_usage(user_id, model, input_tokens, output_tokens)
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/budget/models/pricing', methods=['GET'])
def get_model_pricing():
    """Get current model pricing information"""
    return jsonify({
        "models": budget_manager.token_costs,
        "currency": "USD",
        "unit": "per 1K tokens",
        "note": "Pricing includes both input and output token costs"
    })

@app.route('/budget/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "budget_manager",
        "database": "connected" if budget_manager.database_url else "not_configured"
    })

if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5000, debug=True)
