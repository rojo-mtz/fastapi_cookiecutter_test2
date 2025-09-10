# from sqlalchemy import Column, Integer, String

# from core.db import Base


# class ExampleModel(Base):
#     __tablename__ = "exampletablename"
#     __table_args__ = {
#         "extend_existing": True,
#     }

#     id = Column(Integer, primary_key=True, index=True)
#     code = Column(String, index=True)
#     name = Column(String, index=True)

#     def __init__(self, id, code, name) -> None:
#         self.id = id
#         self.code = code
#         self.name = name
