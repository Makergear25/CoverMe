document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var blockForm = document.getElementById('block-form');
    var detailsContent = document.getElementById('details-content');
    var editForm = document.getElementById('edit-form');
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'local',
        expandRows: true,
        initialView: 'timeGridWeek', // Show month view by default
        height: "100%",
        weekends: true,
        slotMinTime: '08:00',
        slotMaxTime: '15:30',

        headerToolbar: {
            left: 'title',
            center: '',
            right: 'today prev,next'
        },

        eventClick: function(info) {
            // Only process clicks on block events (not day label events)
            if (info.event.allDay) {
                return; // Ignore clicks on all-day events (like day labels)
            }
            
            // Get event information
            const title = info.event.title;
            const blockNumber = title.replace('Block ', '');
            const startTime = info.event.start.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const endTime = info.event.end.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const timeRange = `${startTime} - ${endTime}`;
            const eventDate = info.event.start.toISOString().split('T')[0]; // Get date in YYYY-MM-DD format
            
            // Format the date for display in a more user-friendly format (MM/DD/YYYY)
            // Using a more direct approach to format the date
            const dateObj = new Date(info.event.start);
            const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
            const day = dateObj.getDate().toString().padStart(2, '0');
            const year = dateObj.getFullYear();
            const formattedDate = `${month}/${day}/${year}`;
            console.log("Formatting date:", dateObj, "->", formattedDate);
            
            // Show the form and hide the default content
            detailsContent.style.display = 'none';
            editForm.style.display = 'block';
            
            // Populate form fields
            document.getElementById('block-number').value = blockNumber;
            
            // Make sure the date field exists before setting its value
            const dateField = document.getElementById('date');
            if (dateField) {
                dateField.value = formattedDate;
                console.log("Date set to:", formattedDate); // Debug log
            } else {
                console.error("Date field not found in the form"); // Debug log
            }
            
            document.getElementById('time-range').value = timeRange;
            
            // Check if this event already has a coverage request (it will have the className 'needs-coverage')
            if (info.event.extendedProps.needs_coverage) {
                document.getElementById('name-input').value = info.event.extendedProps.teacher_name || '';
            } else {
                document.getElementById('name-input').value = '';
            }
            
            document.getElementById('name-input').focus();
            
            // Store the current event info for the form submission handler
            blockForm.dataset.blockNumber = blockNumber;
            blockForm.dataset.date = eventDate;
            blockForm.dataset.eventEl = info.el;
        },

        // The events are loaded from the server, which already includes information
        // about which blocks need coverage with the 'className' property set to 'needs-coverage'
        events: '/time_blocks'
    });
    
    // Handle form submission
    if (blockForm) {
        blockForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const blockNumber = document.getElementById('block-number').value;
            const teacherName = document.getElementById('name-input').value;
            const eventDate = this.dataset.date;
            
            if (!teacherName) {
                alert('Please enter your name.');
                return;
            }
            
            // Prepare the data to send to the server
            const requestData = {
                blockNumber: parseInt(blockNumber),
                teacherName: teacherName,
                date: eventDate
            };
            
            // Send the coverage request to the server
            fetch('api/request-coverage/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => {
                        throw new Error(errData.error || 'There was a problem with your request');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Coverage request saved:', data);
                
                // Instead of an alert, update the details content with a success message
                detailsContent.innerHTML = `<p class="success-message">Coverage requested for Block ${blockNumber}. Thank you!</p>`;
                
                // Hide the form and show the default content
                editForm.style.display = 'none';
                detailsContent.style.display = 'block';
                
                // Refresh the calendar to show the updated state
                calendar.refetchEvents();
            })
            .catch(error => {
                console.error('Error saving coverage request:', error);
                
                // Show error in the details panel instead of an alert
                detailsContent.innerHTML = `
                    <p class="error-message">
                        There was a problem saving your coverage request: ${error.message || 'Please try again'}
                    </p>
                    <button id="try-again-btn" class="retry-button">Try Again</button>
                `;
                
                // Hide the form and show the error content
                editForm.style.display = 'none';
                detailsContent.style.display = 'block';
                
                // Add event listener for try again button
                const tryAgainBtn = document.getElementById('try-again-btn');
                if (tryAgainBtn) {
                    tryAgainBtn.addEventListener('click', function() {
                        // Hide the default content and show the form again
                        detailsContent.style.display = 'none';
                        editForm.style.display = 'block';
                    });
                }
            });
        });
    }
    
    calendar.render();
});
