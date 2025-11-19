from typing import List, Optional
from .order_module import Order

class Table:
    """Класс для представления столика в ресторане"""
    
    def __init__(self, table_id: int, seats: int):
        self._table_id = table_id
        self._seats = seats
        self._is_occupied = False
        self._current_order: Optional[Order] = None
    
    @property
    def table_id(self) -> int:
        return self._table_id
    
    @property
    def seats(self) -> int:
        return self._seats
    
    @property
    def is_occupied(self) -> bool:
        return self._is_occupied
    
    def occupy(self):
        """Занять столик"""
        if not self._is_occupied:
            self._is_occupied = True
            self._current_order = Order(self.table_id)
    
    def free(self):
        """Освободить столик"""
        self._is_occupied = False
        self._current_order = None
    
    def add_to_order(self, dish):
        """Добавить блюдо в заказ столика"""
        if self._is_occupied and self._current_order:
            self._current_order.add_dish(dish)
    
    def get_current_order(self) -> Optional[Order]:
        return self._current_order
    
    def __str__(self) -> str:
        status = "Занят" if self._is_occupied else "Свободен"
        return f"Столик #{self.table_id} ({self.seats} мест) - {status}"
    
    def __repr__(self) -> str:
        return f"Table({self.table_id}, {self.seats})"