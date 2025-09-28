#!/bin/bash
# Claude Code Notification Hook
# Provides sound notifications for various Claude events

HOOK_EVENT="$1"
HOOK_DATA="$2"

# Function to play notification sound (WSL-compatible)
play_notification_sound() {
    local sound_type="$1"
    
    case "$sound_type" in
        "approval")
            # Double beep for approval requests
            echo -e "\a"; sleep 0.3; echo -e "\a"
            # Also use PowerShell for better Windows sound
            powershell.exe -c "[System.Media.SystemSounds]::Question.Play()" 2>/dev/null
            ;;
        "completion")
            # Triple ascending beep for task completion
            echo -e "\a"; sleep 0.2; echo -e "\a"; sleep 0.2; echo -e "\a"
            powershell.exe -c "[System.Media.SystemSounds]::Asterisk.Play()" 2>/dev/null
            ;;
        "error")
            # Single long beep for errors
            echo -e "\a"; sleep 1
            powershell.exe -c "[System.Media.SystemSounds]::Hand.Play()" 2>/dev/null
            ;;
        "attention")
            # Single clear beep
            echo -e "\a"
            powershell.exe -c "[System.Media.SystemSounds]::Beep.Play()" 2>/dev/null
            ;;
    esac
}

# Function to send desktop notification
send_desktop_notification() {
    local title="$1"
    local message="$2"
    local sound_type="$3"
    
    # Try different notification methods
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "$title" "$message"
    elif command -v osascript >/dev/null 2>&1; then
        # macOS notification
        osascript -e "display notification \"$message\" with title \"$title\" sound name \"Glass\""
    else
        # Fallback to PowerShell on Windows/WSL
        powershell.exe -c "
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.MessageBox]::Show('$message', '$title', 'OK', 'Information')
        " 2>/dev/null &
    fi
    
    play_notification_sound "$sound_type"
}

# Log notification
log_notification() {
    local event="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] CLAUDE NOTIFICATION: $event - $message" >> ~/.claude/notification.log
}

# Handle different hook events
case "$HOOK_EVENT" in
    "user_prompt_submit")
        send_desktop_notification "Claude Code" "Processing your request..." "attention"
        log_notification "REQUEST_START" "User submitted prompt"
        ;;
    "tool_call_start")
        # Only notify for certain tools that might need attention
        if echo "$HOOK_DATA" | grep -q "approval\|permission"; then
            send_desktop_notification "Claude Code" "Approval required - Check terminal" "approval"
            log_notification "APPROVAL_REQUEST" "Claude needs approval"
        fi
        ;;
    "session_complete")
        send_desktop_notification "Claude Code" "Task completed successfully!" "completion"
        log_notification "TASK_COMPLETE" "Claude processing finished"
        ;;
    "error_occurred")
        send_desktop_notification "Claude Code" "An error occurred - Check terminal" "error"
        log_notification "ERROR" "Error during Claude processing"
        ;;
    *)
        # Default notification for any other event
        send_desktop_notification "Claude Code" "Event: $HOOK_EVENT" "attention"
        log_notification "OTHER" "$HOOK_EVENT"
        ;;
esac

# Print notification to terminal as well
echo ""
echo "🔔 CLAUDE NOTIFICATION: $HOOK_EVENT"
echo "   Time: $(date '+%Y-%m-%d %H:%M:%S')"
if [ -n "$HOOK_DATA" ]; then
    echo "   Data: $HOOK_DATA"
fi
echo "═══════════════════════════════════════════════"
echo ""