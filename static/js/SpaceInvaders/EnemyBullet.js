class EnemyBullet extends Phaser.GameObjects.Sprite{
    constructor(scene, enemy) {
        var x = enemy.x + 15;
        var y = enemy.y + 50;

        super(scene, x, y, "enemyBullet");
        scene.add.existing(this);

        scene.physics.world.enableBody(this);
        this.body.velocity.y = 250;
    }

    
    update(){
        if (this.y > 600) {
            this.destroy();
        }
    }
}