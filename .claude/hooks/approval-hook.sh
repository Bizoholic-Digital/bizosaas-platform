#!/bin/bash
# Enhanced Claude Approval Hook
# Supports both Telegram (online) and local notifications (offline)

HOOK_EVENT="$1"
PROJECT_NAME=$(basename "$(pwd)")
SHARED_DIR="/home/alagiri/projects/shared"

# Get the command being executed from environment variables
CLAUDE_COMMAND="${CLAUDE_USER_MESSAGE:-$HOOK_EVENT}"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> /tmp/claude_approval_log.txt
}

# Test internet connectivity to Telegram API
test_connectivity() {
    if timeout 5 curl -s "https://api.telegram.org/bot7200437482:AAF8aE2uymF5ukm-ntlEnXx1hfhX1Obcfaw/getMe" >/dev/null 2>&1; then
        return 0  # Online
    else
        return 1  # Offline
    fi
}

# Send approval request via Telegram (online mode)
send_telegram_approval() {
    local project="$1"
    local command="$2"
    
    log_message "Sending Telegram approval request for $project: $command"
    
    # Call the Telegram approval system
    python3 /home/alagiri/projects/claude-approval-system.py request "$project" "$command"
    return $?
}

# Send local approval request (offline mode)
send_local_approval() {
    local project="$1"
    local command="$2"
    
    log_message "Sending local approval request for $project: $command"
    
    # Use local notification system
    python3 /home/alagiri/projects/local-notification-system.py create "$project" "$command"
    
    # Get the request ID from the last created request
    local request_id=$(python3 -c "
import json, os
try:
    with open('/tmp/claude_approvals/pending_approvals.json', 'r') as f:
        approvals = json.load(f)
    print(approvals[-1]['id'] if approvals else '')
except:
    print('')
")
    
    if [ ! -z "$request_id" ]; then
        echo ""
        echo "🔔 APPROVAL REQUIRED - PROJECT: $project"
        echo "📋 Command: $command"
        echo "🆔 Request ID: $request_id"
        echo ""
        echo "To approve manually, run:"
        echo "  python3 /home/alagiri/projects/local-notification-system.py approve $request_id"
        echo ""
        echo "To see all pending approvals:"
        echo "  python3 /home/alagiri/projects/local-notification-system.py list"
        echo ""
        
        # Wait for approval or timeout (5 minutes)
        local timeout=300
        local elapsed=0
        
        while [ $elapsed -lt $timeout ]; do
            # Check if approval has been granted
            if python3 -c "
import json, os, sys
try:
    with open('/tmp/claude_approvals/approval_responses.json', 'r') as f:
        responses = json.load(f)
    for response in responses:
        if response.get('request_id') == '$request_id' and response.get('approved'):
            sys.exit(0)
    sys.exit(1)
except:
    sys.exit(1)
"; then
                echo "✅ Approval granted for request: $request_id"
                return 0
            fi
            
            sleep 5
            elapsed=$((elapsed + 5))
            
            # Show periodic reminder
            if [ $((elapsed % 60)) -eq 0 ]; then
                echo "⏱️  Still waiting for approval... (${elapsed}s elapsed)"
            fi
        done
        
        echo "❌ Approval timeout after ${timeout}s for request: $request_id"
        return 1
    else
        echo "❌ Failed to create approval request"
        return 1
    fi
}

# Main approval logic
main() {
    log_message "Approval hook triggered for $PROJECT_NAME with event: $HOOK_EVENT"
    
    # Skip approval for certain safe commands
    case "$CLAUDE_COMMAND" in
        *"read"*|*"list"*|*"status"*|*"help"*|*"--help"*)
            log_message "Skipping approval for safe command: $CLAUDE_COMMAND"
            exit 0
            ;;
    esac
    
    echo "🔐 Approval required for Claude command in project: $PROJECT_NAME"
    echo "📝 Command: $CLAUDE_COMMAND"
    echo ""
    
    # Test connectivity and choose appropriate method
    if test_connectivity; then
        echo "🌐 Online mode - sending Telegram approval request..."
        if send_telegram_approval "$PROJECT_NAME" "$CLAUDE_COMMAND"; then
            echo "✅ Telegram approval granted"
            exit 0
        else
            echo "❌ Telegram approval denied or failed"
            exit 1
        fi
    else
        echo "📶 Offline mode - using local approval system..."
        if send_local_approval "$PROJECT_NAME" "$CLAUDE_COMMAND"; then
            echo "✅ Local approval granted"
            exit 0
        else
            echo "❌ Local approval denied or timeout"
            exit 1
        fi
    fi
}

# Run main function
main "$@"