from flask import Blueprint, render_template, current_app, request

from access import login_required, group_required
from work_with_db import select_dict,select
from sql_provider import SQLProvider
import os

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_query.route("/")
@login_required
@group_required
def query_menu():
    return render_template('query_menu.html')

@blueprint_query.route('/queries', methods=['GET', 'POST'])
@login_required
@group_required
def queries():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = sql_provider.get('product.sql', input_product=input_product)
            product_result, schema= select(current_app.config['db_config'], _sql)
            if not product_result:
                return render_template('product_form.html', error_message="Ничего не найдено")
            else:
                list_name = ["Позиция блюда", "Название блюда", "Цена", "Вес, г"]
                return render_template('db_result.html', schema=list_name, result=product_result, title="Информация о блюде")
        else:
            return render_template('product_form.html', error_message="Введите название еще раз")


@blueprint_query.route('/waitres', methods=['GET', 'POST'])
@login_required
@group_required
def waitres():
    if request.method == 'GET':
        return render_template('waitres_form.html')
    else:
        input_name = request.form.get('w_name')
        if input_name:
            _sql = sql_provider.get('waitres.sql', input_name=input_name)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if not product_result:
                return render_template('waitres_form.html', error_message="Ничего не найдено")
            else:
                list_name = ["ФИО", "Паспорт", "Дата рождения", "Дата устройства на работу", "Дата увольнения"]
                return render_template('db_result.html', schema=list_name, result=product_result, title="Данные об официанте")
        else:
            return render_template('waitres_form.html', error_message="Введите ФИО еще раз")

@blueprint_query.route('/kolvo', methods=['GET', 'POST'])
@login_required
@group_required
def kolvo():
    if request.method == 'GET':
        return render_template('kolvo_form.html')
    else:
        date_sale = request.form.get('date_numb')
        if date_sale:
            month_report = date_sale.split('-')[1]
            year_report = date_sale.split('-')[0]
            _sql = sql_provider.get('kolvo.sql', input_month=month_report, input_year=year_report)
            product_result, schema= select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                 return render_template('kolvo_form.html', message='В заданный период заказов не найдено')
            else:
                list_name = ["Уникальный номер", "ФИО", "Количество заказов"]
                return render_template('db_result.html', schema=list_name, result=product_result, title="Количество заказов у официантов")
        else:
            return render_template('kolvo_form.html', message='Повторите ввод')

@blueprint_query.route('/null', methods=['GET', 'POST'])
@login_required
@group_required
def null():
    if request.method == 'GET':
        return render_template('null_form.html')
    else:
        date_sale = request.form.get('date_numb')
        if date_sale:
            month_report = date_sale.split('-')[1]
            year_report = date_sale.split('-')[0]
            _sql = sql_provider.get('null.sql', input_month=month_report, input_year=year_report)
            product_result, schema= select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                 return render_template('null_form.html', message='В выбранный месяц все официанты принимали заказы')
            else:
                list_name = ["Уникальный номер", "ФИО", "Пасспорт", "Дата рождения"]
                return render_template('db_result.html', schema=list_name, result=product_result, title="Официанты не принявшие заказы за указанный месяц")
        else:
            return render_template('null_form.html', message='Повторите ввод')