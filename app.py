from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = 'expenses.json'

# Initialize expense categories
CATEGORIES = {
    'food': '食品消费',
    'transport': '交通消费',
    'housing': '居家物业',
    'electronics': '电子产品',
    'social': '人情往来'
}

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_expenses(expenses):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    expenses = load_expenses()
    return render_template('index.html', categories=CATEGORIES, expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    expenses = load_expenses()
    
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']
    
    # Get year and month for grouping
    year_month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
    
    if year_month not in expenses:
        expenses[year_month] = {}
    
    if category not in expenses[year_month]:
        expenses[year_month][category] = []
    
    expenses[year_month][category].append({
        'date': date,
        'amount': amount,
        'description': description
    })
    
    save_expenses(expenses)
    return redirect(url_for('index'))

@app.route('/stats')
def statistics():
    expenses = load_expenses()
    
    # Calculate monthly totals
    monthly_stats = {}
    for month, categories in expenses.items():
        monthly_stats[month] = {}
        for category, items in categories.items():
            monthly_stats[month][category] = sum(item['amount'] for item in items)
    
    return render_template('stats.html', stats=monthly_stats, categories=CATEGORIES)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
