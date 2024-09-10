from typing import Any

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Relation


def get_data_from_model(feature_model: FeatureModel, filtered_ingredients: list[str]) -> dict[str, Any]:
    return process_feature(feature_model.root, filtered_ingredients)

def process_feature(feature: Feature, filtered_ingredients: list[str]) -> dict[str, Any]:
    _dict: dict[str, Any] = {}
    if not filtered_ingredients or feature.name in filtered_ingredients or not feature.is_leaf():
        _dict['name'] = feature.name
    relationships = []
    for relation in feature.get_relations():
        relationships.append(process_relation(relation, filtered_ingredients))
    _dict['relations'] = relationships
    return _dict


def process_relation(relation: Relation, filtered_ingredients: list[str] ) -> dict[str, Any]:
    _dict: dict[str, Any] = {}
    _dict['card_min'] = relation.card_min
    _dict['card_max'] = relation.card_max
    if relation.is_mandatory():  # [1..1] and only one children
        relation_type = 'MANDATORY'
    elif relation.is_optional():  # [0..1] and only one children
        relation_type = 'OPTIONAL'
    if relation.is_or():  # [1..n] and two or more children
        relation_type = 'OR'
    elif relation.is_alternative():  # [1..1] and two or more children
        relation_type = 'XOR'
    elif relation.is_mutex():  # [0..1] and two or more children
        relation_type = 'MUX'
    elif relation.is_cardinal():  # [a..b] and two or more children
        relation_type = 'CARDINAL'
    _dict['type'] = relation_type
    children = []
    for child in relation.children:
        children.append(process_feature(child, filtered_ingredients))
    _dict['children'] = children
    return _dict