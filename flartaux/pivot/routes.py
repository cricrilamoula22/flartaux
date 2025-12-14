from flask import Flask, Blueprint, render_template, Request
from jinja2 import FileSystemLoader
from flask import Flask, request, redirect, url_for, session, flash, jsonify, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sqlalchemy.sql import text
from sqlalchemy import desc, asc, and_, select, text, or_, func

from wtforms import SelectField
from flask_wtf import FlaskForm

from flask import Blueprint, render_template
#dossier = Blueprint('dossier_blueprint', __name__)
pivot = Blueprint('pivot', __name__, url_prefix='/pivot', static_folder='static', template_folder='pivot/templates')
from . import pivot
# Personnaliser le moteur de rendu de templates
#groupsel.jinja_loader = FileSystemLoader('/groupsel/templates/groupsel')

# Create the Blueprint instance
#dossier_blueprint = Blueprint('dossier_blueprint', __name__)

#init_zut(app)
"""
import os
print(os.getcwd())
print(app.jinja_loader.searchpath)
"""
from ..database import db
from ..extensions import cache
#from .queries import fetch_dossiers_by_no_interne, fetch_dossiers_by_id, get_parcelle_by_idsuf, get_all_t_demande, get_all_parcelles, get_all_parceldem, get_all_t_com2023, fetch_sections_by_commune
#from .models import TParceldem, TCom2023, TCadastre
#from .forms import Form

from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from .models import db,
"""
from .models import TProprietaires, Group, LeftItem, RightItem, ItemGroup
from ..zut.models import TParceldem, TCadastre
from ..auth.models import TUser
"""
from .models import Products, Regions, Sales
import random
import string
import logging
from sqlalchemy import and_, or_, not_
import re
import pandas as pd
from sqlalchemy import select, literal

from io import BytesIO

from flask import Flask, send_file

@pivot.route('/pivot', methods=['GET'])
def pivot_query():
    region_filter = request.args.get('region')

    #query = db.session.query(Sales.region_id, Sales.product_id, Sales.price_per_unit)
    #query = db.session.query(Regions.name.label('regions_name'), Products.name.label('products_name'), Sales.price_per_unit)
    query = (db.session.query(Regions.name.label('regions_name'), Products.name.label('products_name'), Sales.price_per_unit)\
    .join(Sales, Sales.product_id == Products.id)\
    .join(Regions, Regions.id == Sales.region_id))

    
    if region_filter:
        query = query.filter(Sales.region_id == region_filter)

    #df = pd.read_sql(query.statement, db.session.bind)
    #sql = "SELECT region_id, product_id, price_per_unit FROM sales"
    df = pd.read_sql(query.statement, db.engine)

    #df = pd.read_sql(sql, db.session.bind)

    #pivot_df = df.pivot_table(index='region_id', columns='product_id', values='price_per_unit', aggfunc='sum', fill_value=0)
    pivot_df = df.pivot_table(index='regions_name', columns='products_name', values='price_per_unit', aggfunc='sum', fill_value=0)
    pivot_df = pivot_df.reset_index()

    # Convert to list of dicts and list of column headers
    data = pivot_df.to_dict(orient='records')
    columns = pivot_df.columns.tolist()

    return render_template('pivot/pivot_table.html', data=data, columns=columns)

@pivot.route('/pivot-multi')
def pivot_sales_multi():
    # SQL JOIN across tables
    query = """
        SELECT
            r.name AS region,
            p.name AS product,
            s.quantity,
            s.quantity * s.price_per_unit AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.id
        JOIN regions r ON s.region_id = r.id
    """

    df = pd.read_sql(query, db.engine)

    # Pivot on region/product with multiple value columns
    pivot_df = pd.pivot_table(
        df,
        index='region',
        columns='product',
        values=['quantity', 'revenue'],
        aggfunc='sum',
        fill_value=0
    )

    # Optional: flatten multi-index columns for easier JSON
    pivot_df.columns = [f"{metric}_{product}" for metric, product in pivot_df.columns]
    result = pivot_df.reset_index().to_dict(orient='records')

    return jsonify(result)


@pivot.route('/export-xlsx')
def export_sales_xlsx():
    query = """
        SELECT
            r.name AS region,
            p.name AS product,
            s.quantity,
            s.quantity * s.price_per_unit AS revenue
        FROM sales s
        JOIN products p ON s.product_id = p.id
        JOIN regions r ON s.region_id = r.id
    """
    df = pd.read_sql(query, db.engine)

    # Pivot data
    pivot_df = pd.pivot_table(
        df,
        index='region',
        columns='product',
        values=['quantity', 'revenue'],
        aggfunc='sum',
        fill_value=0
    )

    # Optional: flatten columns
    pivot_df.columns = [f"{metric}_{product}" for metric, product in pivot_df.columns]

    # Save to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pivot_df.to_excel(writer, sheet_name='SalesPivot')
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='sales_pivot.xlsx'
    )

# Example Flask route to return product with sales
@pivot.route("/product/<int:product_id>")
def get_product(product_id):
    product = db.session.query(Products).filter_by(id=product_id).first()
    result = {
        "id": product.id,
        "name": product.name,
        "sales": [
            {"date": sale.sales_date, "amount": sale.price_per_unit, "region": sale.region_id}
            for sale in product.sales
        ]
    }
    return jsonify(result)


@pivot.route("/export/products")
def export_products_to_excel():
    # Fetch all products with their sales
    products = db.session.query(Products).all()

    # Flatten data into rows
    data = []
    for product in products:
        for sale in product.sales:
            data.append({
                "Product ID": product.id,
                "Product Name": product.name,
                "Sale Date": sale.sales_date,
                "Amount": sale.price_per_unit,
                "Region": sale.region_id
            })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales Report')

    output.seek(0)
    return send_file(output, download_name="sales_report.xlsx", as_attachment=True)
   

@pivot.route("/export/pivoted")
def export_pivoted_sales():
    products = db.session.query(Products).all()

    rows = []
    for product in products:
        sales_data = [
            {
                "date": sale.sales_date,
                "amount": sale.price_per_unit,
                "region": sale.region_id
            }
            for sale in product.sales
        ]
        rows.append({
            "Product ID": product.id,
            "Product Name": product.name,
            "Sales": json.dumps(sales_data)  # Convert list of dicts to string
        })

    df = pd.DataFrame(rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Pivoted Sales')

    output.seek(0)
    return send_file(output, download_name="pivoted_sales.xlsx", as_attachment=True)
    
    
@pivot.route("/report")
def sales_report():
    products = db.session.query(Products).all()

    report_data = []
    for product in products:
        sales_strings = [
            f"{sale.sales_date}: ${sale.price_per_unit} ({sale.region_id})"
            for sale in product.sales
        ]
        sales_summary = "; ".join(sales_strings)

        report_data.append({
            "id": product.id,
            "name": product.name,
            "sales_summary": sales_summary
        })

    return render_template("pivot/report.html", products=report_data)    