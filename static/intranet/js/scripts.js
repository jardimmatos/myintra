function CopyPass(passw){
    console.log('copyPasss')
    var temp_text = document.createElement("input");
    temp_text.value = passw;
    document.body.appendChild(temp_text);
    temp_text.select();
    
    document.execCommand("copy");
    document.body.removeChild(temp_text);
    
    alert("Copied the text: " + temp_text.value);
}