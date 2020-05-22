// script.js
$(document).ready(function() {

  // EVENT HANDLER

// will have to set certain amnt of vars to play game...
// game only works for two terms right now

  $("#clickme").click(function() {
    var useranswer1 = $("#answer1").val();
    var answertext = $("#def1").val();
    var answertext2 = $("#answer2").val();
    var useranswer2 = $("#def2").val();

    var answertext3 = $("#answer3").val();
    var useranswer3 = $("#def3").val();


    //$("#status").html(useranswer);

    if (answertext === useranswer1) {
      correct++;
      showOnScreen(); 
    }else {
      incorrect++;
    }

    if (answertext2 === useranswer2){
      correct++;
      showOnScreen();
    }else {
      incorrect++;
    }
    if (answertext3 === useranswer3){
      correct++;
      showOnScreen();
    } else {
      incorrect ++;
    };

  });


});


let correct = 0 
let incorrect = 0 

const showOnScreen = () => {
  document.getElementById("correct").innerHTML = correct; 
  document.getElementById("incorrect").innerHTML = incorrect; 
  correct = Math.min(Math.max(correct,0),4);
  incorrect = Math.min(Math.max(incorrect,0),4);

}





window.onload = showOnScreen