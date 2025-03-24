function populateDates() {
    const dataSelect = document.getElementById('date');
    const year = 2024;
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];

            // Populate dropdown with dates
    for (let month = 0; month < 12; month++) {
        for (let day = 1; day <= new Date(year, month + 1, 0).getDate(); day++) {
            const dateString = `${months[month]} ${day}, ${year}`;
            const option = document.createElement('option');
            option.value = dateString;
            option.textContent = dateString;
            dataSelect.appendChild(option);
        }
    }
}

function populateTimes() {
    const timeSelect = document.getElementById('time');
    const times = [
        '08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', 
        '04:00 PM', '05:00 PM'
    ];

    // Populate dropdown with times
    times.forEach(time => {
        const option = document.createElement('option');
        option.value = time;
        option.textContent = time;
        timeSelect.appendChild(option);
    });
}

// Function to handle form submission
function submitAppointment() {
    const name = document.querySelector('input[name="username"]').value;
    const number = document.querySelector('input[name="number"]').value;
    const service = document.querySelector('input[name="service"]').value;
    const date = document.querySelector('select[name="date"]').value;
    const time = document.querySelector('select[name="time"]').value;

    if (name && number && service && date && time) {
        // Add date checking here
        const poyaDays = [
            '2024-01-01', '2024-01-25', '2024-02-22', 
            '2024-03-29', '2024-04-19', '2024-05-25',
            '2024-06-15', '2024-07-23', '2024-08-19',
            '2024-09-17', '2024-10-18', '2024-11-16',
            '2024-12-15'
        ];
        const publicHolidays = [
            '2024-01-01', '2024-02-04', '2024-04-14', 
            '2024-05-01', '2024-06-21', '2024-08-15',
            '2024-10-08', '2024-12-25'
        ];
        const formattedDate = formatDate(date);

        if (poyaDays.includes(formattedDate) || publicHolidays.includes(formattedDate)) {
            alert(`The selected date (${date}) is a Poya Day or Public Holiday. The salon is closed on this date.`);
        } else {
            alert(`Appointment booked for ${name} on ${date} at ${time}`);
        }
    } else {
        alert('Please fill out all fields.');
    }
}

// Function to format date to match the format in poyaDays and publicHolidays arrays
function formatDate(dateString) {
    const dateParts = dateString.split(' ');
    const month = dateParts[0];
    const day = dateParts[1].replace(',', '');
    const year = dateParts[2];
    const months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
        'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
        'November': '11', 'December': '12'
    };
    return `${year}-${months[month]}-${day.padStart(2, '0')}`;
}

// Initialize dropdowns
populateDates();
populateTimes();
