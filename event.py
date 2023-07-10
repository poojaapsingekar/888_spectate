from flask_restx import Resource, fields, Namespace
from flask import request
from db_models import create_event,get_events_with_name_like, edit_event, get_events_with_min_active_selections


from sport import sport_name, sport_active, sport_slug, sport_input_model

ns = Namespace('Event APIs', description='CRUD on event')


event_name = fields.String(required=True, description="Name indicating the event", example="football")
event_slug = fields.String(required=True, description="URL format for the event name", example="/football_rugby")
event_active = fields.Boolean(required=True, description="Flag to indicate if a event is active or not", example=True)
event_type = fields.String(required=True, description="Flag to indicate if a event is active or not", example="inplay", enum=['inplay', 'preplay'])
event_sport = fields.Nested(sport_input_model)
event_status = fields.String(required=True, description="Status of the event", enum=["Pending", "Started", "Ended", "Cancelled"], example="Started")
event_scheduled_start = fields.String(required=True, description="Scheduled datetime in ISO format in UTC as a string", example="2023-07-08T13:34:03.541312")
event_actual_start = fields.String(required=False, description="Actual datetime in ISO format in UTC as a string", example="2023-07-08T13:34:03.541312")

event_input_model = ns.model('event APIs', {'name': event_name, 'slug': event_slug, 'active': event_active, 'sport': event_sport, 'type': event_type, 'status': event_status, 'scheduled_start': event_scheduled_start, 'actual_start': event_actual_start})
event_patch_input_model = ns.model('event patch API', {'name': event_name, 'new_event': fields.Nested(event_input_model)})

@ns.route('event')
class Event(Resource):
    @ns.expect(event_input_model)
    def post(self):
        name = request.json.get('name')
        slug = request.json.get('slug')
        active = request.json.get('active')
        sport = request.json.get('sport')
        type = request.json.get('type')
        status = request.json.get('status')
        scheduled_start = request.json.get('scheduled_start')
        actual_start = request.json.get('actual_start')

        sport_name=sport["name"]
        create_event(name,slug,active,type,sport_name,status,scheduled_start,actual_start)
        return {'name': name, 'slug': slug, 'active': active, 'sport': sport, 'type': type, 'status': status, 'scheduled_start': scheduled_start, 'actual_start': actual_start}, 200

    @ns.doc(params={
        'name_like': {'in': 'query', 'description': 'Regular Expression to match the event name', 'default': r'ck|ba', 'required': False},
        'num_active_selections': {'in': 'query', 'description': 'Threshold for the number of active selections', 'default': 2, 'required': False},
        'from_datetime': {'in': 'query', 'description': 'Filter to get all the events beyond this datetime un UTC', 'default': '2023-07-08 08:15:30.356415', 'required': False},
        'to_datetime': {'in': 'query', 'description': 'Filter to get all the events upto this datetime un UTC', 'default': '2023-07-08 08:16:34.597997', 'required': False},
    },)
    def get(self):
        name_like_results = []
        active_selection_event_results = []
        if request.args.get('name_like') is not None:
            pattern = request.args.get('name_like')
            name_like_results.extend(get_events_with_name_like(pattern))
        if request.args.get('num_active_selections') is not None:
            num_active_selections = request.args.get('num_active_selections')
            active_selection_event_results.extend(get_events_with_min_active_selections(num_active_selections))
        if len(name_like_results) == 0:
            return active_selection_event_results
        elif len(active_selection_event_results) == 0:
            return name_like_results
        return [name for name in name_like_results if name in active_selection_event_results]
    
    @ns.expect(event_patch_input_model)
    def patch(self):
        name = request.json.get('name')
        new_event = request.json.get('new_event')
        edit_event(name, new_event)




