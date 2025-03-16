from flask import Blueprint, jsonify, request
from src.database import Expense, db, Category
from src.constants.http_status_codes import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc


expenses=Blueprint('expenses', __name__, url_prefix='/api/v1.0/expenses')

# display all expenses
@expenses.get("/get_all")
@jwt_required()
def get_all_expnses():
    current_user_id=get_jwt_identity()

    page=request.args.get('page', 1, type=int)
    per_Page=request.args.get('per_page', 10, type=int)

    all_expenses=db.session.query(Expense.id, Expense.amount, Expense.description, Expense.date, Category.name, Expense.category_id).join(Category).filter(Expense.user_id==current_user_id).order_by(Expense.date.desc()).paginate(page=page, per_page=per_Page)

    data=[]

    for expense in all_expenses.items:
        data.append(
            {
            'id': expense.id,
            'category_id': expense.category_id,
            'amount': expense.amount,
            'description': expense.description,
            'date': expense.date,
            }
        )
        
    if data == []:
        return jsonify({"message": "You do not have any transaction"}), HTTP_200_OK
    

    metadata={
        'page': all_expenses.page,
        'has_next': all_expenses.has_next,
        'has_prev': all_expenses.has_prev,
        'total_pages': all_expenses.total,
        'per_page': all_expenses.per_page,
        'next_page': all_expenses.next_num,
        'prev_page': all_expenses.prev_num
    }

    return jsonify({'data': data, 'metadata': metadata}), HTTP_200_OK


# add expenses route
@expenses.post('/add')
@jwt_required()
def add_expenses():
    current_user_id=get_jwt_identity()
    amount=request.json.get('amount')
    category=request.json.get('category')
    description=request.json.get('description')

    category=category.capitalize()
    
    CATEGORY=Category.query.all()
    categories=[]
    for item in CATEGORY:
        categories.append(item.name)
    
    # validate the user input
    if amount == " " or category == " " or description == " ":
        return jsonify({"error": "required fields should not be empty"}), HTTP_400_BAD_REQUEST
    
    if not amount.isnumeric():
        return jsonify({"error": "amount should be a number"}), HTTP_400_BAD_REQUEST
    
    if category not in categories:
        return jsonify({"error": "category out of range"}), HTTP_400_BAD_REQUEST
    
    # get category id
    get_category=Category.query.filter(Category.name == category).first()

    if get_category:
        category_id = get_category.id
    
    # add to the database
    expense=Expense(amount=amount, category_id=category_id, description=description, user_id=current_user_id)
    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "message": "transaction added",
        "transaction":{
             "amount": amount,
             "category": get_category.name,
             "description": description,
             "category": category
        }
    }), HTTP_201_CREATED
