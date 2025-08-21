#!/usr/bin/env python3
"""
Budget Management CLI Tool
Command line interface for managing user budgets
"""

import argparse
import json
import os
import sys
from budget_manager import BudgetManager

def main():
    parser = argparse.ArgumentParser(description='LiteLLM Budget Management CLI')
    parser.add_argument('--database-url', default=os.getenv('DATABASE_URL'), 
                       help='PostgreSQL database URL')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create user budget
    create_parser = subparsers.add_parser('create-user', help='Create user budget')
    create_parser.add_argument('user_id', help='User ID')
    create_parser.add_argument('--daily-limit', type=float, default=10.0, 
                              help='Daily spending limit in USD (default: 10.0)')
    create_parser.add_argument('--monthly-limit', type=float, default=100.0,
                              help='Monthly spending limit in USD (default: 100.0)')
    
    # Get user stats
    stats_parser = subparsers.add_parser('stats', help='Get user statistics')
    stats_parser.add_argument('user_id', help='User ID')
    
    # Check budget
    check_parser = subparsers.add_parser('check', help='Check user budget')
    check_parser.add_argument('user_id', help='User ID')
    check_parser.add_argument('--model', default='chatgpt-4o-latest', help='Model name')
    check_parser.add_argument('--tokens', type=int, default=1000, help='Estimated tokens')
    
    # Track usage
    track_parser = subparsers.add_parser('track', help='Track usage')
    track_parser.add_argument('user_id', help='User ID')
    track_parser.add_argument('model', help='Model name')
    track_parser.add_argument('input_tokens', type=int, help='Input tokens')
    track_parser.add_argument('output_tokens', type=int, help='Output tokens')
    
    # List all users
    list_parser = subparsers.add_parser('list-users', help='List all users with budgets')
    
    args = parser.parse_args()
    
    if not args.database_url:
        print("❌ Database URL not provided. Set DATABASE_URL environment variable or use --database-url")
        sys.exit(1)
    
    budget_manager = BudgetManager(args.database_url)
    
    if args.command == 'create-user':
        success = budget_manager.create_user_budget(
            args.user_id, args.daily_limit, args.monthly_limit
        )
        if success:
            print(f"✅ User budget created: {args.user_id}")
            print(f"   Daily limit: ${args.daily_limit:.2f}")
            print(f"   Monthly limit: ${args.monthly_limit:.2f}")
        else:
            print("❌ Failed to create user budget")
            sys.exit(1)
    
    elif args.command == 'stats':
        stats = budget_manager.get_user_stats(args.user_id)
        print(json.dumps(stats, indent=2))
    
    elif args.command == 'check':
        result = budget_manager.check_user_budget(args.user_id, args.model, args.tokens)
        print("Budget Check Result:")
        print(json.dumps(result, indent=2))
    
    elif args.command == 'track':
        cost = budget_manager.track_usage(
            args.user_id, args.model, args.input_tokens, args.output_tokens
        )
        print(f"✅ Usage tracked: ${cost:.6f}")
    
    elif args.command == 'list-users':
        # This would need additional database query
        print("Feature not implemented yet")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
