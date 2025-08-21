#!/usr/bin/env python3
"""
Custom Budget Tracker Callback
Replaces Prometheus metrics with custom budget tracking
"""

import os
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

class BudgetTrackerCallback:
    """Custom callback to track usage and budgets without enterprise features"""
    
    def __init__(self):
        self.usage_logs = []
        self.start_time = time.time()
        
    async def async_success_callback(
        self,
        kwargs: Dict[str, Any],
        completion_response: Dict[str, Any],
        start_time: float,
        end_time: float,
    ):
        """Called on successful requests"""
        try:
            # Extract request info
            model = kwargs.get("model", "unknown")
            user_id = self.extract_user_id(kwargs)
            
            # Extract usage from response
            usage = completion_response.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            
            # Calculate response time
            response_time = end_time - start_time
            
            # Create usage log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "response_time": response_time,
                "status": "success"
            }
            
            # Store log (in production, send to database)
            self.usage_logs.append(log_entry)
            
            # Track with budget manager if available
            try:
                from budget_manager import BudgetManager
                budget_manager = BudgetManager(os.getenv("DATABASE_URL"))
                cost = budget_manager.track_usage(user_id, model, input_tokens, output_tokens)
                log_entry["cost"] = cost
            except Exception as e:
                print(f"Budget tracking error: {e}")
            
            # Print usage info (replace with your logging system)
            print(f"✅ Request tracked: {user_id} - {model} - {total_tokens} tokens - {response_time:.3f}s")
            
        except Exception as e:
            print(f"❌ Success callback error: {e}")
    
    async def async_failure_callback(
        self,
        kwargs: Dict[str, Any],
        completion_response: Dict[str, Any],
        start_time: float,
        end_time: float,
    ):
        """Called on failed requests"""
        try:
            model = kwargs.get("model", "unknown")
            user_id = self.extract_user_id(kwargs)
            response_time = end_time - start_time
            
            # Log failure
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "model": model,
                "response_time": response_time,
                "status": "failure",
                "error": str(completion_response)
            }
            
            self.usage_logs.append(log_entry)
            print(f"❌ Request failed: {user_id} - {model} - {response_time:.3f}s")
            
        except Exception as e:
            print(f"❌ Failure callback error: {e}")
    
    def extract_user_id(self, kwargs: Dict[str, Any]) -> str:
        """Extract user ID from request"""
        # Try multiple sources for user ID
        headers = kwargs.get("headers", {})
        user_id = (
            headers.get("x-user-id") or 
            headers.get("user-id") or
            headers.get("X-User-ID") or
            kwargs.get("user_id") or
            "default_user"
        )
        return user_id
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        if not self.usage_logs:
            return {"message": "No usage data available"}
        
        total_requests = len(self.usage_logs)
        successful_requests = len([log for log in self.usage_logs if log["status"] == "success"])
        failed_requests = total_requests - successful_requests
        
        total_tokens = sum(log.get("total_tokens", 0) for log in self.usage_logs)
        avg_response_time = sum(log.get("response_time", 0) for log in self.usage_logs) / total_requests
        
        # Group by model
        model_stats = {}
        for log in self.usage_logs:
            model = log.get("model", "unknown")
            if model not in model_stats:
                model_stats[model] = {"requests": 0, "tokens": 0, "cost": 0.0}
            model_stats[model]["requests"] += 1
            model_stats[model]["tokens"] += log.get("total_tokens", 0)
            model_stats[model]["cost"] += log.get("cost", 0.0)
        
        return {
            "uptime_seconds": time.time() - self.start_time,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": successful_requests / total_requests if total_requests > 0 else 0,
            "total_tokens": total_tokens,
            "average_response_time": avg_response_time,
            "model_stats": model_stats
        }

# Global instance
budget_tracker = BudgetTrackerCallback()

# Functions that LiteLLM will call
async def budget_tracker_success_callback(kwargs, completion_response, start_time, end_time):
    """Success callback function for LiteLLM"""
    await budget_tracker.async_success_callback(kwargs, completion_response, start_time, end_time)

async def budget_tracker_failure_callback(kwargs, completion_response, start_time, end_time):
    """Failure callback function for LiteLLM"""
    await budget_tracker.async_failure_callback(kwargs, completion_response, start_time, end_time)

def get_budget_tracker_stats():
    """Get current statistics"""
    return budget_tracker.get_stats()
