document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'local',
        expandRows: true,
        initialView: 'timeGridWeek', // Show month view by default
        height: "100%",
        weekends: true,
        slotMinTime: '08:00',
        slotMaxTime: '15:00',

        headerToolbar: {
            left: 'title',
            center: '',
            right: 'today prev,next'
        },


        // eventClick: function(info) {
        //     alert('Event: ' + info.event.title);
        //     alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);
        //     alert('View: ' + info.view.type);

        //     info.el.style.borderColor = 'red';
        // },

        //event data:
        events: '/time_blocks'
        
    });
    calendar.render();
});
