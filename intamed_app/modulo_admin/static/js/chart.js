var ctxL = document.getElementById("lineChart").getContext('2d');

var abr = document.getElementById("Abril").value;
var may = document.getElementById("Mayo").value;
var jun = document.getElementById("Junio").value;
var jul = document.getElementById("Julio").value;
var myLineChart = new Chart(ctxL, {
  type: 'line',
  data: {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
      label: "Atenciones concertadas",
      data: [ene, feb, mar, abr, may, jun, jul],
      backgroundColor: [
        'rgba(105, 0, 132, .2)',
      ],
      borderColor: [
        'rgba(200, 99, 132, .7)',
      ],
      borderWidth: 2
    },
    {
      label: "Atenciones canceladas",
      data: [0, 5, 20, 19, 13, 3, 22],
      backgroundColor: [
        'rgba(0, 137, 132, .2)',
      ],
      borderColor: [
        'rgba(0, 10, 130, .7)',
      ],
      borderWidth: 2
    }
    ]
  },
  options: {
    responsive: true
  }
});