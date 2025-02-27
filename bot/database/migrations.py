from database.engine import Base, engine
migrate = lambda: Base.metadata.create_all(engine)
