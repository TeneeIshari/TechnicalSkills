import csv
from graphics import *
from w2120297 import *

# Task D: Histogram Display using graphics.py
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.window = None
        
    def setup_window(self):
        """
        Sets up the graphics window for the histogram.
        """
        self.window = GraphWin("Histogram", 1300, 750)
        self.window.setBackground("#F2F4F4")

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        # Unpacking traffic data for two junctions (Elm and Hanley)
        total_vehicles_elm, total_vehicles_hanley = self.traffic_data

        # Adding a title to the histogram
        title = Text(Point(400, 88), f"Histogram of Vehicle Frequency per Hour ({self.date})")
        title.setSize(18)
        title.setStyle("bold")
        title.draw(self.window)

        # Constants for positioning and scaling
        left_margin = 75
        bottom_margin = 650
        bar_width = 25
        max_height = 450
        hour_spacing = 50
        scale_factor = max_height / max(max(total_vehicles_elm), max(total_vehicles_hanley))

        # Draw x-axis
        x_axis = Line(Point(left_margin, bottom_margin), Point(left_margin + 24 * hour_spacing, bottom_margin))
        x_axis.draw(self.window)

        # Add x-axis labels (hours 00 to 23)
        for i in range(24):
            hour_label = Text(Point(left_margin + i * hour_spacing + hour_spacing / 2 - 4, bottom_margin + 20), f"{i:02}")
            hour_label.draw(self.window)

        # Draw bars and display values
        for i in range(24):
            # Elm bar
            elm_height = total_vehicles_elm[i] * scale_factor
            elm_bar = Rectangle(
                Point(left_margin + i * hour_spacing, bottom_margin - elm_height),
                Point(left_margin + i * hour_spacing + bar_width - 4, bottom_margin)
            )
            elm_bar.setFill("#20948B")
            elm_bar.draw(self.window)

            elm_value = Text(Point(left_margin + i * hour_spacing + bar_width / 2 - 4, bottom_margin - elm_height - 10), str(total_vehicles_elm[i]))
            elm_value.setSize(8)
            elm_value.draw(self.window)

            # Hanley bar
            hanley_height = total_vehicles_hanley[i] * scale_factor
            hanley_bar = Rectangle(
                Point(left_margin + i * hour_spacing + bar_width + 4 - 7, bottom_margin - hanley_height),
                Point(left_margin + i * hour_spacing + 2 * bar_width - 7, bottom_margin)
            )
            hanley_bar.setFill("#6AB187")
            hanley_bar.draw(self.window)

            hanley_value = Text(Point(left_margin + i * hour_spacing + 1.5 * bar_width - 5, bottom_margin - hanley_height - 10), str(total_vehicles_hanley[i]))
            hanley_value.setSize(8)
            hanley_value.draw(self.window)

        # Add axis labels
        x_axis_label = Text(Point(left_margin + 12 * hour_spacing, bottom_margin + 50), "Hours 00:00 to 24.00")
        x_axis_label.setSize(10)
        x_axis_label.setStyle("bold")
        x_axis_label.draw(self.window)

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Elm Avenue/Rabbit Road legend
        elm_legend = Rectangle(Point(100, 160), Point(130, 180))
        elm_legend.setFill(color_rgb(0, 128, 128))
        elm_legend.draw(self.window)
        elm_label = Text(Point(220, 170), "Elm Avenue/Rabbit Road")
        elm_label.draw(self.window)

        # Hanley Highway/Westway legend
        hanley_legend = Rectangle(Point(100, 200), Point(130, 220))
        hanley_legend.setFill(color_rgb(144, 238, 144))
        hanley_legend.draw(self.window)
        hanley_label = Text(Point(220, 210), "Hanley Highway/Westway")
        hanley_label.draw(self.window)

    def run(self):
        """
        Runs the program to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()

        try:
            self.window.getMouse()  # Pause until click to close the window
        except GraphicsError:
            return  
        finally:
            self.window.close()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.file_paths = ['traffic_data15062024.csv', 'traffic_data16062024.csv', 'traffic_data21062024.csv']
        self.current_data = None

    def load_csv_file(self, file_path, date):
        """
        Loads a CSV file and processes its data.
        """
        # Initializing Counts for Elm and Hanley Junctions
        elm_hourly_count = [0] * 24
        hanley_hourly_count = [0] * 24

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) < 10 or row[1] != date:
                    continue

                hour = int(row[2][:2])
                if row[0].lower() == 'elm avenue/rabbit road':
                    elm_hourly_count[hour] += 1
                elif row[0].lower() == 'hanley highway/westway':
                    hanley_hourly_count[hour] += 1

        return [elm_hourly_count, hanley_hourly_count]

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        date = validate_date_input()  # Get date from user input
        formatted_date = date.replace("/", "")
        selected_file = None

        # Check for the matching CSV file based on formatted date
        for file_path in self.file_paths:
            if formatted_date in file_path:
                selected_file = file_path
                break
        else:
            print('No matching data file found.')
                

        if selected_file:
            # Load the traffic data for the selected file and date
            self.current_data = self.load_csv_file(selected_file, date)
            if self.current_data:
                # Process the CSV data (this function should return the processed outcomes)
                outcomes = process_csv_data(selected_file, date)  
                results_list = display_outcomes(selected_file, outcomes)  # Display the results
                for line in results_list:
                    print(line)
                save_results_to_file(results_list)  # Assuming save_results_to_file saves the outcomes
                # Run the histogram display with the loaded data
                app = HistogramApp(self.current_data, date)
                app.run()  # Display the histogram
            else:
                print(f"No data found for the selected date: {date}")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            self.handle_user_interaction()
            # Validate if the user wants to continue or quit
            if not validate_continue_input():
                break

if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
