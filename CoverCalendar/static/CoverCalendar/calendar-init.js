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
        events: [
            {
                title: 'day #',
                start: '2025-03-24',
                end: '2025-03-24'
            },
            {
                title: 'Block #',
                start: '2025-03-24T08:00:00',
                end: '2025-03-24T08:45:00',
                allDay: false

            },
            {
                title: 'Block #',
                start: '2025-03-24T08:50:00',
                end: '2025-03-24T09:55:00',
                allDay: false

            },
            {
                title: 'Block #',
                start: '2025-03-24T10:40:00',
                end: '2025-03-24T11:55:00',
                allDay: false

            },
            {
                title: 'Block #',
                start: '2025-03-24T12:00:00',
                end: '2025-03-24T12:45:00',
                allDay: false

            },            {
                title: 'Block #',
                start: '2025-03-24T13:25:00',
                end: '2025-03-24T14:10:00',
                allDay: false

            },
            {
                title: 'Block #',
                start: '2025-03-24T14:15',
                end: '2025-03-24T15:00',
                allDay: false

            }
        ]
    });
    calendar.render();
});