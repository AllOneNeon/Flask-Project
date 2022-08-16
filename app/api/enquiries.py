from app import db
from app.api import api
from app.decorators import permission_required
from app.models import Enquiry, Post, Permission

from flask import (
    current_app,
    g,
    jsonify,
    request,
    url_for,
)


@api.route('/enquiries/')
def get_enquiries():
    page = request.args.get('page', 1, type=int)
    pagination = Enquiry.query.order_by(Enquiry.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_ENQUIRIES_PER_PAGE'],
        error_out=False)
    enquiries = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_enquiries', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_enquiries', page=page+1)
    return jsonify({
        'enquiries': [enquiry.to_json() for enquiry in enquiries],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/enquiries/<int:id>')
def get_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)
    return jsonify(enquiry.to_json())


@api.route('/posts/<int:id>/enquiries/')
def get_post_enquiries(id):
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.enquiries.order_by(Enquiry.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_ENQUIRIES_PER_PAGE'],
        error_out=False)
    enquiries = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_post_enquiries', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_post_enquiries', id=id, page=page+1)
    return jsonify({
        'enquiries': [enquiry.to_json() for enquiry in enquiries],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>/enquiries/', methods=['POST'])
@permission_required(Permission.ENQUIRY)
def new_post_enquiries(id):
    post = Post.query.get_or_404(id)
    enquiry = Enquiry.from_json(request.json)
    enquiry.author = g.current_user
    enquiry.post = post
    db.session.add(enquiry)
    db.session.commit()
    return jsonify(enquiry.to_json()), 201, \
        {'Location': url_for('api.get_enquiry', id=enquiry.id)}