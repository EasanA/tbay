from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey, desc

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    bids = relationship("Bid", backref = "item")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    auctions = relationship("Item", backref="user")
    bids = relationship("Bid", backref = "user")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key = True)
    floating_price = Column(Float, nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False) 
    item_id = Column(Integer, ForeignKey('items.id'), nullable = False)

    
Base.metadata.create_all(engine)

def main():
    jim = User(username="jimsmith", password="random123")
    john = User(username="johndoe", password="123hi")
    jane = User(username="janedoe", password="789panther")
    baseball = Item(name="baseball")
    jim.auctions.append(baseball)
    bid1 = Bid()
    bid1.floating_price = 1.00 
    bid1.item = baseball
    bid1.user = jane
    bid2 = Bid()
    bid2.floating_price = 1.25 
    bid2.item = baseball 
    bid2.user = john
    session.add_all([jim, john, jane, baseball, bid1, bid2])
    session.commit()
    bidders = session.query(Bid).order_by(desc(Bid.floating_price)).all()
    print(bidders[0].user.username)

if __name__ == "__main__":
    main()