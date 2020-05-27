// vocab matching game 5 words for terms and sentences/definitions
  let wrong = "";

$(document).ready(function() {

  var csrf = $("input[name = csrfmiddlewaretoken]").val();




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


    let word = "";

    if (answertext === useranswer1) {
      correct++;
      showOnScreen();
    }else{
      word = useranswer1 + ',';
    document.getElementById("w").value += word;
    }


    if (answertext2 === useranswer2){
      correct++;
      showOnScreen();
    }else{
      word = useranswer2 + ',';
    document.getElementById("w").value += word;
    }

    if (answertext3 === useranswer3){
      correct++;
      showOnScreen();
    }else{
       word = useranswer3 + ',';
    document.getElementById("w").value += word;
    }


    if (answertext4 === useranswer4){
      correct++;
      showOnScreen();
    }else{
       word = useranswer4 + ',';
    document.getElementById("w").value += word;
    }


    if (answertext5 === useranswer5){
      correct++;
      showOnScreen();

    }else{
       word = useranswer5 + ',';
    document.getElementById("w").value += word;
    }




  });







});

// Defining correct answers and our button
let correct = 0
let clickme = document.getElementById("clickme");


//constant function that show and updates score
// Capping the score at 5
const showOnScreen = () => {
  document.getElementById("correct").innerHTML = correct;
  document.getElementById("score").value = correct;
  correct = Math.min(Math.max(correct,0),4);

}

// Click submit - Submit button disabled, reset button enabled
const finish = () =>{
  let clickme = document.getElementById("clickme");
  clickme.disabled = true;

       }

//load our function


window.onload = showOnScreen
