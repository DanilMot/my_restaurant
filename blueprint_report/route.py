import os
from flask import Blueprint, request, render_template, current_app, redirect, url_for
from access import login_required, group_required
from work_with_db import call_proc, select_dict, select
from sql_provider import SQLProvider


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def start_report():
    report_url = current_app.config['report_url']
    report_list = current_app.config['report_list']
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        return redirect(url_for(url_rep))


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@login_required
@group_required
def create_rep1():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        date_sale = request.form.get('date_numb')
        print('date_sell = ', date_sale)
        if date_sale:
            input_month = int(date_sale.split('-')[1])
            input_year = date_sale.split('-')[0]
            _sql = provider.get('otchet_o_blude.sql', input_month=input_month, input_year=input_year)
            ticket_result = select_dict(current_app.config['db_config'], _sql)
            if ticket_result is None:
                return render_template('report_err.html', err = 'Продаж в этом месяце не было')
            else:
                _sql = provider.get('otchet_bludo.sql', input_month=input_month, input_year=input_year)
                product_result = select_dict(current_app.config['db_config'], _sql)
                if product_result is not None:
                    return render_template('report_err.html',err = 'Отчет уже существует')
                else:
                    res = call_proc(current_app.config['db_config'], 'new_otchets', int(input_year), int(input_month))
                    print('res = ', res)
                    return render_template('report_created.html')
        else:
            return render_template('report_create.html', message='Повторите ввод')


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@login_required
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        date_sell = request.form.get('date_numb')
        if date_sell:
            input_month = int(date_sell.split('-')[1])
            input_year = date_sell.split('-')[0]
            _sql = provider.get('otchet_bludo.sql', input_month=input_month, input_year=input_year)
            print(_sql)
            result, schema = select(current_app.config['db_config'], _sql)
            print(result)
            if len(result) == 0:
                return render_template('report_err.html', err='Перед просмотром отчета требуется его создать')
            else:
                return render_template('result_view1.html', schema=schema, result=result, mon=input_month, yea=input_year)
        else:
            return render_template('report_create.html', message='Повторите ввод')


@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@login_required
@group_required
def create_rep2():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        date_sale = request.form.get('date_numb')
        print('date_sale = ', date_sale)
        if date_sale:
            input_month = int(date_sale.split('-')[1])
            input_year = date_sale.split('-')[0]
            _sql = provider.get('check_workers.sql',  input_month=input_month, input_year=input_year)
            ticket_result = select_dict(current_app.config['db_config'], _sql)
            if ticket_result is None:
                return render_template('report_err.html', err='В этом месяце нет трудоустроенных официантов')
            else:
                _sql = provider.get('workers.sql', input_month=input_month, input_year=input_year)
                product_result = select_dict(current_app.config['db_config'], _sql)
                if product_result is not None:
                    return render_template('report_err.html', err = 'Отчет уже существует')
                else:
                    res = call_proc(current_app.config['db_config'], 'workers', int(input_month), int(input_year))
                    print('res = ', res)
                    return render_template('report_created.html')
        else:
            return render_template('report_create.html', message='Повторите ввод')


@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@login_required
@group_required
def view_rep2():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        date_sale = request.form.get('date_numb')
        if date_sale:
            month_report = int(date_sale.split('-')[1])
            year_report = date_sale.split('-')[0]
            _sql = provider.get('workers.sql', input_month=month_report, input_year=year_report)
            air_result, schema = select(current_app.config['db_config'], _sql)
            if len(air_result) == 0:
                 return render_template('report_err.html',err='Перед просмотром отчета требуется его создать')
            else:
                return render_template('result_view2.html', schema=schema, result=air_result, mon=month_report, yea=year_report)
        else:
            return render_template('report_create.html', message='Повторите ввод')
