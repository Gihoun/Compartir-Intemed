//Farmacos agregar filas farmacos habituales de Pacientes
function add_row(x) {
    var tablafarmaco =  document.getElementById(x).getElementsByTagName('tbody')[0];
    var lenT = (tablafarmaco.rows.length);
    var row = tablafarmaco.insertRow(lenT);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);


    cell1.innerHTML='<input type="text" id="inputNfarmaco'+lenT+'" placeholder="Ingrese Fármaco" name="inputNfarmaco" oninput="auto_farma(this.id)">'
    cell2.innerHTML='<input type="text" id="inputDfarmaco'+lenT+'" placeholder="Ingrese Dosis" name="inputDfarmaco">'
    cell3.innerHTML='<input type="text" id="inputVfarmaco'+lenT+'" placeholder="Ingrese Via Adminsitración" name="inputVfarmaco">'
    cell4.innerHTML='<button class="mt-3" type="button" id="eliminarFar" onclick="delRow(this)"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16"><path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z" /></svg></button>'
    
}

function delRow(e) {
    e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
}

function refresh_Farma(x){
    var tablafarmaco =  document.getElementById(x).getElementsByTagName('tbody')[0];
    var farmaname0 = document.getElementById('inputNfarmaco').value
    var farmadosis0 = document.getElementById('inputDfarmaco').value
    var farmaadmin0 = document.getElementById('inputVfarmaco').value
  
    var texto_medH = farmaname0+' '+farmadosis0+' '+farmaadmin0
    for (let index = 1; index < tablafarmaco.rows.length; index++) {
        var farmaname0 = document.getElementById('inputNfarmaco'+index).value
        var farmadosis0 = document.getElementById('inputDfarmaco'+index).value
        var farmaadmin0 = document.getElementById('inputVfarmaco'+index).value
        var texto_medH =texto_medH+' | '+farmaname0+' '+farmadosis0+' '+farmaadmin0
   }
   document.getElementById('inputHabmed').value=texto_medH
}

// Calculo del IMC //////////////////////////////////////////////////////////////
function roundUp(num, precision) {
    precision = Math.pow(10, precision)
    return Math.ceil(num * precision) / precision
}

function cal_imc() {
    var peso = document.getElementById("inputPeso").value
    var talla = document.getElementById("inputTalla").value            
    if (talla > 0 && peso > 0) {
        var imc = (peso)/((talla/100)*(talla/100))
        document.getElementById("inputIMC").value = roundUp(imc, 2)
    } else
        document.getElementById("inputIMC").value = 0
}
function cal_imc2() {
    var peso = document.getElementById("inputPeso2").value
    var talla = document.getElementById("inputTalla2").value               
    if (talla > 0 && peso > 0) {
        var imc = (peso)/((talla/100)*(talla/100))
        document.getElementById("inputIMC2").value = roundUp(imc, 2)
    } else
        document.getElementById("inputIMC2").value = 0
}
//////////////////////////////////////////////////////////////////////

// Atencion alergias
function validar_Alergia(id) {
    var Alergia = document.getElementById(id).value;
    document.getElementById('select_alergia').value = Alergia;
}
function detalle_Alergia() {
    var detalle = document.getElementById('select_alergia').value;
    var agregado = document.getElementById('inputDetalleA').value;
    if (detalle == '' && agregado == ''){
        alert('No ha seleccionado una alergia.')
    }else{
        document.getElementById('inputDetalleA').value = detalle+ ' ' + agregado;
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
    $("#fecha").datepicker({
        multidate: true
    });
});


