import os
from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand
from app import create_app,db
from app.models import Users,Blogs,Comments

app = create_app('production')




manager=Manager(app)
manager.add_command('server',Server)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def shell_context():
    return dict(app=app,db=db,User=User)


if __name__=='__main__':
    manager.run()
