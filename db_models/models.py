from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class KioskLocations(Base):
  __tablename__ = 'kiosk_locations'

  id = Column(Integer, primary_key=True)
  name = Column(String(1000))
  latitude = Column(Float)
  longitude = Column(Float)
  address = Column(String(1000))

  def __repr__(self):
      return "<Kiosk Location(name='%s')>" % (self.name)


class TravelDiatances(Base):
  __tablename__ = 'travel_distances'

  id = Column(Integer, primary_key=True)
  distance = Column(Float)
  from_kiosk_location_id = Column(Integer, ForeignKey('kiosk_locations.id'))
  to_kiosk_location_id = Column(Integer, ForeignKey('kiosk_locations.id'))

  def __repr__(self):
    return "Distance from {} to {} is: {} miles".format(
      from_kiosk_location_id,
      to_kiosk_location_id,
      distance
    )