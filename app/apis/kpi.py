# server/app/apis/kpi.py

import app.models
from flask import (
    jsonify,
    request,
)

from app import db
from app.apis import kpi_blueprint as kpi
from app.apis.auth import protected_route
from app.models import User, Company

KPI = {
    'sales': app.models.Sale,
    'traffic': app.models.Traffic,
    'subscribers': app.models.Subscriber,
    'engagement': app.models.Engagement,
    'mrr': app.models.MRR,
    'pilots': app.models.Pilot,
    'active_users': app.models.ActiveUser,
    'paying_users': app.models.PayingUser,
    'cpa': app.models.CPA,
    'product_releases': app.models.ProductRelease,
    'preorders': app.models.Preorder,
    'automation_percents': app.models.AutomationPercentage,
    'conversion_rate': app.models.ConversionRate,
    'marketing_spent': app.models.MarketingSpent,
    'other_1': app.models.Other1,
    'other_2': app.models.Other2,
}


def get_kpi_for_company(company_id):
    metric_field = {}

    for metric in KPI:
        kpi_query = KPI[metric].query.filter_by(company_id=company_id)
        total_weeks = kpi_query.count()
        values = kpi_query.order_by(KPI[metric].week).all()
        last_updated = KPI[metric].get_last_updated(company_id).updated_at \
            if KPI[metric].get_last_updated(company_id) else 'NOT AVAILABLE'

        metric_field[metric] = {
            'weeks': total_weeks,
            'last_updated': last_updated,
            'data': list(map(
                lambda value: value.value,
                values
            ))
        }

    return metric_field


@kpi.route('/companies/<int:company_id>', methods=['POST'])
@protected_route
def post_company(company_id, resp=None):
    user = User.query.get(resp)
    if not user.staff \
        and (not user.founder_info
             or user.founder_info.company_id != company_id):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

    if not request.json:
        return jsonify({
            'status': 'failure',
            'message': 'empty metrics'
        }), 400

    for metric in request.json:
        if request.json[metric] == '':
            return jsonify({
                'status': 'failure',
                'message': 'one of the metrics is empty'
            }), 400

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    response_data = {
        'metrics_added': {}
    }

    for metric in request.json:
        KPI[metric](
            company_id=company_id,
            value=request.json[metric]
        ).save()
        response_data['metrics_added'][metric] = request.json[metric]

    response_data['status'] = 'success'
    response_data['message'] = 'metrics added'

    return jsonify(response_data), 201


@kpi.route('/companies/<int:company_id>/metrics', methods=['GET'])
@protected_route
def get_metrics(company_id, resp=None):
    user = User.query.get(resp)
    if not user.staff \
        and (not user.founder_info
             or user.founder_info.company_id != company_id):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    response_obj = {}

    response_obj = get_kpi_for_company(company_id)

    return jsonify(response_obj), 200


@kpi.route('/companies/<int:company_id>/metrics', methods=['PUT'])
@protected_route
def put_metric(company_id, resp=None):
    user = User.query.get(resp)
    if not user.staff \
        and (not user.founder_info
             or user.founder_info.company_id != company_id):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    for metric in request.json:
        # if there is no data in the database
        if KPI[metric].query.count() == 0:
            return jsonify({
                'status': 'failure',
                'message': 'there is no data to update'
            }), 400

    for metric in request.json:
        KPI[metric].get_last_updated(company_id).value = request.json[metric]
        db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'resource updated'
    }), 200
