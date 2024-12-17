document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");
  const dateField = document.querySelector('input[name="date"]');
  const timeSlots = document.querySelectorAll(".time-slot");

  if (calendarEl) {
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      locale: "ru",
      dateClick: function (info) {
        dateField.value = info.dateStr;
        fetchBookedSlots(info.dateStr);

        // Подсветка выбранной даты
        document.querySelectorAll(".fc-daygrid-day").forEach((dayEl) => {
          dayEl.classList.remove("fc-day-selected");
        });
        info.dayEl.classList.add("fc-day-selected");
      },
    });

    calendar.render();
  }

  function fetchBookedSlots(date) {
    fetch(`/get_booked_slots/${date}`)
      .then((response) => response.json())
      .then((data) => {
        const bookedTimes = data.booked_times;
        timeSlots.forEach((slot) => {
          if (bookedTimes.includes(slot.dataset.value)) {
            slot.classList.add("disabled");
            slot.classList.remove("selected");
          } else {
            slot.classList.remove("disabled");
          }
        });
      });
  }

  timeSlots.forEach((slot) => {
    slot.addEventListener("click", function () {
      if (!this.classList.contains("disabled")) {
        timeSlots.forEach((s) => s.classList.remove("selected"));
        this.classList.add("selected");
        const timeField = document.querySelector('input[name="time"]');
        timeField.value = this.dataset.value;
      }
    });
  });
});