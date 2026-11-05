(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");
    if (!calendarEl || typeof FullCalendar === "undefined") {
      return;
    }

    var eventsUrl = calendarEl.getAttribute("data-events-url");
    var addUrl = calendarEl.getAttribute("data-add-url");
    var modalEl = document.getElementById("addEventModal");
    var modal = modalEl ? new bootstrap.Modal(modalEl) : null;

    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      locale: "fa",
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek"
      },
      editable: false,
      selectable: true,
      navLinks: true,
      dayMaxEvents: true,
      events: eventsUrl,
      eventClick: function (info) {
        info.jsEvent.preventDefault();
        if (info.event.url) {
          window.location.href = info.event.url;
        }
      },
      select: function (info) {
        // پر کردن مقادیر شروع و پایان در Modal
        if (document.getElementById("eventStart")) {
          document.getElementById("eventStart").value = info.startStr;
        }
        if (document.getElementById("eventEnd")) {
          document.getElementById("eventEnd").value = info.endStr || "";
        }
        if (modal) {
          modal.show();
        }
      }
    });

    calendar.render();

    // اگر افزودن رویداد از طریق AJAX خواستید، این بخش را تغییر دهید.
    // در حالت پیش‌فرض، Modal رویداد جدید را با فرم POST به addUrl می‌فرستد
    // و صفحه reload می‌شود.
  });
})();