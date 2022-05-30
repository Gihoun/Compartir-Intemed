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

// Validaciones para Usuario
function val_rut(){
    var inf = document.getElementById('inputRut').value.trim();
    if (inf.length <= 6){
        console.log(inf.length)
        document.getElementById('rut_span').innerText = "* Campo Run debe tener 7 dígitos como mínimo";
        return false; 
    }else if (inf.length > 8){
        console.log(inf.length)
        document.getElementById('rut_span').innerText = "* Campo Run posee un máximo de 8 dígitos";  
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
function val_segn(){
    var inf = document.getElementById('inputSNom').value.trim();
    if (inf.length < 2){
        console.log(inf.length)
        document.getElementById('segn_span').innerText = "* Mínimo 2";
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
}
function val_apPaterno(){
    var inf = document.getElementById('inputAp').value.trim();
    if (inf.length < 2){
        console.log(inf.length)
        document.getElementById('ap_span').innerText = "* Mínimo 2";
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
        document.getElementById('am_span').innerText = "* Mínimo 2";
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
        document.getElementById('dir_span').innerText = "* Mínimo 5";
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
      document.getElementById('correo_span').innerText = "* correo invalido";
      document.form1.text1.focus();
  
      return false;
  
    }
  
  }
function val_fechanac(){
    var inf = document.getElementById('FechaNac').value;
    if (inf.length < 12){
        console.log(inf.length)
        document.getElementById('fnac_span').innerText = "* fecha invalida";
        return false; 
    }else if (inf.length > 12){
        console.log(inf.length)
        document.getElementById('fnac_span').innerText = "* fecha invalida";  
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
        document.getElementById('tel_span').innerText = "* Mínimo 5";
        return false; 
    }else if (inf.length > 12){
        console.log(inf.length)
        document.getElementById('tel_span').innerText = "*máximo 12 caracteres";  
        return false;
    }
    document.getElementById('tel_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}







