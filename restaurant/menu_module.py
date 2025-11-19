from abc import ABC, abstractmethod
from typing import List, Dict

class MenuItem(ABC):
    """Абстрактный базовый класс для элементов меню"""
    
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def price(self) -> float:
        return self._price
    
    @abstractmethod
    def calculate_cost(self) -> float:
        pass
    
    def __str__(self) -> str:
        return f"{self.name} - {self.price} руб."
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}', {self.price})"

class Dish(MenuItem):
    """Класс для представления блюда"""
    
    def __init__(self, name: str, price: float, cooking_time: int, ingredients: Dict[str, float]):
        super().__init__(name, price)
        self._cooking_time = cooking_time
        self._ingredients = ingredients
    
    @property
    def cooking_time(self) -> int:
        return self._cooking_time
    
    def calculate_cost(self) -> float:
        """Расчет стоимости блюда на основе ингредиентов"""
        ingredient_cost = sum(self._ingredients.values()) * 2.5  # Коэффициент наценки
        return max(ingredient_cost, self.price * 0.3)
    
    def get_ingredients(self) -> Dict[str, float]:
        return self._ingredients.copy()
    
    def __add__(self, other):
        """Объединение блюд в комплексный обед"""
        if isinstance(other, Dish):
            new_name = f"Комплекс: {self.name} + {other.name}"
            new_price = (self.price + other.price) * 0.9  # Скидка 10%
            new_time = max(self.cooking_time, other.cooking_time) + 5
            new_ingredients = {**self._ingredients, **other._ingredients}
            return Dish(new_name, new_price, new_time, new_ingredients)
        return NotImplemented

class Menu:
    """Класс для управления меню ресторана"""
    
    def __init__(self):
        self._dishes: List[Dish] = []
    
    def add_dish(self, dish: Dish):
        self._dishes.append(dish)
    
    def remove_dish(self, dish_name: str):
        self._dishes = [d for d in self._dishes if d.name != dish_name]
    
    def find_dish(self, name: str) -> Dish:
        for dish in self._dishes:
            if dish.name.lower() == name.lower():
                return dish
        raise ValueError(f"Блюдо '{name}' не найдено")
    
    def get_all_dishes(self) -> List[Dish]:
        return self._dishes.copy()
    
    def __len__(self) -> int:
        return len(self._dishes)
    
    def __getitem__(self, index: int) -> Dish:
        return self._dishes[index]