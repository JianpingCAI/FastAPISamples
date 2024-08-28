from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.category import Category

class CategoryRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, category: Category) -> None:
        if category.id is None:
            self.db_session.add(category)
        self.db_session.commit()

    def find_by_id(self, category_id: int) -> Optional[Category]:
        return self.db_session.query(Category).filter_by(id=category_id).first()

    def find_all(self) -> List[Category]:
        return self.db_session.query(Category).all()

    def delete(self, category: Category) -> None:
        self.db_session.delete(category)
        self.db_session.commit()
