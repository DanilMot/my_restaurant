from connection import DBContextManager
from typing import Tuple, List
import datetime


def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor is not created')
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            if result:
                schema = [item[0] for item in cursor.description]
                res_dict = []
                for product in result:
                    res_dict.append(dict(zip(schema, product)))
                return res_dict
            return None


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с ук  азанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def insert(dbconfig: dict, _sql: str):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        result = cursor.execute(_sql)
    return result


def call_proc(db_config: dict, proc_name: str, *args):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        res = cursor.callproc(proc_name, param_list)
    return res


def save_order_with_list(dbconfig: dict, user_id: int, current_basket: dict, provider: object, tab_id: int):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        total_sum = 0
        for key in current_basket.keys():
            total_sum += current_basket[key]['blud_amount'] * int(current_basket[key]['price'])
        _sql1 = provider.get('insert_order.sql', user_id=user_id, order_date=datetime.datetime.now(), tab_id=tab_id,
                             ord_sum=total_sum)
        print(_sql1)
        result1 = cursor.execute(_sql1)
        print(result1)
        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]
            print('order_id=', order_id)
            if order_id:
                for key in current_basket:
                    prod_amount = current_basket[key]['blud_amount']
                    _sql3 = provider.get('insert_order_list.sql', order_id=order_id, id_bludo=key,
                                         blud_amount=prod_amount,
                                         am_price=float(current_basket[key]['price']) * current_basket[key][
                                             'blud_amount'])
                    cursor.execute(_sql3)
                return order_id,total_sum
