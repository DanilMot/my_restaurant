from flask import Blueprint, session, current_app, request, render_template, redirect, url_for
from sql_provider import SQLProvider
from work_with_db import select_dict, save_order_with_list
import os
from access import login_required, group_required

blueprint_basket = Blueprint('bp_basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_basket.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def choise_table():
    if request.method == 'GET':
        sql = provider.get('all_table.sql')
        tab_id = select_dict(current_app.config['db_config'], sql)
        return render_template('choise_table.html', tab_id=tab_id)
    else:
        tab_id = request.form.get('tab_id')
        session['tab_id'] = tab_id
        return redirect(url_for('bp_basket.basket_index'))


@blueprint_basket.route('/zakaz', methods=['GET', 'POST'])
@login_required
@group_required
def basket_index():
    db_config = current_app.config['db_config']
    if 'basket' not in session:
        session['basket'] = {}
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        id_bludo = request.form.get('id_bludo')
        id_bludo_del = request.form.get('id_bludo_del')
        if id_bludo:
            sql = provider.get('added_item.sql', id_bludo=id_bludo)
            item = select_dict(db_config, sql)
        else:
            sql = provider.get('added_item.sql', id_bludo=id_bludo_del)
            item = select_dict(db_config, sql)
        add_and_delete(item, id_bludo, id_bludo_del)

    return redirect(url_for('bp_basket.basket_index'))


def add_and_delete(item, id_bludo, id_bludo_del):
    if 'basket' not in session:
        session['basket'] = {}
    elif item is not None:
        if id_bludo and id_bludo in session['basket']:
            session['basket'][id_bludo]['blud_amount'] += 1
        elif id_bludo:
            session['basket'][id_bludo] = {}
            session['basket'][id_bludo]['blud_name'] = item[0]['blud_name']
            session['basket'][id_bludo]['price'] = item[0]['price']
            session['basket'][id_bludo]['blud_amount'] = 1

    if id_bludo_del is not None:
        if session['basket'][id_bludo_del]['blud_amount'] > 1:
            session['basket'][id_bludo_del]['blud_amount'] -= 1
        else:
            del (session['basket'])[id_bludo_del]
    session.permanent = False


@blueprint_basket.route('/save_order', methods=['GET', 'POST'])
@login_required
@group_required
def save_order():
    current_basket = session.get('basket', {})
    session.pop('basket')
    print(current_basket)
    if current_basket:
        order_id, total_sum = save_order_with_list(current_app.config['db_config'], session.get('user_id'), current_basket,
                                        provider, session.get('tab_id'))
        return render_template('order_created.html', order_id=order_id, total_sum=total_sum)
    else:
        return render_template('empty_order.html')
