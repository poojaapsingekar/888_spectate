from flask_restx import Resource, fields, Namespace
from flask import request
from db_models import create_selection, edit_selection, get_selections_with_name_like
from event import event_input_model

ns = Namespace('Selection APIs', description='CRUD on selection')

selection_name = fields.String(required=True, description="Name indicating the event", example="football")
selection_event = fields.Nested(event_input_model)
selection_price = fields.Float(required=True, description="Price of the selection", example=12.5)
selection_active = fields.Boolean(required=True, description="Flag to indicate if a selection is active or not", example=True)
selection_outcome = fields.String(required=True, description="Selection outcome", enum=["Unsettled", "Void", "Lose", "Win"], example="Win")

selection_input_model = ns.model('Selection APIs', {'name': selection_name, 'selection_event': selection_event, 'selection_price': selection_price, 'selection_active': selection_active, 'selection_outcome': selection_outcome})

selection_patch_input_model = ns.model('Selection PATCH API', {'name': selection_name, 'new_selection': fields.Nested(selection_input_model)})


#The below method is to allocate the  resource
@ns.route('selection')
class Selection(Resource):
    @ns.expect(selection_input_model)
    def post(self):
        name = request.json.get('name')
        event = request.json.get('selection_event')
        price = request.json.get('selection_price')
        active = request.json.get('selection_active')
        outcome = request.json.get('selection_outcome')
        _ = create_selection(name, event, price, active, outcome)
        return {'name': name, 'event': event, 'price': price, 'active': active, 'outcome': outcome}

    @ns.doc(params={
        'name_like': {'in': 'query', 'description': 'Regular Expression to match the event name', 'default': r'ck|ba', 'required': False},
    },)
    def get(self):
        """
        This is a get method for selections with name like regex pattern
        """
        selections = []
        if request.args.get('name_like'):
            name_like = request.args.get('name_like')
            selections = get_selections_with_name_like(name_like)
        return selections



    @ns.expect(selection_patch_input_model)
    def patch(self):
        name = request.json.get('name')
        new_selection = request.json.get('new_selection')
        edit_selection(name, new_selection)





