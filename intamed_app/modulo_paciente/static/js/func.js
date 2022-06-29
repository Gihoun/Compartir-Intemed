$.datepicker.regional['es'] = {
    closeText: 'Cerrar',
    prevText: '< Ant',
    nextText: 'Sig >',
    currentText: 'Hoy',
    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
    dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Juv', 'Vie', 'Sáb'],
    dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
    weekHeader: 'Sm',
    dateFormat: 'yy-mm-dd',
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ''
};
$.datepicker.setDefaults($.datepicker.regional['es']);
$(function () {
    $("#fechacalendar").datepicker({
         
    });
});
function confirmar(id){


    var inputd = document.getElementById('hor_sel').value.trim();
    const data = new FormData();
    var csrftoken = '{{ csrf_token }}';
    data.append('hor_sel',id);
          console.log(id);
          fetch('', {
            method: 'POST',
            body: data ,
            headers: {
              'X-CSRFToken': csrftoken ,
            }
    });

}
function confirmatio(id){
    Swal.fire({
      "title": "¿Esta Seguro?",
      "text": "Esta Acción es Irreversible",
      "icon": "question",
      "showCancelButton": true,
      "cancelButtonText": "No, Cancelar",
      "confirmButtonText": "Si, seguro",
      "reverseButtons": true,
      "confirmButtonColor": "#dc3545"
    })
    .then(function(result){
      if(result.isConfirmed){
        const data = new FormData();
        var csrftoken = '{{ csrf_token }}';
        data.append('hor_sel',id);
        console.log(id);
        fetch('modulo_paciente:indexPaciente', {
          method: 'POST',
          body: data ,
          headers: {
            'X-CSRFToken': csrftoken ,
          }
       });
       Swal.fire({
        "title": "Realizado",
        "text": "Colaborador Eliminado Exitosamente",
        "icon": "success"
      })
      .then(function(result){
        if(result.isConfirmed){
        window.location.href = "{% url 'userg' %}";
        }
      });
    }
  })   
  }