function valida_via(){
    var inputv = document.getElementById('inputVia').value.trim();
    if (inputv.length <= 3){
        alert("Minimo 3 caracteres en via de administracion");
        document.getElementById('via_span').innerText = "* al menos debe haber 3 caracteres en este campo";
        console.log(inputv.length)
        return false; 
    }else if (inputv.length > 100){
        alert("maximo 100 caracteres");
        console.log(inputv.length)
        return false;
    }
    console.log(inputv.length)
    return true;
}
function validar_txt() {
    var confarma = document.getElementById('textArea1').value.trim();
    if (confarma.length <= 3) {
        alert("empty box");
        console.log(confarma.length)
        return false;
    }else if (confarma.length > 500){
        alert("too much text");
        console.log(confarma.length)
        return false;
    }
    console.log(confarma.length)
    return true;
}
function valida_nom(){
    var inf = document.getElementById('inputNF').value.trim();
    if (inf.length == 0){
        console.log(inf.length)
        alert("nulo no permitido");
        
        return false; 
    }else if (inf.length > 100){
        console.log(inf.length)
        alert("maximo 100 caracteres");  
        return false;
    }
    return true;
}