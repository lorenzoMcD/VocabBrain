// vocab matching game 5 words for terms and sentences/definitions
let data1 = document.getElementById("data1"); 
let data2 = document.getElementById("data2"); 
let data3 = document.getElementById("data3"); 
let data4 = document.getElementById("data4"); 
let data5 = document.getElementById("data5"); 



var customalert = document.getElementById("customAlert");



$(document).ready(function() {

  // EVENT HANDLER

  $("#clickme").click(function() {
    var useranswer1 = $("#sent1").val();
    var answertext = $("#answer1").val();

    var answertext2 = $("#answer2").val();
    var useranswer2 = $("#sent2").val();

    var answertext3 = $("#answer3").val();
    var useranswer3 = $("#sent3").val();


    var answertext4 = $("#answer4").val();
    var useranswer4 = $("#sent4").val();

    var answertext5 = $("#answer5").val();
    var useranswer5 = $("#sent5").val();

    var useranswer6 = $("#sent6").val();
    var answertext6 = $("#answer6").val();

    var answertext7 = $("#answer7").val();
    var useranswer7 = $("#sent7").val();

    var answertext8 = $("#answer8").val();
    var useranswer8 = $("#sent8").val();


    var answertext9 = $("#answer9").val();
    var useranswer9 = $("#sent9").val();

    var answertext10 = $("#answer10").val();
    var useranswer10 = $("#sent10").val();


    //$("#status").html(useranswer);

    if (answertext.toLowerCase() === useranswer1.toLowerCase()) {
      correct++;
      data1.style.color = "#0ead38";
      showOnScreen();
    }else{
      data1.style.color = "#EB1111"
    }


    if (answertext2.toLowerCase() === useranswer2.toLowerCase()){
      correct++;
      data2.style.color = "#0ead38";
      showOnScreen();
    }else{
      data2.style.color = "#EB1111"
    }

    if (answertext3.toLowerCase() === useranswer3.toLowerCase()){
      correct++;
     data3.style.color = "#0ead38";
      showOnScreen();
    }else{
      data3.style.color = "#EB1111"
    }

    if (answertext4.toLowerCase() === useranswer4.toLowerCase()){
      correct++;
      data4.style.color = "#0ead38";
      showOnScreen();
    }else{
      data4.style.color = "#EB1111"
    }

    if (answertext5.toLowerCase() === useranswer5.toLowerCase()){
      correct++;
      data5.style.color = "#0ead38";      
      showOnScreen();
    }else{
      data5.style.color = "#EB1111";
    }
    
    if (answertext6.toLowerCase() === useranswer6.toLowerCase()){
      correct++;
      data6.style.color = "#0ead38";      
      showOnScreen();
    }else{
      data6.style.color = "#EB1111";
    }
    
    if (answertext7.toLowerCase() === useranswer7.toLowerCase()){
      correct++;
      data7.style.color = "#0ead38";      
      showOnScreen();
    }else{
      data7.style.color = "#EB1111";
    }
    
    if (answertext8.toLowerCase() === useranswer8.toLowerCase()){
      correct++;
      data8.style.color = "#0ead38";      
      showOnScreen();
    }else{
      data8.style.color = "#EB1111";
    }
  
   if (answertext9.toLowerCase() === useranswer9.toLowerCase()){
      correct++;
      data9.style.color = "#0ead38";      
      showOnScreen();
    }else{
      data9.style.color = "#EB1111";
    }
   
   if (answertext10.toLowerCase() === useranswer10.toLowerCase()){
      correct++;
      data10.style.color = "#0ead38";      
      showOnScreen();
    }else{
      data10.style.color = "#EB1111";
    }




  });


});

// Defining correct answers and our button
let correct = 0
let clickme = document.getElementById("clickme");


//constant function that show and updates score
// Capping the score at 5
const showOnScreen = () => {
  document.getElementById("content").innerHTML = "You've scored "  + correct+ " out of 10!" ;
  correct = Math.min(Math.max(correct,0),9);


}

// Click submit - Submit button disabled, reset button enabled
const finish = () =>{
  let clickme = document.getElementById("clickme");
  let home = document.getElementById("home");
  let reset = document.getElementById("reset");
  clickme.disabled = true;
  reset.hidden = false;
  home.hidden= false;
  showCustom();

 
}


var customalert = document.getElementById("customAlert");

// Custom Alert function 
function showCustom(){
  customalert.style.display = 'block';
}

function hideCustom(){
  customalert.style.display = 'none';
}



//load our function


window.onload = showOnScreen
