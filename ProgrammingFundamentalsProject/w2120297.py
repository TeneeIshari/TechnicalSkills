#Author: Teneesha Alwis
#Date: 10.12.2024
#Student ID: 20231326

# Task A: Function used to validate the date  from the user
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
# Loop until the user enter a valid day between (1 - 31)
    while True: 
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if not 1 <= day <= 31:
                print("Out of range - values must be in the range 1 and 31.")
                continue
        except ValueError:
            print("Integer required.")
            continue
        break

# Loop until the user enter a valid month between (1 - 12)
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if not 1 <= month <= 12:
                print("Out of range - values must be in the range 1 to 12.")
                continue
        except ValueError:
            print("Integer required.")
            continue
        break

# Loop until the user enter a valid year between (2000 - 2024)
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if not 2000 <= year <= 2024:
                print("Out of range - values must range from 2000 and 2024.")
                continue
        except ValueError:
            print("Integer required.")
            continue
        break

# Formating the date as dd/MM/YYYY
    date = f"{day:02}/{month:02}/{year}"
    print(f"The date is {date}")
    return date

# Function to ask the user whether they want to continue loading another dataset or not.
def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        user_choice = input("Do you want to load another dataset? ('Y' to continue and 'N' to quit): ").strip().upper()
        if user_choice == "Y":
            return True
        elif user_choice == "N":
            return False
        else:
            print("Invalid Input. Please enter 'Y' or 'N'.")

# Task B: Function to process the CSV data
def process_csv_data(file_path, date):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
# Initializing variables in a dictionary 
    stats = {
        "total_vehicles": 0,
        "total_trucks": 0,
        "total_electric_vehicles": 0,
        "two_wheeled_vehicles": 0,
        "busses_north": 0,
        "no_turning_vehicles": 0,
        "over_speeding_vehicles": 0,
        "vehicles_elm_avenue": 0,
        "vehicles_hanley_highway": 0,
        "total_bicycles": 0,
        "total_scooters": 0,
        "peak_hour_vehicles": 0,
        "rain_hours": 0,
        "peak_hour_time": ""
    }
    
# List use to track vehicles count per hour (24 hours)
    peak_hours = [0 for _ in range(24)]
    
#List to track rain hours
    rain_hours_list = []

#Error handling used to open and process the csv file
    try:
        with open(file_path, 'r') as file:
            for line in file:
                row = line.strip().split(',')

                if len(row) < 10: # Skipping rows with insufficient data
                    continue
                
            # Process the row only if the date matches the input date
                if row[1] == date: 
                    stats["total_vehicles"] += 1  # Calculating total vehicles
                    
            # Calculating specific vehicle types
                    if row[8].lower() == 'truck':
                        stats["total_trucks"] += 1

                    if row[9].lower() == 'true':
                        stats["total_electric_vehicles"] += 1

                    if row[8].lower() in ['bicycle', 'motorcycle', 'scooter']:
                        stats["two_wheeled_vehicles"] += 1

                    if row[8].lower() == 'bicycle':
                        stats["total_bicycles"] += 1
                        
           # Count vehicles that are not turning left or right
                    if row[8].lower() == 'buss' and row[0].lower() == 'elm avenue/rabbit road' and row[4].upper() == 'N':
                        stats["busses_north"] += 1
                        
          # Count vehicles that are not turning left or right
                    if row[3].upper() == row[4].upper():
                        stats["no_turning_vehicles"] += 1
                        
          #Calculating over speeding vehicles
                    if int(row[7]) > int(row[6]):
                        stats["over_speeding_vehicles"] += 1
                        
           # Counting vehicles through Elm Avenue and Hanley Highway junctions
                    if row[0].lower() == 'elm avenue/rabbit road':
                        stats["vehicles_elm_avenue"] += 1

                    if row[0].lower() == 'hanley highway/westway':
                        stats["vehicles_hanley_highway"] += 1
                        
            # Counting scooters on Elm Avenue
                    if row[8].lower() == 'scooter' and row[0].lower() == 'elm avenue/rabbit road':
                        stats["total_scooters"] += 1
                        
            # Calculating rain hours
                    if row[5].lower()=='light rain' or row[5].lower()=='heavy rain':
                        hour = row[2][0:2]

                        if hour not in rain_hours_list:
                            rain_hours_list.append(hour)

                # Calculating vehicles per hour on Hanley Highway/Westway
                    if row[0].lower() == "hanley highway/westway":
                        hour = int(row[2][0:2])  # Extract the hour from the time (first 2 characters)
                        peak_hours[hour] += 1
                    
    except FileNotFoundError:
        print(f"File not found: {file_path}")

