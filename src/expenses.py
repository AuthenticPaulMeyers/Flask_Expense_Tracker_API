from flask import Blueprint, jsonify



expenses=Blueprint('expenses', __name__, url_prefix='/api/v1.0/expenses')


@expenses.get("/get_all")
def get_all_expnses():
    return jsonify({'data': "all expenses"})