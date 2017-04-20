from app import app, db, manager, sess
import os

if __name__ == "__main__":
    app.debug = True;
    app.run()
    # manager.run()
     