document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'local',
        expandRows: true,
        initialView: 'timeGridWeek',
        height: "100%",
        weekends: false,
        slotMinTime: '08:00',
        slotMaxTime: '15:00',

        headerToolbar: {
            left: 'title',
            center: '',
            right: 'today prev,next'
        },

        eventClick: function(info) {
            alert('Event: ' + info.event.title);
            alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);
            alert('View: ' + info.view.type);

            info.el.style.borderColor = 'red';
        },


        //event data:
        // TODO: Come back to this moving on for now
        events: '/time_blocks'
    });
    calendar.render();
});