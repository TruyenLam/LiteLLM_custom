#!/usr/bin/env python3
"""
LiteLLM Budget Middleware
Integrates budget checking into LiteLLM proxy
"""

import os
import json
import asyncio
from typing import Dict, Any
from budget_manager import BudgetManager

class LiteLLMBudgetMiddleware:
    def __init__(self):
        self.budget_manager = BudgetManager(
            database_url=os.getenv("DATABASE_URL")
        )
    
    async def pre_request_hook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called before each LiteLLM request
        Checks user budget and blocks if exceeded
        """
        try:
            # Extract user info from request
            user_id = self.extract_user_id(data)
            model = data.get("model", "unknown")
            
            # Estimate tokens from message content
            estimated_tokens = self.estimate_tokens(data)
            
            # Check budget
            budget_check = self.budget_manager.check_user_budget(
                user_id, model, estimated_tokens
            )
            
            if not budget_check["can_proceed"]:
                # Return error response
                return {
                    "error": {
                        "type": "budget_exceeded",
                        "message": budget_check["reason"],
                        "code": "BUDGET_EXCEEDED",
                        "details": {
                            "daily_remaining": budget_check["daily_remaining"],
                            "monthly_remaining": budget_check["monthly_remaining"],
                            "estimated_cost": budget_check["estimated_cost"]
                        }
                    }
                }
            
            # Store budget info for post-request tracking
            data["_budget_info"] = {
                "user_id": user_id,
                "model": model,
                "pre_check": budget_check
            }
            
            return data
            
        except Exception as e:
            print(f"❌ Budget middleware error: {e}")
            return data  # Allow request to proceed on error
    
    async def post_request_hook(self, data: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called after each LiteLLM request
        Tracks actual usage and updates budget
        """
        try:
            budget_info = data.get("_budget_info")
            if not budget_info:
                return response
            
            # Extract actual token usage from response
            usage = response.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            
            # Track usage
            actual_cost = self.budget_manager.track_usage(
                user_id=budget_info["user_id"],
                model=budget_info["model"],
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            # Add budget info to response
            response["budget_info"] = {
                "user_id": budget_info["user_id"],
                "cost": actual_cost,
                "daily_remaining": budget_info["pre_check"]["daily_remaining"] - actual_cost,
                "monthly_remaining": budget_info["pre_check"]["monthly_remaining"] - actual_cost
            }
            
            return response
            
        except Exception as e:
            print(f"❌ Post-request budget tracking error: {e}")
            return response
    
    def extract_user_id(self, data: Dict[str, Any]) -> str:
        """
        Extract user ID from request data
        Can be from API key, header, or default
        """
        # Try to get from headers (if passed by client)
        headers = data.get("headers", {})
        user_id = headers.get("x-user-id") or headers.get("user-id")
        
        if user_id:
            return user_id
        
        # Try to get from API key metadata (if using custom keys)
        api_key = headers.get("authorization", "").replace("Bearer ", "")
        if api_key and api_key != os.getenv("LITELLM_MASTER_KEY"):
            return f"key_{api_key[-8:]}"  # Use last 8 chars of API key
        
        # Default user
        return "default_user"
    
    def estimate_tokens(self, data: Dict[str, Any]) -> int:
        """
        Estimate token count from request content
        Simple approximation: 1 token ≈ 4 characters
        """
        try:
            messages = data.get("messages", [])
            total_chars = 0
            
            for message in messages:
                content = message.get("content", "")
                if isinstance(content, str):
                    total_chars += len(content)
                elif isinstance(content, list):
                    # Handle multi-modal content
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            total_chars += len(item.get("text", ""))
            
            # Add estimated tokens for response
            max_tokens = data.get("max_tokens", 1000)
            
            # Rough estimate: 4 chars per token
            estimated_tokens = (total_chars // 4) + max_tokens
            
            return min(estimated_tokens, 4000)  # Cap at reasonable limit
            
        except Exception as e:
            print(f"❌ Token estimation error: {e}")
            return 1000  # Default estimate

# Initialize middleware instance
budget_middleware = LiteLLMBudgetMiddleware()

# Hooks for LiteLLM to call
async def litellm_pre_call_hook(data):
    """LiteLLM pre-call hook"""
    return await budget_middleware.pre_request_hook(data)

async def litellm_post_call_hook(data, response):
    """LiteLLM post-call hook"""
    return await budget_middleware.post_request_hook(data, response)
