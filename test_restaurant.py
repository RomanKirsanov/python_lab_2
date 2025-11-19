import pytest
from restaurant import Dish, Menu, Order, Table

class TestDish:
    def test_dish_creation(self):
        dish = Dish("Тестовое блюдо", 100, 10, {"ингредиент": 10})
        assert dish.name == "Тестовое блюдо"
        assert dish.price == 100
        assert dish.cooking_time == 10
    
    def test_dish_cost_calculation(self):
        dish = Dish("Тестовое блюдо", 100, 10, {"ингредиент": 10})
        cost = dish.calculate_cost()
        assert cost > 0
    
    def test_dish_addition(self):
        dish1 = Dish("Блюдо 1", 100, 10, {"инг1": 10})
        dish2 = Dish("Блюдо 2", 150, 15, {"инг2": 15})
        combined = dish1 + dish2
        assert combined.name == "Комплекс: Блюдо 1 + Блюдо 2"
        assert combined.price == 225  # (100 + 150) * 0.9

class TestMenu:
    def test_menu_operations(self):
        menu = Menu()
        dish = Dish("Тестовое блюдо", 100, 10, {"ингредиент": 10})
        
        menu.add_dish(dish)
        assert len(menu) == 1
        
        found_dish = menu.find_dish("Тестовое блюдо")
        assert found_dish == dish
        
        menu.remove_dish("Тестовое блюдо")
        assert len(menu) == 0

class TestOrder:
    def test_order_operations(self):
        order = Order(1)
        dish = Dish("Тестовое блюдо", 100, 10, {"ингредиент": 10})
        
        order.add_dish(dish)
        assert len(order.get_dishes()) == 1
        
        order.apply_discount(10)
        total = order.calculate_total()
        assert total == 90  # 100 - 10%
        
        waiting_time = order.calculate_waiting_time()
        assert waiting_time > 0

class TestTable:
    def test_table_operations(self):
        table = Table(1, 4)
        dish = Dish("Тестовое блюдо", 100, 10, {"ингредиент": 10})
        
        assert not table.is_occupied
        table.occupy()
        assert table.is_occupied
        
        table.add_to_order(dish)
        order = table.get_current_order()
        assert order is not None
        assert len(order.get_dishes()) == 1
        
        table.free()
        assert not table.is_occupied

if __name__ == "__main__":
    pytest.main()