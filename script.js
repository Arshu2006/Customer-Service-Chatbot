function sendMessage(){

let msg=document.getElementById("userInput").value;

fetch("/get",{

method:"POST",

headers:{
"Content-Type":"application/x-www-form-urlencoded"
},

body:"msg="+encodeURIComponent(msg)

})

.then(response=>response.json())

.then(data=>{

let chatbox=document.getElementById("chatbox");

chatbox.innerHTML +=
"<p><b>You:</b> "+msg+"</p>";

chatbox.innerHTML +=
"<p><b>Bot:</b> "+data.reply+"</p>";

document.getElementById("userInput").value="";

chatbox.scrollTop=chatbox.scrollHeight;

});

}