"""Script to check database data and export to CSV."""
import asyncio
import csv
import sys
from datetime import datetime
from sqlalchemy import select
from app.database.connection import AsyncSessionLocal
from app.models.lead import Lead
from app.models.call import Call
from app.models.appointment import Appointment


async def check_database(output_file=None):
    """Check and display all data in the database as CSV.
    
    Args:
        output_file: Optional file path to save CSV. If None, prints to stdout.
    """
    try:
        async with AsyncSessionLocal() as session:
            # Get Leads
            result = await session.execute(select(Lead).order_by(Lead.created_at.desc()))
            leads = result.scalars().all()
            
            # Get Calls
            result = await session.execute(select(Call).order_by(Call.created_at.desc()))
            calls = result.scalars().all()
            
            # Get Appointments
            result = await session.execute(select(Appointment).order_by(Appointment.scheduled_time))
            appointments = result.scalars().all()
            
            # Determine output destination
            if output_file:
                f = open(output_file, 'w', newline='', encoding='utf-8')
                writer = csv.writer(f)
            else:
                f = sys.stdout
                writer = csv.writer(sys.stdout)
            
            # Output Leads CSV
            if output_file:
                f.write("=== LEADS ===\n")
            else:
                print("=== LEADS ===")
            
            if leads:
                writer.writerow([
                    "ID", "Name", "Email", "Phone", "Company", 
                    "Status", "Source", "Notes", "CRM ID", 
                    "Created At", "Updated At"
                ])
                for lead in leads:
                    writer.writerow([
                        lead.id,
                        lead.name or "",
                        lead.email or "",
                        lead.phone or "",
                        lead.company or "",
                        lead.status.value if lead.status else "",
                        lead.source or "",
                        lead.notes or "",
                        lead.crm_id or "",
                        lead.created_at.isoformat() if lead.created_at else "",
                        lead.updated_at.isoformat() if lead.updated_at else ""
                    ])
            else:
                if output_file:
                    f.write("No leads found\n")
                else:
                    print("No leads found")
            
            # Output Calls CSV
            if output_file:
                f.write("\n=== CALLS ===\n")
            else:
                print("\n=== CALLS ===")
            
            if calls:
                writer.writerow([
                    "ID", "Call ID (Vapi)", "Lead ID", "Direction", 
                    "Status", "Outcome", "Duration (seconds)", 
                    "Transcript", "Recording URL", "Started At", 
                    "Ended At", "Created At", "Updated At"
                ])
                for call in calls:
                    writer.writerow([
                        call.id,
                        call.call_id or "",
                        call.lead_id,
                        call.direction or "",
                        call.status.value if call.status else "",
                        call.outcome.value if call.outcome else "",
                        call.duration if call.duration else "",
                        call.transcript or "",
                        call.recording_url or "",
                        call.started_at.isoformat() if call.started_at else "",
                        call.ended_at.isoformat() if call.ended_at else "",
                        call.created_at.isoformat() if call.created_at else "",
                        call.updated_at.isoformat() if call.updated_at else ""
                    ])
            else:
                if output_file:
                    f.write("No calls found\n")
                else:
                    print("No calls found")
            
            # Output Appointments CSV
            if output_file:
                f.write("\n=== APPOINTMENTS ===\n")
            else:
                print("\n=== APPOINTMENTS ===")
            
            if appointments:
                writer.writerow([
                    "ID", "Lead ID", "Scheduled Time", "Status", 
                    "Calendar Event ID", "Notes", "Reminder Sent", 
                    "Created At", "Updated At"
                ])
                for apt in appointments:
                    writer.writerow([
                        apt.id,
                        apt.lead_id,
                        apt.scheduled_time.isoformat() if apt.scheduled_time else "",
                        apt.status.value if apt.status else "",
                        apt.calendar_event_id or "",
                        apt.notes or "",
                        apt.reminder_sent or "",
                        apt.created_at.isoformat() if apt.created_at else "",
                        apt.updated_at.isoformat() if apt.updated_at else ""
                    ])
            else:
                if output_file:
                    f.write("No appointments found\n")
                else:
                    print("No appointments found")
            
            # Summary
            summary = f"\n=== SUMMARY ===\nTotal Leads: {len(leads)}\nTotal Calls: {len(calls)}\nTotal Appointments: {len(appointments)}\n"
            if output_file:
                f.write(summary)
                f.close()
                print(f"Data exported to: {output_file}")
            else:
                print(summary)
            
    except Exception as e:
        print(f"[ERROR] Error checking database: {str(e)}", file=sys.stderr)
        print("\nMake sure:", file=sys.stderr)
        print("  1. PostgreSQL is running", file=sys.stderr)
        print("  2. DATABASE_URL in .env is correct", file=sys.stderr)
        print("  3. Database tables are created (run the app once to auto-create)", file=sys.stderr)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Export database data to CSV')
    parser.add_argument('-o', '--output', type=str, help='Output CSV file path (optional)')
    args = parser.parse_args()
    
    asyncio.run(check_database(output_file=args.output))

