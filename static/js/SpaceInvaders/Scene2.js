class Scene2 extends Phaser.Scene {
	constructor() {
		super("playGame");
	}

	init(data) {
		console.log('init', data);
		this.pShip = data.ship;
	}

	create() {

		///// Create Images /////

		this.background = this.add.tileSprite(0, 0, config.width, config.height, "background");
		this.background.setOrigin(0, 0);

		this.player = this.physics.add.sprite(550 / 2, config.height - 75, 'ship1');
		this.chooseShip(this.pShip);

		this.player.body.setCollideWorldBounds(true); //player cannot go out of screen
		this.player.setScale(.5); //make the player smaller

		// text style for words on screen
		var textStyle = {
			font: "25px Arial",
			fill: "white"
		};

		///// Create Groups /////

		this.enemies = this.physics.add.group();
		this.enemies1 = this.physics.add.group();
		this.enemies2 = this.physics.add.group();
		this.enemies3 = this.physics.add.group();
		this.enemies4 = this.physics.add.group();

		this.projectiles = this.add.group();
		this.physics.add.overlap(this.projectiles, this.enemies, this.hitEnemy, null, this);

		this.enemyProjectiles = this.add.group();
		this.physics.add.overlap(this.player, this.enemyProjectiles, this.hurtPlayer, null, this);

		///// Create Controls /////

		this.cursors = this.input.keyboard.createCursorKeys();
		this.spacebar = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
		this.r = this.input.keyboard.addKey('R');

		///// Score /////

		this.score = 0;
		this.scoreText = this.add.text(950, 10, "Score: " + this.score, textStyle);

		///// Lives /////
		this.lives = 3;
		//this.livesText = this.add.text(410, 10, "Lives: " + this.lives, textStyle);

		///// GameOver /////

		this.gameOverText = this.add.text(120, 200, "", this.textStyle);
		this.gameOverText.text = "Game Over! \nClick to restart!";
		this.gameOverText.setVisible(false);
		this.gameOverText.setDepth(0);

		this.difficulty = 1000;

		///// Words and Definitions /////

		var words = ["A", "B", "C", "D", "E"];
		var definitions = ["A_def", "B_def", "C_def", "D_def", "E_def"];
		
		this.currentIndex = 0; //current word we are on
		
		this.wordText = this.add.text(810, 10, "Word: " + words[this.currentIndex], textStyle);
				
		// enemies defeated
		this.enem_defeated = 0;
		this.defeatedText = this.add.text(810, 40, "Enemies Defeated: " + this.enem_defeated, textStyle);
		
		// enemy / options display on right
		
		var displayedOptions = ["test", "test", "test", "test"];
		
		this.display1 = this.add.text(900, 90, displayedOptions[0], textStyle);
		this.display2 = this.add.text(900, 150, displayedOptions[1], textStyle);
		this.display3 = this.add.text(900, 210, displayedOptions[2], textStyle);
		this.display4 = this.add.text(900, 270, displayedOptions[3], textStyle);
		
		this.answerIndex = this.updateWords(displayedOptions, definitions, this.currentIndex);
		
		this.enemy1_display = this.physics.add.sprite(830, 110, "enemies1").setScale(.6);
		this.enemy2_display = this.physics.add.sprite(830, 170, "enemies2").setScale(.6);
		this.enemy3_display = this.physics.add.sprite(830, 230, "enemies3").setScale(.6);
		this.enemy4_display = this.physics.add.sprite(830, 290, "enemies4").setScale(.6);
		
		this.createEnemies();
		
		// collision when correct answer found
		
		this.physics.add.overlap(this.player, this.enemies1, function(){ this.wordClear1(words, definitions, displayedOptions); }, null, this);
		this.physics.add.overlap(this.player, this.enemies2, function(){ this.wordClear2(words, definitions, displayedOptions); }, null, this);
		this.physics.add.overlap(this.player, this.enemies3, function(){ this.wordClear3(words, definitions, displayedOptions); }, null, this);
		this.physics.add.overlap(this.player, this.enemies4, function(){ this.wordClear4(words, definitions, displayedOptions); }, null, this);
		
		this.physics.add.overlap(this.player, this.enemies, this.hurtPlayer, null, this);
	}

	update() {

		//move the background and characters
		this.background.tilePositionY -= 0.5;
		this.movePlayer();
		this.playerShoot();
		this.enemyShoot();
		this.levelClear();
		
		if(Phaser.Input.Keyboard.JustDown(this.r) && this.enem_defeated >= 10) {
			this.enemyReset();
		}

		//update projectiles so they're deleted when off screen
		for(var i = 0; i < this.projectiles.getChildren().length; i++) {
			var beam = this.projectiles.getChildren()[i];
			beam.update();
		}

		for(var i = 0; i < this.enemyProjectiles.getChildren().length; i++) {
			var beam = this.enemyProjectiles.getChildren()[i];
			beam.update();
		}
		
	}


	///// Helper Methods /////

	chooseShip(ship) {
		
		if(ship == 1) {
			this.player.setTexture('ship1')
		}
		else if(ship == 2) {
			this.player.setTexture('ship2')
		}
		else if(ship == 3) {
			this.player.setTexture('ship3')
		}
		else if(ship == 4) {
			this.player.setTexture('ship4')
		}
		else if(ship == 5) {
			this.player.setTexture('ship5')
		}
		else if(ship == 6) {
			this.player.setTexture('ship6')
		}
		else if(ship == 7) {
			this.player.setTexture('ship7')
		}
		else if(ship == 8) {
			this.player.setTexture('ship8')
		}

	}

	movePlayer(){

		//move left and right
		if(this.cursors.left.isDown){
			this.player.body.setVelocityX(-gameSettings.playerSpeed);
		}
		else if(this.cursors.right.isDown){
			this.player.body.setVelocityX(gameSettings.playerSpeed);
		}
		else {
			this.player.body.setVelocityX(0)
		}

		//move up and down
		if(this.cursors.up.isDown){
			this.player.body.setVelocityY(-gameSettings.playerSpeed);
		}
		else if(this.cursors.down.isDown){
			this.player.body.setVelocityY(gameSettings.playerSpeed);
		}
		else {
			this.player.body.setVelocityY(0)
		}
	}

	playerShoot(){

		if (Phaser.Input.Keyboard.JustDown(this.spacebar)) {
			if(this.player.active) {
				var playerBullet = new PlayerBullet(this);
				this.projectiles.add(playerBullet); //add to group
			}
		}

	}

	inArr(arr, n) {
		for(var i = 0; i < arr.length; i++) {
			if(arr[i] == n) {
				return true;
			}
		}
		
		return false;
	}
	
	getEnemyString(n) {
		if(n == 1) 
			return 'ship1';
		if(n == 2) 
			return 'ship2';
		if(n == 3) 
			return 'ship3';
		if(n == 4) 
			return 'ship4';
		if(n == 5) 
			return 'ship5';
		if(n == 6) 
			return 'ship6';
		if(n == 7) 
			return 'ship7';
		if(n == 8) 
			return 'ship8';
	}
	
	createEnemies(){

		var used = [this.pship];
		var displayed = [];
		
		for(var i = 0; i < 4; i++) { 
			do {
				var displayedEnemies = Phaser.Math.Between(1, 8);
			} while(this.inArr(used, displayedEnemies));
			
			displayed.push(displayedEnemies);
			used.push(displayedEnemies);
		}
		

		for(var y = 0; y < 3; y++) {
			for(var x = 0; x < 6; x++) {

				//var randomEnemy = Phaser.Math.Between(1, 4);
				var randomEnemy = 1;
				
				if(randomEnemy == 1){
					var enemy = this.enemies1.create((1.3*x + 2) * (550 / 7) + 30, ((1.5*y + 2) * 50) - 35, this.getEnemyString(displayed[0]));
					this.enemies.add(enemy); 
					enemy.setScale(.6);
					enemy.flipY = true;
				}
				
				if(randomEnemy == 2){
					var enemy = this.enemies2.create((1.3*x + 2) * (550 / 7) + 30, ((1.5*y + 2) * 50) - 35, this.getEnemyString(displayed[1]));
					this.enemies.add(enemy); 
					enemy.setScale(.6);
					enemy.flipY = true;
				}
				
				if(randomEnemy == 3){
					var enemy = this.enemies3.create((1.3*x + 2) * (550 / 7) + 30, ((1.5*y + 2) * 50) - 35, this.getEnemyString(displayed[2]));
					this.enemies.add(enemy); 
					enemy.setScale(.6);
					enemy.flipY = true;
				}
				
				if(randomEnemy == 4){
					var enemy = this.enemies4.create((1.3*x + 2) * (550 / 7) + 30, ((1.5*y + 2) * 50) - 35, this.getEnemyString(displayed[3]));
					this.enemies.add(enemy); 
					enemy.setScale(.6);
					enemy.flipY = true;
				}

				enemy.body.velocity.x = -90
			}
		}

		// update enemy display on the right menu
		this.enemy1_display.setTexture(this.getEnemyString(displayed[0])).setScale(.6)
		this.enemy2_display.setTexture(this.getEnemyString(displayed[1])).setScale(.6)
		this.enemy3_display.setTexture(this.getEnemyString(displayed[2])).setScale(.6)
		this.enemy4_display.setTexture(this.getEnemyString(displayed[3])).setScale(.6)
		
		// timer to make enemies change direction
		this.enemyTimer = this.time.addEvent({
			delay: 1500,
			callback: this.changeEnemyDirection,
			callbackScope: this,
			loop: true
		});
	}

	changeEnemyDirection() {

		for(var i = 0; i < this.enemies.getChildren().length; i++) {
			var enemy = this.enemies.getChildren()[i];
			enemy.body.velocity.x *= -1;
		}
	}

	enemyShoot() {

		for(var i = 0; i < this.enemies.getChildren().length; i++) {
			var randomEnemyShoot = Phaser.Math.Between(1, this.difficulty);
			if (randomEnemyShoot == 1) { //10% chance to shoot
				var enemyBullet = new EnemyBullet(this, this.enemies.getChildren()[i]);
				this.enemyProjectiles.add(enemyBullet); //add to group
			}
		}

	}

	hitEnemy(projectile, enemy) {

		var explosion = new Explosion(this, enemy.x, enemy.y);

		projectile.destroy();
		enemy.destroy();

		this.score += 15;
		this.scoreText.text = "Score: " + this.score;
		
		this.enem_defeated++;
		this.defeatedText.text = "Enemies Defeated: " + this.enem_defeated;
	}

	hurtPlayer(player, enemy) {
		//this.lives -= 1;
		//this.livesText.text = "Lives: " + this.lives;

		var explosion = new Explosion(this, player.x, player.y);

		enemy.destroy();
		player.disableBody(true, true);

		if (this.lives >= 1) {
			this.time.addEvent({
				delay: 1000,
				callback: this.resetPlayer,
				callbackScope: this,
				loop: false
			})
		}
		else if (this.lives < 1) {
			this.gameOverText.setVisible(true);
			this.gameOverText.setDepth(1);
			this.input.once("pointerdown", this.restart, this);
		}
	}

	resetPlayer() {

		var x = 550 / 2 - 8;
		var y = config.height + 64;
		this.player.enableBody(true, x, y, true, true);

		this.player.alpha = 0.5;

		var tween = this.tweens.add({
			targets: this.player,
			y: config.height - 64,
			ease: 'Power1',
			duration: 1500,
			repeat: 0,
			onComplete: function(){
				this.player.alpha = 1;
			},
			callbackScope: this
		});

	}

	restart() {

		this.lives = 3;
		this.livesText.text = "Lives: " + this.lives;

		this.score = 0;
		this.scoreText.text = "Score: " + this.score;

		this.difficulty = 1000;

		this.enemyProjectiles.clear(true, true);

		this.enemies.clear(true, true);
		this.enemyTimer.remove();
		this.createEnemies();
		this.resetPlayer();
		this.gameOverText.setVisible(false);
	}

	
	levelClear() {

		if(this.enemies.getChildren().length == 0) {

			this.enemyTimer.remove();
			this.createEnemies();

			/*
			if(this.difficulty > 200) {
				this.difficulty -= 100
			}

			else if(this.difficulty <= 200) {
				this.difficulty -= 10
			}
			*/
		}
	}
	

	wordClear1(words, definitions, displayedOptions) {
		
		if(this.answerIndex == 0 && this.enemies1.getChildren().length == 1) {
			
			this.index = Phaser.Math.Between(0, words.length - 1);
			
			this.resetPlayer();
			this.wordCorrect(displayedOptions, definitions, this.index);
			this.wordText.text = "Word: " + words[this.index];
		}
	
	}
	
	wordClear2(words, definitions, displayedOptions) {
		
		if(this.answerIndex == 1 && this.enemies2.getChildren().length == 1) {
			
			this.index = Phaser.Math.Between(0, words.length - 1);
			
			this.resetPlayer();
			this.wordCorrect(displayedOptions, definitions, this.index);
			this.wordText.text = "Word: " + words[this.index];
		}
		
	}
	
	wordClear3(words, definitions, displayedOptions) {
		
		if(this.answerIndex == 2 && this.enemies3.getChildren().length == 1) {
			
			this.index = Phaser.Math.Between(0, words.length - 1);
			
			this.resetPlayer();
			this.wordCorrect(displayedOptions, definitions, this.index);
			this.wordText.text = "Word: " + words[this.index];
		}
		
	}
	
	wordClear4(words, definitions, displayedOptions) {
		
		if(this.answerIndex == 3 && this.enemies4.getChildren().length == 1) {
			
			this.index = Phaser.Math.Between(0, words.length - 1);
			
			this.resetPlayer();
			this.wordCorrect(displayedOptions, definitions, this.index);
			this.wordText.text = "Word: " + words[this.index];
		}
		
	}
	
	enemyReset() {
			
			this.projectiles.clear(true, true);
			this.enemyProjectiles.clear(true, true);
			this.enemies.clear(true, true);
			this.enemies1.clear(true, true);
			this.enemies2.clear(true, true);
			this.enemies3.clear(true, true);
			this.enemies4.clear(true, true);
			this.enemyTimer.remove();
			this.createEnemies();
			
			this.enem_defeated = 0;
			this.defeatedText.text = "Enemies Defeated: " + this.enem_defeated;
	}
	
	wordCorrect(displayedOptions, definitions, index) {
		
		this.answerIndex = this.updateWords(displayedOptions, definitions, index);
		this.enemyReset()
	}
	
	
	//updates the words displayed on the screen for the user to choose from
	updateWords(displayedOptions, definitions, index) {
		
		for(var i = 0; i < 4; i++) {
			
			displayedOptions[i] = "test";
		}
		
		var answerIndex = Phaser.Math.Between(0, 3);
		displayedOptions[answerIndex] = definitions[index];
		var usedIndexes = [index];
		
		for(var i = 0; i < 4; i++) {
			if(i != answerIndex) {
				var wrongIndex;
				do {
					
					wrongIndex = Phaser.Math.Between(0, definitions.length - 1);
				}
				while(usedIndexes.includes(wrongIndex));
				
				displayedOptions[i] = definitions[wrongIndex];
				usedIndexes.push(wrongIndex);
			}
		}
		
		
		this.display1.text = displayedOptions[0];
		this.display2.text = displayedOptions[1];
		this.display3.text = displayedOptions[2];
		this.display4.text = displayedOptions[3];
		
		return answerIndex;
	}
}
