from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isInDiet = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # datetime objects are not JSON serializable by default; convert to ISO string
            "datetime": self.datetime.isoformat() if self.datetime is not None else None,
            "isInDiet": self.isInDiet,
            "user_id": self.user_id
        }
