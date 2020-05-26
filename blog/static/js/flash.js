


function flipOne() {
	let def1 = document.getElementById("def1").hidden = false;
	let word1 = document.getElementById("word1").hidden = true; 
	var card1 = document.getElementsByClassName("card1");
  
  if (card1.innerHTML === word1) {
  	card1.innerHTML = def1;
  }

}
function flipTwo() {
	let def2 = document.getElementById("def2").hidden = false;
	let word2 = document.getElementById("word2").hidden = true;
	var card2 = document.getElementsByClassName("card2");
if (card2.innerHTML === def2){
		card2.innerHTML = word2;
	}
}	


function flipThree() {
	let def3 = document.getElementById("def3").hidden = false;
	let word3 = document.getElementById("word3").hidden = true;
	var card3 = document.getElementsByClassName("card3");
	if (card3.innerHTML === def3){
		card3.innerHTML = word3;
	}
}	


function flipFour() {
	let def4= document.getElementById("def4").hidden = false;
	let word4 = document.getElementById("word2").hidden = true;
	var card4 = document.getElementsByClassName("card4");
if (card4.innerHTML === def4){
		card4.innerHTML = word4;
	}
}	

function flipFive() {
	let def5 = document.getElementById("def5").hidden = false;
	let word5 = document.getElementById("word5").hidden = true;
	var card5 = document.getElementsByClassName("card5");
	if (card5.innerHTML === def5){
		card5.innerHTML = word5;
	}
}

