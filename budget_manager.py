#!/usr/bin/env python3
"""
LiteLLM User Budget Management System
Tracks input/output tokens and enforces budget limits per user
"""

import os
import json
import sqlite3
import psycopg2
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import requests
from dataclasses import dataclass

@dataclass
class UserBudget:
    user_id: str
    daily_limit_usd: float
    monthly_limit_usd: float
    current_daily_spend: float = 0.0
    current_monthly_spend: float = 0.0
    total_tokens_input: int = 0
    total_tokens_output: int = 0
    last_reset_date: str = ""

class BudgetManager:
    def __init__(self, database_url: str):
        """Initialize budget manager with database connection"""
        self.database_url = database_url
        self.token_costs = {
            # Model pricing per 1K tokens (input, output)
            "chatgpt-4o-latest": {"input": 0.005, "output": 0.015},
            "chatgpt-4o": {"input": 0.005, "output": 0.015},
            "chatgpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
            "gemini-1-5-pro": {"input": 0.00125, "output": 0.005},
            "llama-3-1-70b": {"input": 0.0009, "output": 0.0009},
            "llama-3-1-8b": {"input": 0.0002, "output": 0.0002},
        }
        self.setup_database()
    
    def setup_database(self):
        """Create budget tracking tables"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Create user budget table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_budgets (
                    user_id VARCHAR(255) PRIMARY KEY,
                    daily_limit_usd DECIMAL(10,4) DEFAULT 10.0,
                    monthly_limit_usd DECIMAL(10,4) DEFAULT 100.0,
                    current_daily_spend DECIMAL(10,4) DEFAULT 0.0,
                    current_monthly_spend DECIMAL(10,4) DEFAULT 0.0,
                    total_tokens_input BIGINT DEFAULT 0,
                    total_tokens_output BIGINT DEFAULT 0,
                    last_reset_date DATE DEFAULT CURRENT_DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create usage tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_usage_logs (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255),
                    model VARCHAR(100),
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    cost_usd DECIMAL(10,6),
                    request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_budgets(user_id)
                );
            """)
            
            conn.commit()
            conn.close()
            print("✅ Budget database tables created successfully")
            
        except Exception as e:
            print(f"❌ Database setup error: {e}")
    
    def create_user_budget(self, user_id: str, daily_limit: float = 10.0, monthly_limit: float = 100.0) -> bool:
        """Create or update user budget settings"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_budgets (user_id, daily_limit_usd, monthly_limit_usd)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    daily_limit_usd = EXCLUDED.daily_limit_usd,
                    monthly_limit_usd = EXCLUDED.monthly_limit_usd,
                    updated_at = CURRENT_TIMESTAMP;
            """, (user_id, daily_limit, monthly_limit))
            
            conn.commit()
            conn.close()
            print(f"✅ User budget created: {user_id} - Daily: ${daily_limit}, Monthly: ${monthly_limit}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating user budget: {e}")
            return False
    
    def check_user_budget(self, user_id: str, model: str, estimated_tokens: int = 1000) -> Dict:
        """Check if user can make request within budget"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Get user budget info
            cursor.execute("""
                SELECT daily_limit_usd, monthly_limit_usd, current_daily_spend, 
                       current_monthly_spend, last_reset_date
                FROM user_budgets WHERE user_id = %s;
            """, (user_id,))
            
            result = cursor.fetchone()
            if not result:
                # Create default budget for new user
                self.create_user_budget(user_id)
                daily_limit, monthly_limit, daily_spend, monthly_spend = 10.0, 100.0, 0.0, 0.0
                last_reset = datetime.now().date()
            else:
                daily_limit, monthly_limit, daily_spend, monthly_spend, last_reset = result
            
            # Reset daily spend if new day
            today = datetime.now().date()
            if last_reset < today:
                daily_spend = 0.0
                cursor.execute("""
                    UPDATE user_budgets 
                    SET current_daily_spend = 0.0, last_reset_date = CURRENT_DATE
                    WHERE user_id = %s;
                """, (user_id,))
                conn.commit()
            
            # Estimate cost for request
            if model in self.token_costs:
                estimated_cost = (estimated_tokens / 1000) * self.token_costs[model]["input"]
                estimated_cost += (estimated_tokens / 1000) * self.token_costs[model]["output"]
            else:
                estimated_cost = 0.01  # Default estimate
            
            # Check budget limits
            can_proceed = True
            reason = ""
            
            if daily_spend + estimated_cost > daily_limit:
                can_proceed = False
                reason = f"Daily budget exceeded: ${daily_spend:.4f} + ${estimated_cost:.4f} > ${daily_limit:.2f}"
            
            if monthly_spend + estimated_cost > monthly_limit:
                can_proceed = False
                reason = f"Monthly budget exceeded: ${monthly_spend:.4f} + ${estimated_cost:.4f} > ${monthly_limit:.2f}"
            
            conn.close()
            
            return {
                "can_proceed": can_proceed,
                "reason": reason,
                "daily_remaining": daily_limit - daily_spend,
                "monthly_remaining": monthly_limit - monthly_spend,
                "estimated_cost": estimated_cost,
                "current_daily_spend": float(daily_spend),
                "current_monthly_spend": float(monthly_spend)
            }
            
        except Exception as e:
            print(f"❌ Error checking budget: {e}")
            return {"can_proceed": False, "reason": f"Budget check error: {e}"}
    
    def track_usage(self, user_id: str, model: str, input_tokens: int, output_tokens: int) -> float:
        """Track actual usage and update budget"""
        try:
            # Calculate actual cost
            if model in self.token_costs:
                cost = (input_tokens / 1000) * self.token_costs[model]["input"]
                cost += (output_tokens / 1000) * self.token_costs[model]["output"]
            else:
                cost = 0.0
            
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Log usage
            cursor.execute("""
                INSERT INTO user_usage_logs (user_id, model, input_tokens, output_tokens, cost_usd)
                VALUES (%s, %s, %s, %s, %s);
            """, (user_id, model, input_tokens, output_tokens, cost))
            
            # Update user budget
            cursor.execute("""
                UPDATE user_budgets 
                SET current_daily_spend = current_daily_spend + %s,
                    current_monthly_spend = current_monthly_spend + %s,
                    total_tokens_input = total_tokens_input + %s,
                    total_tokens_output = total_tokens_output + %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s;
            """, (cost, cost, input_tokens, output_tokens, user_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Usage tracked: {user_id} - {model} - ${cost:.6f} ({input_tokens}+{output_tokens} tokens)")
            return cost
            
        except Exception as e:
            print(f"❌ Error tracking usage: {e}")
            return 0.0
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get user usage statistics"""
        try:
            conn = psycopg2.connect(self.database_url)
            cursor = conn.cursor()
            
            # Get budget info
            cursor.execute("""
                SELECT daily_limit_usd, monthly_limit_usd, current_daily_spend, 
                       current_monthly_spend, total_tokens_input, total_tokens_output
                FROM user_budgets WHERE user_id = %s;
            """, (user_id,))
            
            budget_result = cursor.fetchone()
            if not budget_result:
                return {"error": "User not found"}
            
            daily_limit, monthly_limit, daily_spend, monthly_spend, total_input, total_output = budget_result
            
            # Get recent usage
            cursor.execute("""
                SELECT model, SUM(input_tokens), SUM(output_tokens), SUM(cost_usd), COUNT(*)
                FROM user_usage_logs 
                WHERE user_id = %s AND request_timestamp >= NOW() - INTERVAL '7 days'
                GROUP BY model
                ORDER BY SUM(cost_usd) DESC;
            """, (user_id,))
            
            recent_usage = cursor.fetchall()
            
            conn.close()
            
            return {
                "user_id": user_id,
                "budget": {
                    "daily_limit": float(daily_limit),
                    "monthly_limit": float(monthly_limit),
                    "daily_spent": float(daily_spend),
                    "monthly_spent": float(monthly_spend),
                    "daily_remaining": float(daily_limit - daily_spend),
                    "monthly_remaining": float(monthly_limit - monthly_spend)
                },
                "usage": {
                    "total_input_tokens": int(total_input),
                    "total_output_tokens": int(total_output),
                    "total_tokens": int(total_input + total_output)
                },
                "recent_models": [
                    {
                        "model": row[0],
                        "input_tokens": int(row[1]),
                        "output_tokens": int(row[2]),
                        "cost": float(row[3]),
                        "requests": int(row[4])
                    } for row in recent_usage
                ]
            }
            
        except Exception as e:
            print(f"❌ Error getting user stats: {e}")
            return {"error": str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Initialize budget manager
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://llmproxy:bTBwUQHt7VTltFyB@34.136.3.30:5432/litellm")
    budget_manager = BudgetManager(DATABASE_URL)
    
    # Example: Create user budget
    budget_manager.create_user_budget("user123", daily_limit=5.0, monthly_limit=50.0)
    
    # Example: Check budget before request
    budget_check = budget_manager.check_user_budget("user123", "chatgpt-4o-latest", 1000)
    print("Budget check:", budget_check)
    
    # Example: Track usage after request
    if budget_check["can_proceed"]:
        cost = budget_manager.track_usage("user123", "chatgpt-4o-latest", 500, 200)
        print(f"Request cost: ${cost:.6f}")
    
    # Example: Get user statistics
    stats = budget_manager.get_user_stats("user123")
    print("User stats:", json.dumps(stats, indent=2))
