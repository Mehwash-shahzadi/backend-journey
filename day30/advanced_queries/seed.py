from app.database import SessionLocal
from app import models

db = SessionLocal()

# Tags
tag_python = models.Tag(name="python")
tag_fastapi = models.Tag(name="fastapi")
db.add_all([tag_python, tag_fastapi])
db.commit()

# Posts
post1 = models.Post(title="Learn Python", content="Python basics", author="Mehwash", tags=[tag_python])
post2 = models.Post(title="FastAPI Tutorial", content="Build APIs", author="Inshal", tags=[tag_fastapi])
post3 = models.Post(title="Advanced Python", content="ORM queries", author="Anzish", tags=[tag_python, tag_fastapi])

db.add_all([post1, post2, post3])
db.commit()
db.close()
print("Seed data added!")
