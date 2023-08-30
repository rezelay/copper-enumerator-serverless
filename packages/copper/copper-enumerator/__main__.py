import json

from client import Copper


def main(args):
    try:
        new_opportunity_ids = args.get("ids")
        if not new_opportunity_ids:
            raise AttributeError("Opportunities ids is required")

        copper_client = Copper('https://api.copper.com/developer_api/v1')

        return {
            'success': True,
            'message': "Opportunities with ids {ids} created with success".format(ids=new_opportunity_ids)
        }
    except BaseException as exc:
        print(json.dumps({'success': False, 'exc': type(exc).__name__, 'message': str(exc)}))
        return {'success': False, 'exc': type(exc).__name__, 'message': str(exc)}
