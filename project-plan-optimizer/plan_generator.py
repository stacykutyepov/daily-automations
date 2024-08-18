import csv
import datetime
import argparse
from dateutil import rrule


# Function to validate the CSV data
def validate_task_data(data):
    tasks = []
    for row in data:
        if len(row) < 3:
            raise ValueError("Each row must have at least three columns: task name, effort in days, and owner.")

        task_name = row[0].strip()
        try:
            duration = int(row[1].strip())
        except ValueError:
            raise ValueError("Second column should be an integer (effort in days).")

        owner = row[2].strip()
        if not isinstance(task_name, str) or not isinstance(owner, str):
            raise ValueError("First and third columns should be strings (task name and owner).")

        tasks.append((task_name, duration, owner))

    return tasks


# Function to parse days off
def parse_days_off(days_off_file):
    days_off = {}
    with open(days_off_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            owner = row[0].strip().lower()
            period = row[1].strip()
            if owner not in days_off:
                days_off[owner] = set()
            if '-' in period:
                start, end = period.split('-')
                start_date = datetime.datetime.strptime(start.strip(), "%m/%d/%Y")
                end_date = datetime.datetime.strptime(end.strip(), "%m/%d/%Y")
                days_off[owner].update(rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date))
            else:
                days_off[owner].add(datetime.datetime.strptime(period.strip(), "%m/%d/%Y"))
    return days_off


# Function to calculate start and end dates for each task
def generate_project_plan(tasks, days_off, start_date):
    project_plan = []

    current_date = start_date

    for task_name, duration, owner in tasks:
        owner_days_off = days_off.get(owner.lower(), set())
        total_days_off = 0

        # Find the next available start date
        while current_date.weekday() >= 5 or current_date in owner_days_off:
            if current_date in owner_days_off:
                total_days_off += 1
            current_date += datetime.timedelta(days=1)

        task_start_date = current_date

        # Calculate the end date, skipping weekends and days off
        work_days = 0
        while work_days < duration:
            current_date += datetime.timedelta(days=1)
            if current_date.weekday() < 5 and current_date not in owner_days_off:
                work_days += 1
            elif current_date in owner_days_off:
                total_days_off += 1

        end_date = current_date

        # Format the days off information
        days_off_comment = f"{total_days_off} total days off" if total_days_off > 0 else ""

        project_plan.append((task_name, duration, owner, task_start_date.strftime("%m/%d/%Y"),
                             end_date.strftime("%m/%d/%Y"), days_off_comment))

    return project_plan


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Generate a project plan from a task CSV file and days off CSV file.")
    parser.add_argument("--tasks", type=str, required=True, help="Path to the task CSV file.")
    parser.add_argument("--days-off", type=str, required=True, help="Path to the days off CSV file.")
    parser.add_argument("--output-file", type=str, required=True, help="Path to the output CSV file.")
    parser.add_argument("--start-date", type=str,
                        help="Start date of the project in the format MM/DD/YYYY. Default is today's date.",
                        default=datetime.datetime.today().strftime("%m/%d/%Y"))

    args = parser.parse_args()

    # Parse the start date
    start_date = datetime.datetime.strptime(args.start_date, "%m/%d/%Y")

    # Load and validate task data
    with open(args.tasks, 'r') as csvfile:
        reader = csv.reader(csvfile)
        tasks = validate_task_data(reader)

    # Parse days off from the days off file
    days_off = parse_days_off(args.days_off)

    # Generate the project plan
    project_plan = generate_project_plan(tasks, days_off, start_date)

    # Output the project plan to the specified CSV file
    with open(args.output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Task", "Effort in Days", "Owner", "Start Date", "End Date", "Days Off"])
        for row in project_plan:
            writer.writerow(row)

    print(f"Project plan has been generated and saved to {args.output_file}.")


if __name__ == "__main__":
    main()
