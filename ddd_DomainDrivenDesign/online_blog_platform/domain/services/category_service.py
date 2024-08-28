from typing import Optional, List
from sqlalchemy.orm import Session
from domain.models.category import Category
from domain.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db_session: Session):
        self.category_repository = CategoryRepository(db_session)

    def create_category(self, name: str) -> Category:
        category = Category(name=name)
        self.category_repository.save(category)
        return category

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_repository.find_by_id(category_id)

    def get_all_categories(self) -> List[Category]:
        return self.category_repository.find_all()

    def update_category(self, category: Category, name: str) -> Category:
        category.name = name
        self.category_repository.save(category)
        return category

    def delete_category(self, category: Category) -> None:
        self.category_repository.delete(category)
