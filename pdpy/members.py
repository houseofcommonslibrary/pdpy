# -*- coding: utf-8 -*-
"""Functions for downloading and analysing data on Members of either House."""

# Imports ---------------------------------------------------------------------

from . import constants
from . import core

# Raw Members queries ---------------------------------------------------------

def fetch_members_raw(house=None):

    """Fetch key details for Members."""

    # Initialise house constraint
    house_constraint = ''

    # If a house is specified set the house constraint
    if house == constants.PDP_ID_HOUSE_OF_COMMONS or \
        house == constants.PDP_ID_HOUSE_OF_LORDS:
        house_constraint = 'BIND(d:{0} AS ?house)'.format(house)

    # Build the query
    members_query = """
        PREFIX : <https://id.parliament.uk/schema/>
        PREFIX d: <https://id.parliament.uk/>
        SELECT DISTINCT

            ?person_id
            ?mnis_id
            ?given_name
            ?family_name
            ?other_names
            ?display_name
            ?full_title
            ?gender
            ?date_of_birth
            ?date_of_death

        WHERE {{

            # House constraint
            {0}

            ?person_id :memberMnisId ?mnis_id ;
                :personGivenName ?given_name ;
                :personFamilyName ?family_name ;
                <http://example.com/F31CBD81AD8343898B49DC65743F0BDF> ?display_name ;
                <http://example.com/D79B0BAC513C4A9A87C9D5AFF1FC632F> ?full_title ;
                :personHasGenderIdentity/:genderIdentityHasGender/:genderName ?gender ;
                :memberHasParliamentaryIncumbency/:seatIncumbencyHasHouseSeat/:houseSeatHasHouse ?house .
            OPTIONAL {{ ?person_id :personOtherNames ?other_names . }}
            OPTIONAL {{ ?person_id :personDateOfBirth ?date_of_birth . }}
            OPTIONAL {{ ?person_id :personDateOfDeath ?date_of_death . }}
        }}
    """.format(house_constraint)

    return core.sparql_select(members_query)


def fetch_party_memberships_raw(house=None):

    """Fetch party memberships for Members."""

    # Initialise house constraint
    house_constraint = ''

    # If a house is specified set the house constraint
    if house == constants.PDP_ID_HOUSE_OF_COMMONS or \
        house == constants.PDP_ID_HOUSE_OF_LORDS:
        house_constraint = 'BIND(d:{0} AS ?house)'.format(house)

    party_memberships_query = """
        PREFIX : <https://id.parliament.uk/schema/>
        PREFIX d: <https://id.parliament.uk/>
        SELECT DISTINCT

            ?person_id
            ?mnis_id
            ?given_name
            ?family_name
            ?display_name
            ?party_id
            ?party_mnis_id
            ?party_name
            ?party_membership_id
            ?party_membership_start_date
            ?party_membership_end_date

        WHERE {{

            # House constraint
            {0}

            ?person_id :memberMnisId ?mnis_id;
                :personGivenName ?given_name ;
                :personFamilyName ?family_name ;
                <http://example.com/F31CBD81AD8343898B49DC65743F0BDF> ?display_name ;
                :partyMemberHasPartyMembership ?party_membership_id ;
                :memberHasParliamentaryIncumbency/:seatIncumbencyHasHouseSeat/:houseSeatHasHouse ?house .
            ?party_membership_id a :PartyMembership ;
                :partyMembershipHasParty ?party_id ;
                :partyMembershipStartDate ?party_membership_start_date .
            OPTIONAL {{ ?party_membership_id :partyMembershipEndDate ?party_membership_end_date . }}
            ?party_id :partyMnisId ?party_mnis_id ;
                :partyName ?party_name .
        }}
    """.format(house_constraint)

    return core.sparql_select(party_memberships_query)


def fetch_government_roles_raw(house=None):

    """Fetch government roles for Members."""

    # Initialise house constraint
    house_constraint = ''

    # If a house is specified set the house constraint
    if house == constants.PDP_ID_HOUSE_OF_COMMONS or \
        house == constants.PDP_ID_HOUSE_OF_LORDS:
        house_constraint = 'BIND(d:{0} AS ?house)'.format(house)

    government_roles_query = """
        PREFIX : <https://id.parliament.uk/schema/>
        PREFIX d: <https://id.parliament.uk/>
        SELECT DISTINCT

            ?person_id
            ?mnis_id
            ?given_name
            ?family_name
            ?display_name
            ?position_id
            ?position_name
            ?government_incumbency_id
            ?government_incumbency_start_date
            ?government_incumbency_end_date

        WHERE {{

            # House constraint
            {0}

            ?person_id :memberMnisId ?mnis_id;
                :personGivenName ?given_name ;
                :personFamilyName ?family_name ;
                <http://example.com/F31CBD81AD8343898B49DC65743F0BDF> ?display_name ;
                :governmentPersonHasGovernmentIncumbency ?government_incumbency_id ;
                :memberHasParliamentaryIncumbency/:seatIncumbencyHasHouseSeat/:houseSeatHasHouse ?house .
            ?government_incumbency_id a :GovernmentIncumbency ;
                :governmentIncumbencyHasGovernmentPosition ?position_id ;
                :incumbencyStartDate ?government_incumbency_start_date .
            OPTIONAL {{ ?government_incumbency_id :incumbencyEndDate ?government_incumbency_end_date . }}
            ?position_id :positionName ?position_name .
        }}
    """.format(house_constraint)

    return core.sparql_select(government_roles_query)


