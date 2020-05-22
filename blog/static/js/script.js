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


    //$("#status").html(useranswer);

    if (answertext == useranswer1) {
      alert("correct");
    }


    else if (answertext2 == useranswer2){
      alert("correct on 2");
    }

    else {
      alert("incorrect");

    };

  });


});