$(function() {
    moment.locale('es');
    $('#fechita').daterangepicker({
      "minDate": moment(),
      "maxSpan": {
          "days": 4
      },
      "locale": {
        "daysOfWeek": [
            "Dom",
            "Lun",
            "Mar",
            "Mier",
            "Jue",
            "Vie",
            "Sab"
        ],
      }
    }, function(start, end, label) {
      
      console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
      var $days = end.diff(start, 'days');
      console.log($days);
      var arr_horas = ["08-00","08-15","08-30","08-45","09-00","09:15","09:30","09:45","10-00","10:15","10:30","10:45","11-00","11:15","11:30","11:45","12-00","12:15","12:30","12:45","13-00","13:15","13:30","13:45","14-00","14:15","14:30","14:45","15-00","15:15","15:30","15:45","16-00","16:15","16:30","16:45","17-00","17:15","17:30","17:45","18-00"];
      for (var i = 0; i <= $days; i++) {
        
        var $item = $('<div class="accordion-item" id="aco_item'+i+'">'+'<h2 class="accordion-header" id="jjj">'+'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-'+i+'" aria-expanded="false" aria-controls="flush-collapseOne"><input type="label" class="badge badge-pill badge-info" name="'+start.format('dd')+'" value="'+start.format('YYYY-MM-DD')+'" >'+start.format('dddd DD - MMMM')+'</button></h2>'+'</div>');
        var $acob = $('<div id="flush-'+i+'" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlush"> <div class="accordion-body overflow-auto" style="max-height: 300px;"> <ul class="list-group" id="li'+i+'" ></ul></div></div>');
        var $ids = 'li'+i ;
        var $acoit = 'aco_item' + i ;
        
        $('#accordionFlush').append($item);
        $('#'+$acoit).append($acob);
        
        for (var p = 0; p < arr_horas.length; p++) {
            var $horas = $('<li class="list-group-item">'+ '<input class="form-check-input me-1" type="checkbox" name="'+start.format('dd')+'" value="'+arr_horas[p]+'" aria-label="...">'+arr_horas[p]+'</li>');
            
            $('#'+ $ids).append($horas);
        }
        var $ext = $()
        
        $vd = start.add(1,'days');
        console.log(start.format('dd'));
        
        
      }
      
      
    });

    $('#fechita').on('apply.daterangepicker', function(ev, picker) {
    $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
        document.getElementById("fechita").style.visibility = "hidden";
        document.getElementById("boton").style.visibility = "visible";
        var $el = $('<button id="boton1" class="btn btn-outline-secondary">reiniciar</button>').click(function () { window.location.href = ""; $(this).parent().detach();});
        $('#reinicio').append($el);
        
        });

    $('input[name="datefilter"]').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});
  });