def fetch_opposition_roles_raw(house=None):

    """Fetch opposition roles for Members."""

    # Initialise house constraint
    house_constraint = ''

    # If a house is specified set the house constraint
    if house == constants.PDP_ID_HOUSE_OF_COMMONS or \
        house == constants.PDP_ID_HOUSE_OF_LORDS:
        house_constraint = 'BIND(d:{0} AS ?house)'.format(house)

    opposition_roles_query = """
        PREFIX : <https://id.parliament.uk/schema/>
        PREFIX d: <https://id.parliament.uk/>
        SELECT DISTINCT

            ?person_id
            ?mnis_id
            ?given_name
            ?family_name
            ?display_name
            ?position_id
            ?position_name
            ?opposition_incumbency_id
            ?opposition_incumbency_start_date
            ?opposition_incumbency_end_date

        WHERE {{

            # House constraint
            {0}

            ?person_id :memberMnisId ?mnis_id;
                :personGivenName ?given_name ;
                :personFamilyName ?family_name ;
                <http://example.com/F31CBD81AD8343898B49DC65743F0BDF> ?display_name ;
                :oppositionPersonHasOppositionIncumbency ?opposition_incumbency_id ;
                :memberHasParliamentaryIncumbency/:seatIncumbencyHasHouseSeat/:houseSeatHasHouse ?house .
            ?opposition_incumbency_id a :OppositionIncumbency ;
                :oppositionIncumbencyHasOppositionPosition ?position_id ;
                :incumbencyStartDate ?opposition_incumbency_start_date .
            OPTIONAL {{ ?opposition_incumbency_id :incumbencyEndDate ?opposition_incumbency_end_date . }}
            ?position_id :positionName ?position_name .
        }}
    """.format(house_constraint)

    return core.sparql_select(opposition_roles_query)


def fetch_committee_memberships_raw(house=None):

    """Fetch committee memberships for Members."""

    # Initialise house constraint
    house_constraint = ''

    # If a house is specified set the house constraint
    if house == constants.PDP_ID_HOUSE_OF_COMMONS or \
        house == constants.PDP_ID_HOUSE_OF_LORDS:
        house_constraint = 'BIND(d:{0} AS ?house)'.format(house)

    committee_memberships_query = """
        PREFIX : <https://id.parliament.uk/schema/>
        PREFIX d: <https://id.parliament.uk/>
        SELECT DISTINCT

            ?person_id
            ?mnis_id
            ?given_name
            ?family_name
            ?display_name
            ?committee_id
            ?committee_name
            ?committee_type_id
            ?committee_type_name
            ?committee_membership_id
            ?committee_membership_start_date
            ?committee_membership_end_date

        WHERE {{

            # House constraint
            {0}

            ?person_id :memberMnisId ?mnis_id;
                :personGivenName ?given_name ;
                :personFamilyName ?family_name ;
                <http://example.com/F31CBD81AD8343898B49DC65743F0BDF> ?display_name ;
                :personHasFormalBodyMembership ?committee_membership_id ;
                :memberHasParliamentaryIncumbency/:seatIncumbencyHasHouseSeat/:houseSeatHasHouse ?house .
            ?committee_membership_id :formalBodyMembershipHasFormalBody ?committee_id ;
                :formalBodyMembershipStartDate ?committee_membership_start_date .
            OPTIONAL {{ ?committee_membership_id :formalBodyMembershipEndDate ?committee_membership_end_date . }}
            ?committee_id a :FormalBody ;
                :formalBodyName ?committee_name .
            OPTIONAL {{
                ?committee_id :formalBodyHasFormalBodyType ?committee_type_id ;
                    :formalBodyHasFormalBodyType/:formalBodyTypeName ?committee_type_name .
            }}
        }}
    """.format(house_constraint)

    return core.sparql_select(committee_memberships_query)
