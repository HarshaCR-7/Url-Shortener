from url_shortener import create_app
from url_shortener.models import db
#db.create_all(app=create_app())
app = create_app()

if __name__ == '__main__':
  app.run()


