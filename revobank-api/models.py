from app import db

class TestTable(db.Model):
    __tablename__ = "test_table"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<TestTable id={self.id} name={self.name}>"