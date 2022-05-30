function valida_via(){
    var inputv = document.getElementById('inputVia').value.trim();
    if (inputv.length <= 3){
        document.getElementById('via_span').innerText = "* al menos debe haber 3 caracteres en este campo";
        console.log(inputv.length)
        return false; 
    }else if (inputv.length > 99){
        document.getElementById('via_span').innerText = "* maximo 100 caracteres";
        console.log(inputv.length)
        return false;
    }
    document.getElementById('via_span').innerText = "*";
    console.log(inputv.length)
    return true;
}
function validar_txt() {
    var confarma = document.getElementById('textArea1').value.trim();
    if (confarma.length <= 3) {
        document.getElementById('contra_span').innerText = "* al menos debe haber 3 caracteres en este campo";
        console.log(confarma.length)
        return false;
    }else if (confarma.length > 499){
        document.getElementById('contra_span').innerText = "* maximo 500 caracteres";
        console.log(confarma.length)
        return false;
    }
    document.getElementById('contra_span').innerText = "*";
    console.log(confarma.length)
    return true;
}
function valida_nom(){
    var inf = document.getElementById('inputNF').value.trim();
    if (inf.length <= 3){
        console.log(inf.length)
        document.getElementById('nom_span').innerText = "* al menos debe haber 3 caracteres en este campo";
        return false; 
    }else if (inf.length > 99){
        console.log(inf.length)
        document.getElementById('nom_span').innerText = "* maximo 100 caracteres";  
        return false;
    }
    document.getElementById('nom_span').innerText = "*"; 
    console.log(inf.length)
    return true;
}