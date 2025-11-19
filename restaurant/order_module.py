from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime, timedelta
from .menu_module import Dish

class AbstractOrder(ABC):
    """Абстрактный базовый класс для заказов"""
    
    @abstractmethod
    def calculate_total(self) -> float:
        pass
    
    @abstractmethod
    def calculate_waiting_time(self) -> int:
        pass

class Order(AbstractOrder):
    """Класс для представления заказа"""
    
    def __init__(self, order_id: int):
        self._order_id = order_id
        self._dishes: List[Dish] = []
        self._order_time = datetime.now()
        self._discount = 0.0
    
    @property
    def order_id(self) -> int:
        return self._order_id
    
    @property
    def order_time(self) -> datetime:
        return self._order_time
    
    @property
    def discount(self) -> float:
        return self._discount * 100  # Возвращаем в процентах
    
    def add_dish(self, dish: Dish):
        self._dishes.append(dish)
    
    def remove_dish(self, dish_name: str):
        self._dishes = [d for d in self._dishes if d.name != dish_name]
    
    def apply_discount(self, percent: float):
        """Применение скидки в процентах"""
        if 0 <= percent <= 100:
            self._discount = percent / 100
    
    def calculate_original_total(self) -> float:
        """Расчет исходной суммы без скидки"""
        return sum(dish.price for dish in self._dishes)
    
    def calculate_total(self) -> float:
        """Расчет общей суммы заказа с учетом скидки"""
        original_total = self.calculate_original_total()
        return original_total * (1 - self._discount)
    
    def get_discount_amount(self) -> float:
        """Расчет суммы скидки"""
        return self.calculate_original_total() * self._discount
    
    def calculate_waiting_time(self) -> int:
        """Расчет времени ожидания заказа"""
        if not self._dishes:
            return 0
        
        max_cooking_time = max(dish.cooking_time for dish in self._dishes)
        base_time = max_cooking_time + 10  # Базовое время + 10 минут на обслуживание
        
        # Учет количества блюд
        if len(self._dishes) > 3:
            base_time += (len(self._dishes) - 3) * 5
        
        return base_time
    
    def get_dishes(self) -> List[Dish]:
        return self._dishes.copy()
    
    def __str__(self) -> str:
        original_total = self.calculate_original_total()
        final_total = self.calculate_total()
        
        if self._discount > 0:
            return (f"Заказ #{self.order_id} - {len(self._dishes)} блюд\n"
                    f"Общая сумма: {original_total:.2f} руб.\n"
                    f"Скидка: {self.discount:.1f}% (-{self.get_discount_amount():.2f} руб.)\n"
                    f"Итого к оплате: {final_total:.2f} руб.")
        else:
            return f"Заказ #{self.order_id} - {len(self._dishes)} блюд - {final_total:.2f} руб."
    
    def __repr__(self) -> str:
        return f"Order({self.order_id})"