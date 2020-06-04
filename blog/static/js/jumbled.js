function jumbled(words){
	// declare variable
	var shuffled = "", len, i, randPos;
	// Check if words are strings
	words = "" + words;
	// length of string
	len = words.length;
	// Change items in words to have a random position
	for (i=0; i<len; i++){

		randPos = Math.floor(Math.random() * words.length); 
		shuffled += words[randPos];
		words = words.slice(0, randPos) + words.slice(randPos +1); 

	}
	//output 
	return shuffled; 
} 	
	let words = document.getElementById("1");
	var shuffled = jumbled(words); 

	console.log(shuffled)

