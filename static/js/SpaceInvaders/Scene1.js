class Scene1 extends Phaser.Scene {
  constructor() {
    super("bootGame");
  }

  preload(){
	this.load.image("background", "/static/js/SpaceInvaders/assets/back.jpg");
	this.load.image("title", "/static/js/SpaceInvaders/assets/title.jpg");
	
	this.load.image('ship1', '/static/js/SpaceInvaders/assets/newShips/ship1.png');
	this.load.image('ship2', '/static/js/SpaceInvaders/assets/newShips/ship2.png');
	this.load.image('ship3', '/static/js/SpaceInvaders/assets/newShips/ship3.png');
	this.load.image('ship4', '/static/js/SpaceInvaders/assets/newShips/ship4.png');
	this.load.image('ship5', '/static/js/SpaceInvaders/assets/newShips/ship5.png');
	this.load.image('ship6', '/static/js/SpaceInvaders/assets/newShips/ship6.png');
	this.load.image('ship7', '/static/js/SpaceInvaders/assets/newShips/ship7.png');
	this.load.image('ship8', '/static/js/SpaceInvaders/assets/newShips/ship8.png');

    this.load.image('enemies1', '/static/js/SpaceInvaders/assets/newAlien.png');
	this.load.image('enemies2', '/static/js/SpaceInvaders/assets/newAlien2.png');
	this.load.image('enemies3', '/static/js/SpaceInvaders/assets/newAlien3.png');
	this.load.image('enemies4', '/static/js/SpaceInvaders/assets/newAlien4.png');

	this.load.image('playerBullet', '/static/js/SpaceInvaders/assets/blueBeam.png');
	this.load.image('enemyBullet', '/static/js/SpaceInvaders/assets/redBeam.png');

	this.load.spritesheet('explosion', '/static/js/SpaceInvaders/assets/explosion.png', {
		frameWidth: 16,
		frameHeight: 16
	});

  }

  create() {

	this.back = this.add.image(config.width/2, config.height/2, "background");
	this.titleText = this.add.image(config.width/2, 100, "title");

	///// Animations /////

	this.anims.create({
		key: "player_anim",
		frames: this.anims.generateFrameNumbers("player"),
		frameRate: 20,
		repeat: -1
	});

	this.anims.create({
        key: "playerBullet_anim",
        frames: this.anims.generateFrameNumbers("playerBullet"),
        frameRate: 20,
        repeat: -1
    });

	this.anims.create({
        key: "enemies_anim",
        frames: this.anims.generateFrameNumbers("enemies"),
        frameRate: 20,
        repeat: -1
	});

	this.anims.create({
		key: "explode",
		frames: this.anims.generateFrameNumbers("explosion"),
		frameRate: 20,
		repeat: 0,
		hideOnComplete: true
	});

	this.ship1 = this.physics.add.sprite(275, config.height - 205, "ship1").setInteractive();
	this.ship2 = this.physics.add.sprite(458, config.height - 205, "ship2").setInteractive();
	this.ship3 = this.physics.add.sprite(642, config.height - 205, "ship3").setInteractive();
	this.ship4 = this.physics.add.sprite(825, config.height - 205, "ship4").setInteractive();
	
	this.ship5 = this.physics.add.sprite(275, config.height - 75, "ship5").setInteractive();
	this.ship6 = this.physics.add.sprite(458, config.height - 75, "ship6").setInteractive();
	this.ship7 = this.physics.add.sprite(642, config.height - 75, "ship7").setInteractive();
	this.ship8 = this.physics.add.sprite(825, config.height - 75, "ship8").setInteractive();
	
	this.ship1.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 1 } );
	}, this);
	
	this.ship2.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 2 } );
	}, this);
	
	this.ship3.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 3 } );
	}, this);
	
	this.ship4.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 4 } );
	}, this);
	
	this.ship5.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 5 } );
	}, this);
	
	this.ship6.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 6 } );
	}, this);
	
	this.ship7.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 7 } );
	}, this);
	
	this.ship8.on('pointerdown', function (pointer) {
		this.scene.start("playGame", { ship: 8 } );
	}, this);
	
  }

}
