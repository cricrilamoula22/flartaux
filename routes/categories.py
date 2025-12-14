from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Category
from sqlalchemy import text

categories_bp = Blueprint("categories", __name__)

def check_category_id_sequence():
    result = db.session.execute(text("""
        SELECT column_default
        FROM information_schema.columns
        WHERE table_schema = 'w_sadr_artaux'
          AND table_name = 'categories'
          AND column_name = 'id';
    """)).scalar()

    return result is not None and "nextval" in result

@categories_bp.route("/categories", methods=["GET", "POST"])
@login_required
def index():
    uid = current_user.id
    if request.method == "POST":
        name = request.form["name"].strip()
        if not name:
            flash("Category name required.", "warning")
            return redirect(url_for("categories.index"))
        if db.session.query(Category).filter_by(user_id=uid, name=name).first():
            flash("Category already exists.", "warning")
            return redirect(url_for("categories.index"))   
        db.session.add(Category(user_id=uid, name=name)); db.session.commit()
        flash("Category added.", "success")
        return redirect(url_for("categories.index"))
    items = db.session.query(Category).filter_by(user_id=uid).order_by(Category.name).all()
    return render_template("categories.html", categories=items)

@categories_bp.route("/categories/<int:cat_id>/delete", methods=["POST"])
@login_required
def delete(cat_id):
    cat = db.session.get(Category, cat_id)
    if not cat or cat.user_id != current_user.id:
        flash("Not found.", "warning"); return redirect(url_for("categories.index"))
    db.session.delete(cat); db.session.commit()
    flash("Category deleted.", "success")
    return redirect(url_for("categories.index"))
