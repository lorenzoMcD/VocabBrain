var config = {
    type: Phaser.AUTO,
    width: 550 * 2,
    height: 580,
    backgroundColor: 0x000000,
    scene: [Scene1, Scene2],
	
	physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
	
};

var gameSettings = {
	playerSpeed: 200
}

var game = new Phaser.Game(config);
