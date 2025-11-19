import sqlite3
from typing import List, Dict, Any
from .order_module import Order
from .menu_module import Dish

class Database:
    """Класс для работы с базой данных SQLite"""
    
    def __init__(self, db_name: str = "restaurant.db"):
        self._db_name = db_name
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()
            
            # Таблица заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    total_amount REAL NOT NULL,
                    discount REAL NOT NULL,
                    waiting_time INTEGER NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица блюд в заказах
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    dish_name TEXT NOT NULL,
                    dish_price REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders (id)
                )
            ''')
            
            conn.commit()
    
    def save_order(self, order: Order):
        """Сохранение заказа в базу данных"""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO orders (order_id, total_amount, discount, waiting_time)
                VALUES (?, ?, ?, ?)
            ''', (order.order_id, order.calculate_total(), 
                  getattr(order, '_discount', 0) * 100, 
                  order.calculate_waiting_time()))
            
            order_db_id = cursor.lastrowid
            
            for dish in order.get_dishes():
                cursor.execute('''
                    INSERT INTO order_dishes (order_id, dish_name, dish_price)
                    VALUES (?, ?, ?)
                ''', (order_db_id, dish.name, dish.price))
            
            conn.commit()
    
    def get_all_orders(self) -> List[Dict[str, Any]]:
        """Получение всех заказов из базы данных"""
        with sqlite3.connect(self._db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT o.order_id, o.total_amount, o.discount, o.waiting_time, o.order_date,
                       GROUP_CONCAT(od.dish_name, ', ') as dishes
                FROM orders o
                LEFT JOIN order_dishes od ON o.id = od.order_id
                GROUP BY o.id
                ORDER BY o.order_date DESC
            ''')
            
            orders = []
            for row in cursor.fetchall():
                orders.append({
                    'order_id': row[0],
                    'total_amount': row[1],
                    'discount': row[2],
                    'waiting_time': row[3],
                    'order_date': row[4],
                    'dishes': row[5]
                })
            
            return orders