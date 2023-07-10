from flask_restx import Resource, fields, Namespace
from flask import request
from db_models import create_sport, get_sports_with_namelike, get_sports_with_min_active_events, edit_sport
ns = Namespace('Sport APIs', description='CRUD on Sport')


sport_name = fields.String(required=True, description="Name indicating the sport", example="football")
sport_slug = fields.String(required=True, description="URL format for the sport name", example="/football_rugby")
sport_active = fields.Boolean(required=True, description="Flag to indicate if a sport is active or not", example=True)

sport_input_model = ns.model('Sport APIs', {'name': sport_name, 'slug': sport_slug, 'active': sport_active})

sport_patch_input_model = ns.model('Sport Patch API', {'name': sport_name, 'new_sport': fields.Nested(sport_input_model)})


@ns.route('sport')
class Sport(Resource):
    @ns.expect(sport_input_model)
    def post(self):
        name = request.json.get('name')
        slug = request.json.get('slug')
        active = request.json.get('active')
        create_sport(name, slug, active)
        return {'name': name, 'slug': slug, 'active': active}

    @ns.doc(params={
        'name_like': {'in': 'query', 'description': 'Regular Expression to match the sport name', 'default': r'ck|ba', 'required': False},
        'num_active_events': {'in': 'query', 'description': 'Threshold for the number of active events', 'default': 2, 'required': False},
    },)
    def get(self):
        name_like_results = []
        active_event_sport_results = []
        if request.args.get('name_like') is not None:
            pattern = request.args.get('name_like')
            name_like_results.extend(get_sports_with_namelike(pattern))
        if request.args.get('num_active_events') is not None:
            num_active_events = request.args.get('num_active_events')
            active_event_sport_results.extend(get_sports_with_min_active_events(num_active_events))
        if len(name_like_results) == 0:
            return active_event_sport_results
        elif len(active_event_sport_results) == 0:
            return name_like_results
        return [name for name in name_like_results if name in active_event_sport_results]

    @ns.expect(sport_patch_input_model)
    def patch(self):
        name = request.json.get('name')
        new_sport = request.json.get('new_sport')
        edit_sport(name, new_sport)