# Calculating average, percentage and other statistics
    stats["peak_hour_vehicles"] = max(peak_hours)
    stats["peak_hour_time"] = f"{peak_hours.index(stats['peak_hour_vehicles'])}:00 to {peak_hours.index(stats['peak_hour_vehicles']) + 1}:00"
    stats["percentage_trucks"] = (stats["total_trucks"] / stats["total_vehicles"] * 100) if stats["total_vehicles"] > 0 else 0
    stats["average_bicycles"] = (stats["total_bicycles"] / 24) if stats["total_bicycles"] > 0 else 0
    stats["percentage_scooters"] = ((stats["total_scooters"] *100)// stats["vehicles_elm_avenue"]) if stats["vehicles_elm_avenue"] > 0 else 0
    stats["rain_hours"] = len(rain_hours_list)

    return stats

# Function to display the processed outcomes in a readable format
def display_outcomes(file_path, outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    results = [
        f"Data file selected is {file_path}",
        f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}",
        f"The total number of trucks recorded for this date is {outcomes['total_trucks']}",
        f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}",
        f"The total number of two-wheeled vehicles for this date is {outcomes['two_wheeled_vehicles']}",
        f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['busses_north']}",
        f"The total number of Vehicles through both junctions not turning left or right is {outcomes['no_turning_vehicles']}",
        f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['percentage_trucks']:.0f}%",
        f"The average number of Bikes per hour for this date is {outcomes['average_bicycles']:.0f}",
        f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['over_speeding_vehicles']}",
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['vehicles_elm_avenue']}",
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['vehicles_hanley_highway']}",
        f"{outcomes['percentage_scooters']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
        f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_vehicles']}",
        f"The most vehicles recorded through Hanley Highway/Westway were recorded between {outcomes['peak_hour_time']}",
        f"The number of hours of rain for this date is {outcomes['rain_hours']}"
    ]
    return results

# Task C: Saving Results to a Text File
def save_results_to_file(results, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    try:
        # Open the file in append mode and write the results
        with open(file_name, "a") as file:
            for line in results:
                file.write(line + "\n")
            file.write("\n")
        print(f"Results saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving the results: {e}")


def main():
    # List of file paths containing traffic data (CSV files)
    file_paths = ['traffic_data15062024.csv', 'traffic_data16062024.csv', 'traffic_data21062024.csv']

    while True:
        # Validate and get the date input
        date = validate_date_input()
        formatted_date = f"{date[0:2]}{date[3:5]}{date[6:10]}"  # Format as DDMMYYYY

        # Process each file and match with the date
        file_found = False
        for file_path in file_paths:
            if formatted_date in file_path:  # Match the date with the filename
                file_found = True
                outcomes = process_csv_data(file_path, date)
                
                # Display the results of the processed data
                results_list = display_outcomes(file_path, outcomes)
                for line in results_list:
                    print(line)
                
                # Save results to a text file
                save_results_to_file(results_list)
                break  

        if not file_found:
            print(f"No matching file found for the date {date}.")

        # Check if the user wants to continue
        if not validate_continue_input():
            break

 # Call the main function to start the program
if __name__ == "__main__":
    main()

    


