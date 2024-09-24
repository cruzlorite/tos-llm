from __future__ import annotations 
from datetime import (
    datetime,
    date,
    time
)
from decimal import Decimal 
from enum import Enum 
import re
import sys
from typing import (
    Any,
    ClassVar,
    List,
    Literal,
    Dict,
    Optional,
    Union
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)
metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'utdo',
     'default_range': 'string',
     'description': 'Simple ODRL Extraction Template',
     'id': 'http://w3id.org/ontology/utdo',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'name': 'utdo',
     'prefixes': {'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'odrl': {'prefix_prefix': 'odrl',
                           'prefix_reference': 'http://www.w3.org/ns/odrl/2/'},
                  'rdf': {'prefix_prefix': 'rdf',
                          'prefix_reference': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'},
                  'utdo': {'prefix_prefix': 'utdo',
                           'prefix_reference': 'http://w3id.org/ontology/utdo'}},
     'source_file': 'src/tos/resources/ontologies/utdo.yaml',
     'title': 'Simple ODRL Extraction Template'} )

class PartyType(str, Enum):
    """
    The role of the party in a policy
    """
    # The provider of a service.
    PROVIDER = "PROVIDER"
    # The consumer of a service.
    CONSUMER = "CONSUMER"


class DeonticModality(str, Enum):
    """
    The type of rule
    """
    # The obligation to do something under the given constraints
    IS_OBLIGATED_TO = "IS_OBLIGATED_TO"
    # The right to do something under the given constraints
    HAS_RIGHT_TO = "HAS_RIGHT_TO"
    # The prohibition to do something under the given constraints
    IS_PROHIBITED_TO = "IS_PROHIBITED_TO"


class ActionType(str, Enum):
    """
    The type of action
    """
    # The action of deleting something: a file, a record, data, user content, etc.
    DELETE = "DELETE"
    # The action of modifying something: the contract, the service, a subscription, etc.
    MODIFY = "MODIFY"
    # The action of suspending the delivery of a service, a subscription, etc.
    SUSPEND = "SUSPEND"
    # The action of giving consent to something, like a contract, a policy, etc.
    CONSENT = "CONSENT"


class ActionTargetType(str, Enum):
    """
    The type of action target
    """
    # User content, for example personal data, a photo, a video, etc.
    USER_CONTENT = "USER_CONTENT"
    # A service, access to a service or similar, for example a subscription, a license, etc.
    SERVICE = "SERVICE"
    # The contract itself
    CONTRACT = "CONTRACT"


class ConstrainType(str, Enum):
    """
    The type of constraint applied to a rule
    """
    # If the action can be taken unilaterally by the assignee
    UNILATERALLY = "UNILATERALLY"
    # If prior notice is not required before the action is taken
    WITHOUT_PRIOR_NOTICE = "WITHOUT_PRIOR_NOTICE"
    # If consent is not required the other party before the action is taken
    WITHOUT_USER_CONSENT = "WITHOUT_USER_CONSENT"
    # if the action can be taken without cause
    WITHOUT_CAUSE = "WITHOUT_CAUSE"



class NamedEntity(ConfiguredBaseModel):
    """
    A named entity
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontology/utdo'})

    id: int = Field(..., description="""The unique identifier of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['NamedEntity']} })
    name: str = Field(..., description="""The name of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['NamedEntity']} })


class Party(NamedEntity):
    """
    A party involved in the contract. A party can be the service provider, the user, the client, etc.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odrl:Party'],
         'from_schema': 'http://w3id.org/ontology/utdo'})

    type: PartyType = Field(..., description="""The type: PROVIDER or CONSUMER""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Party', 'Action']} })
    id: int = Field(..., description="""The unique identifier of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['NamedEntity']} })
    name: str = Field(..., description="""The name of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['NamedEntity']} })


class Policy(ConfiguredBaseModel):
    """
    A group of one or more Rules
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odrl:Policy'],
         'from_schema': 'http://w3id.org/ontology/utdo'})

    rules: List[Rule] = Field(..., description="""The rules that make up the policy""", json_schema_extra = { "linkml_meta": {'alias': 'rules', 'domain_of': ['Policy']} })


class Rule(ConfiguredBaseModel):
    """
    An abstract concept that represents an OBLIGATION, RIGHT or PROHIBITION
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'close_mappings': ['odrl:Rule'],
         'from_schema': 'http://w3id.org/ontology/utdo'})

    actor: Party = Field(..., description="""The party to whom the rule applies to""", json_schema_extra = { "linkml_meta": {'alias': 'assignee', 'domain_of': ['Rule']} })
    modality: DeonticModality = Field(..., description="""The type of rule: IS_OBLIGATED_TO, HAS_RIGTH_TO or IS_PROHIBITED_TO""", json_schema_extra = { "linkml_meta": {'alias': 'modality', 'domain_of': ['Rule']} })
    action: Action = Field(..., description="""The action that is prohibited, obligared or permited""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['Rule']} })
    constrains: Optional[List[ConstrainType]] = Field(None, description="""List of constraints that apply to the rule""", json_schema_extra = { "linkml_meta": {'alias': 'constrains', 'domain_of': ['Rule']} })


class Action(ConfiguredBaseModel):
    """
    An action that can be taken
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odrl:Action'],
         'from_schema': 'http://w3id.org/ontology/utdo'})

    type: ActionType = Field(..., description="""The type of action: delete, modify, distribute, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Party', 'Action']} })
    target: ActionTarget = Field(..., description="""The target of the action""", json_schema_extra = { "linkml_meta": {'alias': 'target', 'domain_of': ['Action']} })


class ActionTarget(NamedEntity):
    """
    Something an action can be taken on. For example, a service, a contract, user data or similar
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'close_mappings': ['odrl:ActionTarget'],
         'from_schema': 'http://w3id.org/ontology/utdo'})

    type: ActionTargetType = Field(..., description="""The type of action target""", json_schema_extra = { "linkml_meta": {'alias': 'type', 'domain_of': ['Party', 'Action', 'Asset']} })
    id: int = Field(..., description="""The unique identifier of the entity""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['NamedEntity']} })
    name: str = Field(..., description="""The name of the target""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['NamedEntity']} })

class PartyList(ConfiguredBaseModel):
    """
    A list of parties
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontology/utdo'})

    parties: List[Party] = Field(..., description="""The list of parties""", json_schema_extra = { "linkml_meta": {'alias': 'parties', 'domain_of': ['PartyList']} })

class ActionTargetList(ConfiguredBaseModel):
    """
    A list of action targets. Basically a list things that an action can be taken on.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://w3id.org/ontology/utdo'})

    targets: List[ActionTarget] = Field(..., description="""The list of action targets""", json_schema_extra = { "linkml_meta": {'alias': 'targets', 'domain_of': ['ActionTargetList']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedEntity.model_rebuild()
Party.model_rebuild()
Policy.model_rebuild()
Rule.model_rebuild()
Action.model_rebuild()
ActionTarget.model_rebuild()

