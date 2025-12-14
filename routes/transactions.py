from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func, case
from models import db, Transaction, Category

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/transactions", methods=["GET", "POST"])
@login_required
def index():
    uid = current_user.id
    categories = db.session.query(Category).filter_by(user_id=uid).order_by(Category.name).all()

    if request.method == "POST":
        t_type = request.form["type"]
        amount = request.form["amount"]
        desc = request.form.get("description", "")
        t_date_str = request.form.get("date") or date.today().isoformat()
        cat_id = request.form.get("category_id") or None

        # ✅ Convert string → Python date
        try:
            t_date = datetime.strptime(t_date_str, "%Y-%m-%d").date()
        except ValueError:
            t_date = date.today()

        if t_type not in ("income", "expense"):
            flash("Invalid type.", "danger")
            return redirect(url_for("transactions.index"))

        tx = Transaction(
            user_id=uid,
            category_id=int(cat_id) if cat_id else None,
            amount=float(amount),
            type=t_type,
            description=desc,
            date=t_date
        )
        db.session.add(tx)
        db.session.commit()
        flash("Transaction added.", "success")
        return redirect(url_for("transactions.index"))

    q = db.session.query(Transaction).filter_by(user_id=uid).order_by(Transaction.date.desc(), Transaction.id.desc())
    transactions = q.all()
    #return render_template("transactions.html", transactions=transactions, categories=categories, today=date.today())
    uid = current_user.id

    totals = db.session.query(
        func.coalesce(func.sum(case((Transaction.type=='income', Transaction.amount), else_=0)), 0).label("income"),
        func.coalesce(func.sum(case((Transaction.type=='expense', Transaction.amount), else_=0)), 0).label("expense")
    ).filter(Transaction.user_id==uid).one()
    balance = float(totals.income or 0) - float(totals.expense or 0)

    # Category-wise expenses
    cat_rows = db.session.query(Category.name, func.coalesce(func.sum(Transaction.amount), 0)) \
        .join(Transaction, Transaction.category_id==Category.id, isouter=True) \
        .filter(Category.user_id==uid, Transaction.type=='expense') \
        .group_by(Category.name).all()
    cat_labels = [r[0] for r in cat_rows if float(r[1] or 0) > 0]
    cat_values = [float(r[1]) for r in cat_rows if float(r[1] or 0) > 0]

    # Monthly trend (SQLite vs Postgres)
    sql = """
        SELECT strftime('%Y-%m-01', date) AS month, SUM(amount) AS total
        FROM transactions
        WHERE user_id = :uid AND type = 'expense'
        GROUP BY month
        ORDER BY month
    """ if db.engine.url.get_backend_name().startswith("sqlite") else """
        SELECT date_trunc('month', date) AS month, SUM(amount) AS total
        FROM transactions
        WHERE user_id = :uid AND type = 'expense'
        GROUP BY month
        ORDER BY month
    """
    trend_rows = db.session.execute(db.text(sql), {"uid": uid}).fetchall()
    trend_labels = [str(r[0])[:10] for r in trend_rows]
    trend_values = [float(r[1]) for r in trend_rows]
    return render_template("transactions.html", transactions=transactions, categories=categories, today=date.today(),
                           income=float(totals.income or 0),
                           expense=float(totals.expense or 0),
                           balance=balance,
                           cat_labels=cat_labels, cat_values=cat_values,
                           trend_labels=trend_labels, trend_values=trend_values)
"""
    return render_template("dashboard.html",
                           income=float(totals.income or 0),
                           expense=float(totals.expense or 0),
                           balance=balance,
                           cat_labels=cat_labels, cat_values=cat_values,
                           trend_labels=trend_labels, trend_values=trend_values)
"""

@transactions_bp.route("/transactions/<int:tx_id>/delete", methods=["POST"])
@login_required
def delete(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.user_id != current_user.id:
        flash("Not found.", "warning")
        return redirect(url_for("transactions.index"))
    db.session.delete(tx)
    db.session.commit()
    flash("Deleted.", "success")
    return redirect(url_for("transactions.index"))


@transactions_bp.route("/transactions/<int:tx_id>/edit", methods=["POST"])
@login_required
def edit(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.user_id != current_user.id:
        flash("Not found.", "warning")
        return redirect(url_for("transactions.index"))

    tx.type = request.form.get("type", tx.type)
    tx.amount = float(request.form.get("amount", tx.amount))
    tx.description = request.form.get("description", tx.description)

    # ✅ Handle date conversion
    t_date_str = request.form.get("date")
    if t_date_str:
        try:
            tx.date = datetime.strptime(t_date_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    cat_id = request.form.get("category_id")
    tx.category_id = int(cat_id) if cat_id else None

    db.session.commit()
    flash("Updated.", "success")
    return redirect(url_for("transactions.index"))


@transactions_bp.route("/transactions/<int:tx_id>/edit", methods=["GET"])
@login_required
def edit_form(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.user_id != current_user.id:
        flash("Not found.", "warning")
        return redirect(url_for("transactions.index"))
    categories = db.session.query(Category).filter_by(user_id=current_user.id).order_by(Category.name).all()
    return render_template("edit_transaction.html", transaction=tx, categories=categories)
