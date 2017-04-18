from app import app, db, manager, sess
import os
if __name__ == "__main__":  
    db.create_all()
    app.debug = True
    app.run()