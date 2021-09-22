class PlayerBullet extends Phaser.GameObjects.Sprite{
    constructor(scene) {
        var x = scene.player.x;
        var y = scene.player.y - 15;

        super(scene, x, y, "playerBullet");
        scene.add.existing(this);

        scene.physics.world.enableBody(this);
        this.body.velocity.y = -250;
    }

    
    update(){
        if (this.y < 10) {
            this.destroy();
        }
    }
}