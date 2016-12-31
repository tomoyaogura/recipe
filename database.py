from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

import inquirer

engine = create_engine('postgresql://postgres:postgres@localhost:5432/recipe', convert_unicode=True)
Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__=="__main__":
    from models import init_models
    questions = [inquirer.Confirm('continue', message="This will DROP ALL TABLES. Do you want to continue?")]
    answers = inquirer.prompt(questions)
    if answers['continue']:
        init_models()
    session.close()
