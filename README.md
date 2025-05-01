# Quiz Game API with FastAPI and PostgreSQL
Un backend simple et efficace pour applications de quiz, construit avec :
 FastAPI pour des API performantes
 PostgreSQL pour un stockage fiable des données
 SQLAlchemy pour gérer la base de données
**Fonctionnalités clés :**
 Créer et gérer des questions
 Enregistrer des réponses à choix multiples
 Documentation API automatique
 
# Features
- RESTful API endpoints for quiz questions
- PostgreSQL database integration
- SQLAlchemy ORM for database operations
- Pydantic data validation
- Interactive API documentation (Swagger UI)

# Prerequisites
- Python 3.7+
- PostgreSQL installed and running
- pip package manager

# Installation

1. **Clone the repository**
   git clone https://github.com/yourusername/quiz-app.git
   cd quiz-app

2. **Set up virtual environment**
py -m venv myenv
.\myenv\Scripts\activate

3. **Install dependencies**
pip install fastapi sqlalchemy psycopg2-binary uvicorn

4. **Database setup**

# Encodage sécurisé des paramètres
username = quote_plus("postgres")
password = quote_plus("rym")
host = quote_plus("localhost")
dbname = quote_plus("quizapp")
Create a PostgreSQL database named quizApp
Update connection string in database.py:
URL_DATABASE = f"postgresql://{username}:{password}@{host}:5433/{dbname}"

5. **Running the Application**
uvicorn main:app --reload