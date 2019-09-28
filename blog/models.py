# from . import db
# from datetime import datetime

# class User(db.Model):
#     __tableName__='User'

#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String())
#     email=db.Column(db.String())
#     content=db.Column(db.String())
#     date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)


#     def __init__(self,name,email,content,date_posted):
#         self.name=name
#         self.email=email
#         self.content=content
#         self.date_posted=date_posted #datetime format use datetime.date() function
    
    
#     def __repr__(self):
#         return '<id: {}> <name: {}> <email: {}>'.format(self.id,self.name,self.email)

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'email': self.email,
#             'content': self.content,
#             'date posted': self.date_posted
#         }
