from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = 'countries'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    population: Mapped[int] = mapped_column()  
    capital: Mapped[str] = mapped_column(String)
    timezone: Mapped[str] = mapped_column(String)
    government: Mapped[str] = mapped_column(String)
    area: Mapped[float] = mapped_column()      
    spoken_language: Mapped[str] = mapped_column(String)
    density: Mapped[float] = mapped_column()   
    
    neighbors: Mapped[List["Neighbor"]] = relationship(back_populates="country")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "capital": self.capital,
            "timezone": self.timezone,
            "government": self.government,
            "area": self.area,
            "spoken_language": self.spoken_language,
            "density": self.density
        }

    def __repr__(self):
        return f"->Country(name={self.name}, population={self.population}, density={self.density})"

class Neighbor(Base):
    __tablename__ = 'neighbors'
    
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'), primary_key=True)
    neighbor: Mapped[str] = mapped_column(String, primary_key=True)
    
    country: Mapped["Country"] = relationship(back_populates="neighbors")