"""IT helpdesk ticket allocator: raise, assign, note, close and save tickets."""
import itertools
import json
import os
import re
import subprocess  # nosec B404
import sys
from datetime import datetime

tickets = {}
TICKET_IDS = itertools.count(101)
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket with urgency 1-5 and return its id."""
    priority = int(urgency)
    if not 1 <= priority <= 5:
        raise ValueError(f"Urgency must be between 1 and 5, got {priority}")
    if audit_trail is None:
        audit_trail = []
    ticket_id = next(TICKET_IDS)
    tickets[ticket_id] = {
        "user": user, "issue": issue_type, "priority": priority,
        "tech": None, "notes": [],
    }
    audit_trail.append(f"{user} raised #{ticket_id} at {datetime.now()}")
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign a technician to a ticket."""
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to a ticket, reporting if the ticket does not exist."""
    try:
        tickets[ticket_id]["notes"].append(note)
    except KeyError:
        print("Cannot add note: ticket", ticket_id, "does not exist")


def close_ticket(ticket_id, password):
    """Close (delete) a ticket if the admin password is correct."""
    if ADMIN_PASSWORD and password == ADMIN_PASSWORD:
        del tickets[ticket_id]
    else:
        print("Cannot close ticket", ticket_id, "- wrong password or not set")


def unresolved_high_priority():
    """Return ids of tickets with priority 4 or more and no technician."""
    result = []
    for ticket_id, ticket in tickets.items():
        if ticket["priority"] >= 4 and ticket["tech"] is None:
            result.append(ticket_id)
    return result


def ping_user_machine(hostname):
    """Ping a host once, after checking the hostname is safe."""
    if not re.fullmatch(r"[A-Za-z0-9.-]+", hostname) or hostname.startswith("-"):
        raise ValueError("Invalid hostname")
    count_flag = "-n" if sys.platform == "win32" else "-c"
    # Safe: no shell, fixed argument list, validated hostname.
    return subprocess.call(["ping", count_flag, "1", hostname])  # nosec B603 B607


def save_tickets(file="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(tickets))


def main():
    """Run the helpdesk demo."""
    t1 = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    try:
        raise_ticket("joe", "vpn", "-7")
    except ValueError as error:
        print("Ticket rejected:", error)
    t3 = raise_ticket("joe", "vpn", "2")
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())
    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ") or "3"
    try:
        raise_ticket("sana", "laptop", level)
    except ValueError as error:
        print("Ticket rejected:", error)
    close_ticket(t3, os.environ.get("HELPDESK_ADMIN_PASSWORD", ""))
    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()