// Validaciones para Farmacos
function valida_via(){
    var inputv = document.getElementById('inputVia').value.trim();
    if (inputv.length <= 2){
        document.getElementById('via_span').innerText = "* Al menos debe haber 3 caracteres en este campo";
        console.log(inputv.length)
        return false; 
    }else if (inputv.length > 99){
        document.getElementById('via_span').innerText = "* Máximo 100 caracteres";
        console.log(inputv.length)
        return false;
    }
    document.getElementById('via_span').innerText = "*";
    console.log(inputv.length)
    return true;
}
function validar_txt() {
    var confarma = document.getElementById('textArea1').value.trim();
    if (confarma.length <= 2) {
        document.getElementById('contra_span').innerText = "* Al menos debe haber 3 caracteres en este campo";
        console.log(confarma.length)
        return false;
    }else if (confarma.length > 499){
        document.getElementById('contra_span').innerText = "* Máximo 500 caracteres";
        console.log(confarma.length)
        return false;
    }
    document.getElementById('contra_span').innerText = "*";
    console.log(confarma.length)
    return true;
}
function valida_nom(){
    var inf = document.getElementById('inputNF').value.trim();
    if (inf.length <= 2){
        console.log(inf.length)
        document.getElementById('nom_span').innerText = "* Al menos debe haber 3 caracteres en este campo";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('nom_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('nom_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}

// Validaciones para Perfiles
function val_nom_per(){
    var inf = document.getElementById('inputNombrePerfil').value.trim();
    if (inf.length <= 2){
        console.log(inf.length)
        document.getElementById('nom_span').innerText = "* Al menos debe haber 3 caracteres en este campo";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('nom_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('nom_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}

// Validaciones para Colaboradores (Usuarios) & Pacientes
function val_rut(){
    var inf = document.getElementById('inputRut').value.trim();
    if (inf.length <= 6){
        console.log(inf.length)
        document.getElementById('rut_span').innerText = "* 7 Dígitos Mínimo";
        return false; 
    }else if (inf.length > 8){
        console.log(inf.length)
        document.getElementById('rut_span').innerText = "* Máximo de 8 Dígitos";  
        return false;
    }
    document.getElementById('rut_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_dv(){
    var inf = document.getElementById('inputDV').value.trim();
    if (inf.length < 1){
        console.log(inf.length)
        document.getElementById('dv_span').innerText = "* Mínimo 1";
        return false; 
    }else if (inf.length > 1){
        console.log(inf.length)
        document.getElementById('dv_span').innerText = "* Campo DV posee un máximo de 1 caracter";  
        return false;
    }
    document.getElementById('dv_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_primn(){
    var inf = document.getElementById('inputPNom').value.trim();
    if (inf.length < 2){
        console.log(inf.length)
        document.getElementById('primn_span').innerText = "* Mínimo 2 caracteres";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('primn_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('primn_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
/* function val_segn(){
    var inf = document.getElementById('inputSNom').value.trim();
    if (inf.length < 2){
        console.log(inf.length)
        document.getElementById('segn_span').innerText = "* Mínimo 2 caracteres";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('segn_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('segn_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_nomsoc(){
    var inf = document.getElementById('inputNomSoc').value.trim();
    if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('nomsoc_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('nomsoc_span').innerText = "*"; 
    console.log(inf.length)
    return true;
} */
function val_apPaterno(){
    var inf = document.getElementById('inputAp').value.trim();
    if (inf.length < 2){
        console.log(inf.length)
        document.getElementById('ap_span').innerText = "* Mínimo 2 caracteres";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('ap_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('ap_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_apMaterno(){
    var inf = document.getElementById('inputAM').value.trim();
    if (inf.length < 2){
        console.log(inf.length)
        document.getElementById('am_span').innerText = "* Mínimo 2 caracteres";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('am_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('am_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_direccion(){
    var inf = document.getElementById('inputDir').value.trim();
    if (inf.length < 5){
        console.log(inf.length)
        document.getElementById('dir_span').innerText = "* Mínimo 5 caracteres";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('dir_span').innerText = "* Máximo 100 caracteres";  
        return false;
    }
    document.getElementById('dir_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function ValidateEmail() {
    var email = document.getElementById('inputCorreo').value;
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (email.match(validRegex)) {
        document.getElementById('correo_span').innerText = "*";
      document.form1.text1.focus();
      return true;
    } else {
      document.getElementById('correo_span').innerText = "* Correo No Válido";
      document.form1.text1.focus();
      return false;
    }
  }
function val_fechanac(){
    var inf = document.getElementById('fecha').value;
    if (inf.length < 12){
        console.log(inf.length)
        document.getElementById('fnac_span').innerText = "* Fecha Inválida";
        return false; 
    }else if (inf.length > 12){
        console.log(inf.length)
        document.getElementById('fnac_span').innerText = "* Fecha Inválida";  
        return false;
    }
    document.getElementById('fnac_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_telefono(){
    var inf = document.getElementById('inputFono').value.trim();
    if (inf.length < 5){
        console.log(inf.length)
        document.getElementById('tel_span').innerText = "* Mínimo 5 Dígitos";
        return false; 
    }else if (inf.length > 12){
        console.log(inf.length)
        document.getElementById('tel_span').innerText = "*Máximo 12 Dígitos";  
        return false;
    }
    document.getElementById('tel_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_fechaing(){
    var inf = document.getElementById('inputFechaIngreso').value;
    if (inf.length < 12){
        console.log(inf.length)
        document.getElementById('fing_span').innerText = "* Fecha Inválida";
        return false; 
    }else if (inf.length > 12){
        console.log(inf.length)
        document.getElementById('fing_span').innerText = "* Fecha Inválida";  
        return false;
    }
    document.getElementById('fing_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_sueldo(){
    var inf = document.getElementById('inputSueldo').value.trim();
    if (inf.length < 1){
        console.log(inf.length)
        document.getElementById('sueldo_span').innerText = "* 1 Dígito Mínimo";
        return false; 
    }else if (inf.length > 9){
        console.log(inf.length)
        document.getElementById('sueldo_span').innerText = "* Máximo de 9 Dígitos";  
        return false;
    }
    document.getElementById('sueldo_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}
function val_hrs(){
    var inf = document.getElementById('inputRegimenHrs').value.trim();
    if (inf.length < 1){
        console.log(inf.length)
        document.getElementById('hrs_span').innerText = "* 1 Dígito Mínimo";
        return false; 
    }else if (inf.length > 3){
        console.log(inf.length)
        document.getElementById('hrs_span').innerText = "* Máximo de 3 Dígitos";  
        return false;
    }
    document.getElementById('hrs_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}