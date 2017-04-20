from app import app, db, manager, sess
import os

app.config['SESSION_TYPE'] = 'filesystem'

app.config['SECRET_KEY'] = 'reds209ndsldssdsljdsldsdsljdsldksdksdsdfsfsfsfis'
sess.init_app(app)
app.secret_key()
if __name__ == "__main__":
    app.debug = True;
    app.run()
    # manager.run()
     