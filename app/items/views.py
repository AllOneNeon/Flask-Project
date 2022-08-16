from flask import render_template
from . import items


@items.route('/', methods=['GET', 'POST'])
def index():
    return render_template('items/index.html')