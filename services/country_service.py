from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data.models import Country, Neighbor
from sqlalchemy import or_, func

class CountryService:
    def __init__(self, db_url: str = 'sqlite:///countries.db'):
        self.engine = create_engine(db_url)
    
    def _get_session(self) -> Session:
        return Session(self.engine)
    
    def get_all_countries(self) -> List[Country]:
        with self._get_session() as session:
            countries = session.query(Country).all()
            return [c.to_dict() for c in countries]

    def get_top_by_population(self, limit: int = 10) -> List[Country]:
        with self._get_session() as session:
            countries =  session.query(Country)\
                .order_by(Country.population.desc())\
                .limit(limit)\
                .all()
            return [c.to_dict() for c in countries]
    
    def get_top_by_density(self, limit: int = 10) -> List[Country]:
        with self._get_session() as session:
            countries = session.query(Country)\
                .order_by(Country.density.desc())\
                .limit(limit)\
                .all()
            return [c.to_dict() for c in countries]
    
    def get_by_timezone(self, timezone: str) -> List[Country]:
        with self._get_session() as session:
            timezone_condition = or_(
                Country.timezone.like(f"%UTC{timezone}%"), 
                Country.timezone.like(f"%{timezone}%")
            )
            
            countries = session.query(Country).filter(timezone_condition).all()
            
            return [c.to_dict() for c in countries]
    
    def get_by_language(self, language: str) -> List[Country]:
        with self._get_session() as session:
            countries =  session.query(Country)\
                .filter(Country.spoken_language.like(f'%{language}%'))\
                .all()
            return [c.to_dict() for c in countries]

    def get_by_regime(self, regime: str) -> List[Country]:
        with self._get_session() as session:
            countries =  session.query(Country)\
                .filter(Country.government.like(f'%{regime}%'))\
                .all()
            return [c.to_dict() for c in countries]
    
    def get_by_neighbors_count(self, count: int) -> List[Country]:
        with self._get_session() as session:
            countries = session.query(Country).all()
            return [c.to_dict() for c in countries if len(c.neighbors) >= count]
