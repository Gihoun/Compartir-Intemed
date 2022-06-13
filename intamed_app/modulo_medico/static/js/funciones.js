
//Farmacos agregar filas, tambien elimina
function add_row() {
    var nombrefarmaco = document.getElementById("nombrefarmaco").value;
    var dosisfarmaco = document.getElementById("dosisfarmaco").value;
    var viafarmaco = document.getElementById("viafarmaco").value;
    var tablafarmaco = document.getElementById("tablaF");
    var tabla_len = (tablafarmaco.rows.length);
    var row = tablafarmaco.insertRow(tabla_len).outerHTML = '<tr id="row' + tabla_len + '"><td><input type="text" id="nombrefarmaco' + tabla_len + '" placeholder="Ingrese Fármaco"></td> <td><input type="string" id="dosisfarmaco' + tabla_len + '" placeholder="Ingrese Dosis"></td><td><select class="form-select" aria-label="Default select example" id="viafarmaco' + tabla_len + '"><option selected>Enteral</option><option value="1">Parenteral</option><option value="2">Tópica</option></select></td>    <td><button class="mt-1" type="button" id="eliminarFar' + tabla_len + '"  onclick="delete_row2(this)" ><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16"><path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z" /></svg></button></td>'
}
function add_row2() {         d
    var nombrefarmaco = document.getElementById("nombrefarmaco2").value;
    var dosisfarmaco = document.getElementById("dosisfarmaco2").value;
    var viafarmaco = document.getElementById("viafarmaco2").value;               
    var tablafarmaco = document.getElementById("tablaF2");
    var tabla_len = (tablafarmaco.rows.length);
    var row = tablafarmaco.insertRow(tabla_len).outerHTML = '<tr id="row' + tabla_len + '"><td><input type="text" id="nombrefarmaco' + tabla_len + '" placeholder="Ingrese Fármaco"></td> <td><input type="string" id="dosisfarmaco' + tabla_len + '" placeholder="Ingrese Dosis"></td><td><select class="form-select" aria-label="Default select example" id="viafarmaco' + tabla_len + '"><option selected>Enteral</option><option value="1">Parenteral</option><option value="2">Tópica</option></select></td>    <td><button class="mt-1" type="button" id="eliminarFar' + tabla_len + '"  onclick="delete_row2(this)" ><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16"><path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z" /></svg></button></td>'
    }
function delete_row2(botonE) {
    var fila = botonE.parentNode.parentNode;
    fila.parentNode.removeChild(fila);
}

// Atencion alergias
function validar_Alergia(id) {
    var Alergia = document.getElementById(id).value;
    document.getElementById('select_alergia').value = Alergia;
}
function detalle_Alergia() {
    var detalle = document.getElementById('select_alergia').value;
    var agregado = document.getElementById('inputDetalleA').value;
    if (detalle=='' && agregado == ''){
        alert('No ha seleccionado una alergia.')
    }else{
        document.getElementById('inputDetalleA').value = detalle+ ', '+ agregado;
    }
}
function borrar_Alergia() {
    document.getElementById('inputDetalleA').value = '';
    document.getElementById('inputDetalleA').innerHTML = '';
}
// Consulta alergias
function validar_Alergia2(id) {
    var Alergia = document.getElementById(id).value;
    document.getElementById('select_alergia2').value = Alergia;
}
function detalle_Alergia2() {
    var detalle = document.getElementById('select_alergia2').value;
    var agregado = document.getElementById('inputDetalleA2').value;
    if (detalle=='' && agregado == ''){
        alert('No ha seleccionado una alergia.')
    }else{
        document.getElementById('inputDetalleA2').value = detalle+ ', '+ agregado;
    }
}
function borrar_Alergia2() {
    document.getElementById('inputDetalleA2').value = '';
    document.getElementById('inputDetalleA2').innerHTML = '';
}
function desplegar_alergia() {
    var desplegado = document.getElementById('auto_completar').hidden
    if (desplegado == true){
        document.getElementById('auto_completar').hidden = false;
    } else {
        document.getElementById('auto_completar').hidden = true ;
        document.getElementById('auto_alergia').value = '';
        document.getElementById('select_alergia').value = '';
    }
}
function desplegar_alergia2() {
    var desplegado = document.getElementById('auto_completar2').hidden
    if (desplegado == true){
        document.getElementById('auto_completar2').hidden = false;
    } else {
        document.getElementById('auto_completar2').hidden = true ;
        document.getElementById('auto_alergia2').value = '';
        document.getElementById('select_alergia2').value = '';
    }
}

//Calendario no sacar por ahora ta weno para nuestros requisitos.
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
    dateFormat: 'dd/mm/yy',
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ''
};
$.datepicker.setDefaults($.datepicker.regional['es']);
$(function () {
    $("#fecha").datepicker();
});