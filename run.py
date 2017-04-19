from app import app, db, manager, sess
import os
app.secret_key = 'super secret key'
sess.init_app(app)


if __name__ == "__main__":
    db.create_all()
    app.debug = True;
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    # manager.run()
     