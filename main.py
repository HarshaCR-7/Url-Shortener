from url_shortener import create_app
from url_shortener.models import db

app = create_app()

if __name__ == '__main__':
  app.run(debug=False)


