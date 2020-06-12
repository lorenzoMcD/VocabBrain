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
      data5.style.color = "#EB1111"
    }


  });


});

// Defining correct answers and our button
let correct = 0
let clickme = document.getElementById("clickme");
let back = document.getElementById("back"); 


//constant function that show and updates score
// Capping the score at 5
const showOnScreen = () => {
  document.getElementById("content").innerHTML = "You've scored "  + correct+ " out of 5!" ;
  correct = Math.min(Math.max(correct,0),4);


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
