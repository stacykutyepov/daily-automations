This Python script generates a project plan based on tasks, effort in days, and specific days off for task owners. The script calculates the start and end dates for each task, accounting for weekends, and specified days off. The final output is a CSV file that includes the calculated dates and a summary of days off.

### Features:
Accepts a CSV file with tasks, effort, and owners.
Accepts a CSV file with days off for each owner.
Skips weekends.
Outputs a CSV file with the start date, end date, and a summary of the number of days off.

Example Output:
```
Task, Effort in Days, Owner, Start Date, End Date, Days Off
Task A, 5, Alice, 09/01/2024, 09/08/2024, 3 total days off
Task B, 3, Bob, 09/09/2024, 09/11/2024, 
Task C, 7, Alice, 09/12/2024, 09/21/2024, 1 total day off
```

### Example Command:
```python
python project_plan_generator.py --tasks tasks.csv --days-off days_off.csv --output-file tada.csv --start-date 09/01/2024
```
This command will generate a project plan based on the provided tasks, days off, and start date, saving the result to tada.csv.

If no start date is provided, the script will use today's date as the default start date.



