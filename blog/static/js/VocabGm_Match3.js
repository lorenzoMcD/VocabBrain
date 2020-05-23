// vocab matching game 3 words for terms and sentences/definitons

$(document).ready(function() {

  // EVENT HANDLER

  $("#clickme").click(function() {
    var useranswer1 = $("#answer1").val();
    var answertext = $("#sent1").val();

    var answertext2 = $("#answer2").val();
    var useranswer2 = $("#sent2").val();

    var answertext3 = $("#answer3").val();
    var useranswer3 = $("#sent3").val();


    //$("#status").html(useranswer);

    if (answertext === useranswer1) {
      correct++;
      showOnScreen();
    }


    if (answertext2 === useranswer2){
      correct++;
      showOnScreen();
    }

    if (answertext3 === useranswer3){
      correct++;
      showOnScreen();
    }

  });


});

// Defining correct answers and our button
let correct = 0
let clickme = document.getElementById("clickme");

//constant function that show and updates score
// Capping the score at 3
const showOnScreen = () => {
  document.getElementById("correct").innerHTML = correct;
  correct = Math.min(Math.max(correct,0),2);

}

// Click submit - Submit button disabled, reset button enabled
const finish = () =>{
  let clickme = document.getElementById("clickme");
  let reset = document.getElementById("reset");
  clickme.disabled = true;
  reset.hidden = false;
}




//load our function


window.onload = showOnScreen
