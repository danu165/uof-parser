import tika
from tika import parser
from uof_parser.use_of_force_parser import UOFParser
import yaml


def internal_cols_to_spreadsheet():
    return {
        'police_department': 'Police Department',
        'reviewed': 'Reviewed?',
        'state': 'State',
        'link_to_policy': 'Link to Policy',
        'slack_contributor': 'Slack Handle of Person Contributing to Policy',
        'lexipol': 'Does the policy say/note that it was created by Lexipol? (1=Yes, 0=No, .5 = Hybrid)',
        'requires_deescalation': 'Requires De-Escalation',
        'requires_deescalation_language': ('(Policy Language) Requires De-Escalation: Does the policy require officers '
                                           'to de-escalate situations, when possible?'),
        'ban_choke': 'Bans Chokeholds and Strangleholds',
        'bank_choke_language': ('(Policy Language) Bans Chokeholds and Strangleholds: Are chokeholds and '
                                'strangleholds (including carotid restraints) explicitly prohibited, except in '
                                'situations where deadly force is authorized?'),
        'duty_to_intervene': 'Duty to Intervene',
        'duty_to_intervene_language': ('(Policy Language) Duty to Intervene: Are officers required to intervene when '
                                       'witnessing another officer using excessive force?'),
        'warn_before_shoot': 'Requires Warning Before Shooting',
        'warn_before_shoot_language': ('(Policy Language) Requires Warning Before Shooting: Are officers required to '
                                       'give a verbal warning, when possible, before shooting someone?'),
        'ban_vehicle_shoot': 'Restricts Shooting at Moving Vehicles',
        'ban_vehicle_shoot_language': ('(Policy Language) Restricts Shooting at Moving Vehicles: Are officers '
                                       'prohibited from shooting at people in moving vehicles unless the subject '
                                       'presents a separate deadly threat other than the vehicle itself?'),
        'requires_comprehensive_reporting': 'Requires Comprehensive Reporting',
        'requires_comprehensive_reporting_language': ('(Policy Language) Requires Comprehensive Reporting: Are all uses'
                                                      ' of force required to be reported, including the pointing of a '
                                                      'firearm at a civilian?'),
        'all_other_means': 'Requires Exhaust All Other Means Before Shooting',
        'all_other_means_language': ('(Policy Language) Requires Exhaust All Other Means Before Shooting: Are officers '
                                     'required to exhaust all other reasonable alternatives before resorting to deadly '
                                     'force?'),
        'use_of_force_continuum': 'Has Use of Force Continuum',
        'use_of_force_continuum_language': ('(Policy Language) Has Use of Force Continuum: Is a Force Continuum or '
                                            'Matrix included in the Policy, defining the types of force/weapons that '
                                            'can be used to respond to specific types of resistance?'),
        'year_of_policy': 'Year of Most Recent Policy'
    }


def main():
    url = 'https://www.harrisonburgva.gov/sites/default/files/Police/files/POLICIES/Use_of_Force-1.pdf'
    file_path = '/Users/dturcan/Docs/campaign_zero/use_of_force_docs/harrisonburg_va.pdf'

    # Extract all of the lines
    tika.initVM()
    parsed = parser.from_file(file_path)
    content = parsed["content"]
    uof_parser = UOFParser(content)

    # Read in config
    config = yaml.safe_load(open('../config.yaml'))

    # Run indicators:
    for policy, policy_indicators in config.items():
        print('-------------')
        print("Checking", policy)
        result = uof_parser.perform_search(policy_indicators.get('search_terms', []),
                                           policy_indicators.get('phrases_for_positive_indicator', []))
        print()
        print(policy, ":", result[0])
        print('Context:')
        print(result[1])
        print()


if __name__ == '__main__':
    main()
