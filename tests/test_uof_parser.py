import sys
import os

import tika
from tika import parser
import yaml

# Add parent dir to path to import module
sys.path.insert(1, os.path.realpath((os.path.join(sys.path[0], '..'))))
from uof_parser.use_of_force_parser import UOFParser, convert_input_to_regex


config = yaml.safe_load(open('uof_parser/config.yaml'))
tika.initVM()


def perform_check(uof_parser, lexipol, year_of_policy, true_indicators, false_indicators):
    # Check lexipol
    assert uof_parser.lexipol is lexipol

    # Check year of policy
    assert uof_parser.year_of_policy == year_of_policy

    # Check policy indicators
    for policy, policy_indicators in config.items():
        search_terms = policy_indicators.get('search_terms', [])
        positive_indicator_phrases = policy_indicators.get('phrases_for_positive_indicator', [])
        positive_indicator_phrases = [] if positive_indicator_phrases is None else positive_indicator_phrases
        result = uof_parser.perform_search(search_terms, positive_indicator_phrases)
        if result[0]:
            try:
                assert policy in true_indicators
            except AssertionError:
                print('Regular expressions used', [convert_input_to_regex(p) for p in positive_indicator_phrases])
                raise Exception(f'{policy} should be False but came back as True.\nLanguage found: {result[1]}')
        else:
            try:
                assert policy in false_indicators
            except AssertionError:
                print('Regular expressions used', [convert_input_to_regex(p) for p in positive_indicator_phrases])
                raise Exception(f'{policy} should be True but came back as False.\nLanguage found: {result[1]}')
    return True


def test_harrisonburg_va():
    # Give file path and expected indicator outcomes
    file_path = f'{os.getcwd()}/tests/example_policies/harrisonburg_va.pdf'
    parsed = parser.from_file(file_path)
    uof_parser = UOFParser(parsed["content"])
    assert perform_check(
        uof_parser,
        lexipol=True,
        year_of_policy='2020',
        true_indicators=[
            'bans_chokeholds_and_strangleholds', 'duty_to_intervene', 'requires_warning_before_shooting',
            'bans_shooting_at_moving_vehicle'
        ],
        false_indicators=[
            'requires_deescalation', 'requires_exhaustion_of_all_other_means', 'has_use_of_force_continumm',
            'requires_comprehensive_reporting'
        ]
    )


def test_lafayette_in():
    # Give file path and expected indicator outcomes
    file_path = f'{os.getcwd()}/tests/example_policies/lafayette_in.pdf'
    parsed = parser.from_file(file_path)
    uof_parser = UOFParser(parsed["content"])

    # NOTE: Manually moved "ban_shooting_at_moving_vehicle" to false because of this language:
    #   An officer should only discharge a firearm at a moving vehicle or its occupants when the officer
    #   reasonably believes there are no other reasonable means available to avert the threat of the
    #   vehicle

    assert perform_check(
        uof_parser,
        lexipol=True,
        year_of_policy='2017',
        true_indicators=[
             'duty_to_intervene', 'requires_warning_before_shooting', 'has_use_of_force_continumm'
        ],
        false_indicators=[
            'requires_deescalation', 'bans_chokeholds_and_strangleholds', 'requires_comprehensive_reporting',
            'requires_exhaustion_of_all_other_means', 'bans_shooting_at_moving_vehicle'
        ]
    )


def test_pueblo_co():
    # Give file path and expected indicator outcomes
    file_path = f'{os.getcwd()}/tests/example_policies/pueblo_co.pdf'
    parsed = parser.from_file(file_path)
    uof_parser = UOFParser(parsed["content"])

    # NOTE: Manually moved "ban_shooting_at_moving_vehicle" to false because of this language:
    #   An officer should only discharge a firearm at a moving vehicle or its occupants when the officer
    #   reasonably believes there are no other reasonable means available to avert the threat of the
    #   vehicle

    assert perform_check(
        uof_parser,
        lexipol=True,
        year_of_policy='2018',
        true_indicators=[
            'duty_to_intervene', 'requires_warning_before_shooting', 'has_use_of_force_continumm',
        ],
        false_indicators=[
            'requires_deescalation', 'bans_chokeholds_and_strangleholds', 'requires_exhaustion_of_all_other_means',
            'requires_comprehensive_reporting', 'bans_shooting_at_moving_vehicle'
        ]
    )


def test_vancouver_wa():
    # Give file path and expected indicator outcomes
    file_path = f'{os.getcwd()}/tests/example_policies/vancouver_wa.pdf'
    parsed = parser.from_file(file_path)
    uof_parser = UOFParser(parsed["content"])

    # NOTE: Manually moved "ban_shooting_at_moving_vehicle" to false because of this language:
    #   An officer should only discharge a firearm at a moving vehicle or its occupants when the officer
    #   reasonably believes there are no other reasonable means available to avert the threat of the
    #   vehicle

    assert perform_check(
        uof_parser,
        lexipol=True,
        year_of_policy='2019',
        true_indicators=[
            'requires_deescalation', 'duty_to_intervene', 'requires_warning_before_shooting',
        ],
        false_indicators=[
            'bans_chokeholds_and_strangleholds', 'requires_exhaustion_of_all_other_means',
            'requires_comprehensive_reporting', 'bans_shooting_at_moving_vehicle', 'has_use_of_force_continumm',
        ]
    )