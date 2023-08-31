import json
import re
from datetime import datetime

from utils import number_digits, get_last_n_digits, get_first_n_digits, format_year_short, format_year_month

from client import Copper


def main(args):
    try:
        new_opportunity_ids = args.get("ids")
        if not new_opportunity_ids:
            raise AttributeError("Opportunities ids is required")

        copper_client = Copper('https://api.copper.com/developer_api/v1')

        processed_ids = []
        for opportunity_id in new_opportunity_ids:
            opportunity_data = copper_client.fetch_opportunity(opportunity_id)
            if opportunity_data['pipeline_id'] != copper_client.target_pipeline_id:
                raise AttributeError("Opportunity {0} is not in the correct pipeline".format(opportunity_id))
            match = re.search(r"^Numerador \|(.*)$", opportunity_data['name'])
            if match is None:
                raise AttributeError('Card title does not comply with pattern')
            groups = match.groups()

            last_opportunities = copper_client.search_last_opportunity()
            sorted_opportunities = copper_client.sort_by_proposal_number(last_opportunities)
            last_number_used = copper_client.get_target_custom_field_value(sorted_opportunities[0])

            digits = number_digits(last_number_used)
            last_yearly_number_used = get_last_n_digits(last_number_used, digits - 4)
            last_used_year = str(get_first_n_digits(last_number_used, 2))
            now = datetime.now()
            current_year = format_year_short(now)

            if last_used_year != current_year:
                last_yearly_number_used = -1

            next_proposal_number = "{0}{1}".format(format_year_month(now), last_yearly_number_used + 1)
            target_pipeline_stages_ids = copper_client.fetch_pipeline_stages_ids(copper_client.target_pipeline_id)
            copper_client.update_opportunity(opportunity_id, {
                'name': "RSE {0} |{1}".format(next_proposal_number, groups[0]),
                'pipeline_stage_id': target_pipeline_stages_ids[1] if opportunity_data['pipeline_stage_id'] == target_pipeline_stages_ids[0] else opportunity_data['pipeline_stage_id'],
                'custom_fields': [
                    {
                        'custom_field_definition_id': copper_client.target_custom_field_definition_id,
                        'value': next_proposal_number
                    }
                ]
            })
            processed_ids.append(opportunity_id)
        return {
            'success': True,
            'message': "Opportunities with ids {ids} processed with success".format(ids=processed_ids)
        }
    except BaseException as exc:
        print(json.dumps({'success': False, 'exc': type(exc).__name__, 'message': str(exc)}))
        return {'success': False, 'exc': type(exc).__name__, 'message': str(exc)}
