function konvertiraj(){
     var broj1 = parseInt(document.getElementById('broj1').value);
     var rez = document.getElementById('opcija').value;
 
     if(rez==='op1'){
        document.getElementById('rezultat').value=broj1*61,5;
     }
     if(rez==='op2'){
      document.getElementById('rezultat').value=broj1*57,5;
   }
   if(rez==='op3'){
      document.getElementById('rezultat').value=broj1*64,53;
   }
}