# Auto generated from utdo.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-09-22T19:18:48
# Schema: odrl_simple
#
# id: http://w3id.org/ontology/odrl_simple
# description: Simple ODRL Extraction Template
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime, time
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
ODRL = CurieNamespace('odrl', 'http://www.w3.org/ns/odrl/2/')
ODRL_SIMPLE = CurieNamespace('odrl_simple', 'http://w3id.org/ontology/odrl_simple')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
DEFAULT_ = ODRL_SIMPLE


# Types

# Class references
class NamedEntityId(extended_str):
    pass


class PartyId(NamedEntityId):
    pass


class PolicyId(NamedEntityId):
    pass


class RuleId(NamedEntityId):
    pass


class PermissionId(RuleId):
    pass


class ProhibitionId(RuleId):
    pass


class ObligationId(RuleId):
    pass


class ActionId(NamedEntityId):
    pass


class TerminateId(ActionId):
    pass


class ModifyId(ActionId):
    pass


class ConsentId(ActionId):
    pass


class DeleteId(ActionId):
    pass


class ConstraintId(NamedEntityId):
    pass


@dataclass(repr=False)
class NamedEntity(YAMLRoot):
    """
    A named entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["NamedEntity"]
    class_class_curie: ClassVar[str] = "odrl_simple:NamedEntity"
    class_name: ClassVar[str] = "NamedEntity"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.NamedEntity

    id: Union[str, NamedEntityId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedEntityId):
            self.id = NamedEntityId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Party(NamedEntity):
    """
    A party that can be assigned a role in a policy
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Party"]
    class_class_curie: ClassVar[str] = "odrl_simple:Party"
    class_name: ClassVar[str] = "Party"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Party

    id: Union[str, PartyId] = None
    name: str = None
    type: Union[str, "PartyType"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PartyId):
            self.id = PartyId(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, PartyType):
            self.type = PartyType(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Policy(NamedEntity):
    """
    A group of one or more Rules
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Policy"]
    class_class_curie: ClassVar[str] = "odrl_simple:Policy"
    class_name: ClassVar[str] = "Policy"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Policy

    id: Union[str, PolicyId] = None
    name: str = None
    rules: Union[Union[str, RuleId], List[Union[str, RuleId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PolicyId):
            self.id = PolicyId(self.id)

        if self._is_empty(self.rules):
            self.MissingRequiredField("rules")
        if not isinstance(self.rules, list):
            self.rules = [self.rules] if self.rules is not None else []
        self.rules = [v if isinstance(v, RuleId) else RuleId(v) for v in self.rules]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Rule(NamedEntity):
    """
    An abstract concept that represents the common characteristics of Permissions, Prohibitions, and Duties.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Rule"]
    class_class_curie: ClassVar[str] = "odrl_simple:Rule"
    class_name: ClassVar[str] = "Rule"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Rule

    id: Union[str, RuleId] = None
    name: str = None
    actions: Union[str, ActionId] = None
    constraints: Optional[Union[str, ConstraintId]] = None
    assignee: Optional[Union[str, PartyId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RuleId):
            self.id = RuleId(self.id)

        if self._is_empty(self.actions):
            self.MissingRequiredField("actions")
        if not isinstance(self.actions, ActionId):
            self.actions = ActionId(self.actions)

        if self.constraints is not None and not isinstance(self.constraints, ConstraintId):
            self.constraints = ConstraintId(self.constraints)

        if self.assignee is not None and not isinstance(self.assignee, PartyId):
            self.assignee = PartyId(self.assignee)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Permission(Rule):
    """
    A rule that allows an action to be taken
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Permission"]
    class_class_curie: ClassVar[str] = "odrl_simple:Permission"
    class_name: ClassVar[str] = "Permission"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Permission

    id: Union[str, PermissionId] = None
    name: str = None
    actions: Union[str, ActionId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PermissionId):
            self.id = PermissionId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Prohibition(Rule):
    """
    A rule that prohibits an action from being taken
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Prohibition"]
    class_class_curie: ClassVar[str] = "odrl_simple:Prohibition"
    class_name: ClassVar[str] = "Prohibition"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Prohibition

    id: Union[str, ProhibitionId] = None
    name: str = None
    actions: Union[str, ActionId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProhibitionId):
            self.id = ProhibitionId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Obligation(Rule):
    """
    A rule that requires an action to be taken
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Obligation"]
    class_class_curie: ClassVar[str] = "odrl_simple:Obligation"
    class_name: ClassVar[str] = "Obligation"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Obligation

    id: Union[str, ObligationId] = None
    name: str = None
    actions: Union[str, ActionId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObligationId):
            self.id = ObligationId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Action(NamedEntity):
    """
    An action that can be taken
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Action"]
    class_class_curie: ClassVar[str] = "odrl_simple:Action"
    class_name: ClassVar[str] = "Action"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Action

    id: Union[str, ActionId] = None
    name: str = None
    target: Optional[Union[str, "ActionTargetType"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActionId):
            self.id = ActionId(self.id)

        if self.target is not None and not isinstance(self.target, ActionTargetType):
            self.target = ActionTargetType(self.target)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Terminate(Action):
    """
    The action of terminating a contract
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Terminate"]
    class_class_curie: ClassVar[str] = "odrl_simple:Terminate"
    class_name: ClassVar[str] = "Terminate"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Terminate

    id: Union[str, TerminateId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TerminateId):
            self.id = TerminateId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Modify(Action):
    """
    The action of modifying a contract
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Modify"]
    class_class_curie: ClassVar[str] = "odrl_simple:Modify"
    class_name: ClassVar[str] = "Modify"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Modify

    id: Union[str, ModifyId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ModifyId):
            self.id = ModifyId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Consent(Action):
    """
    The action of consenting to something
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Consent"]
    class_class_curie: ClassVar[str] = "odrl_simple:Consent"
    class_name: ClassVar[str] = "Consent"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Consent

    id: Union[str, ConsentId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConsentId):
            self.id = ConsentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Delete(Action):
    """
    The action of deleting something
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Delete"]
    class_class_curie: ClassVar[str] = "odrl_simple:Delete"
    class_name: ClassVar[str] = "Delete"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Delete

    id: Union[str, DeleteId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DeleteId):
            self.id = DeleteId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Constraint(NamedEntity):
    """
    A condition that must be satisfied for the rule to be enforced
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ODRL_SIMPLE["Constraint"]
    class_class_curie: ClassVar[str] = "odrl_simple:Constraint"
    class_name: ClassVar[str] = "Constraint"
    class_model_uri: ClassVar[URIRef] = ODRL_SIMPLE.Constraint

    id: Union[str, ConstraintId] = None
    name: str = None
    type: Union[Union[str, "ConstraintType"], List[Union[str, "ConstraintType"]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConstraintId):
            self.id = ConstraintId(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, list):
            self.type = [self.type] if self.type is not None else []
        self.type = [v if isinstance(v, ConstraintType) else ConstraintType(v) for v in self.type]

        super().__post_init__(**kwargs)


# Enumerations
class PartyType(EnumDefinitionImpl):
    """
    The role of the party in a policy
    """
    PROVIDER = PermissibleValue(
        text="PROVIDER",
        description="The provider of a service.")
    CONSUMER = PermissibleValue(
        text="CONSUMER",
        description="The consumer of a service.")

    _defn = EnumDefinition(
        name="PartyType",
        description="The role of the party in a policy",
    )

class ActionTargetType(EnumDefinitionImpl):
    """
    The type of asset
    """
    PERSONAL_DATA = PermissibleValue(
        text="PERSONAL_DATA",
        description="Personal data")
    NON_PERSONAL_DATA = PermissibleValue(
        text="NON_PERSONAL_DATA",
        description="Non-personal data")
    CONTRACT = PermissibleValue(
        text="CONTRACT",
        description="The contract itself")

    _defn = EnumDefinition(
        name="ActionTargetType",
        description="The type of asset",
    )

class ConstraintType(EnumDefinitionImpl):
    """
    The type of constraint applied to a rule
    """
    UNILATERALLY = PermissibleValue(
        text="UNILATERALLY",
        description="If the action can be taken unilaterally by the assignee")
    NO_PIOR_NOTICE_REQUIRED = PermissibleValue(
        text="NO_PIOR_NOTICE_REQUIRED",
        description="If prior notice is not required before the action is taken")
    NO_CONSENT_REQUIRED = PermissibleValue(
        text="NO_CONSENT_REQUIRED",
        description="If consent is not required the other party before the action is taken")

    _defn = EnumDefinition(
        name="ConstraintType",
        description="The type of constraint applied to a rule",
    )

# Slots
class slots:
    pass

slots.namedEntity__id = Slot(uri=ODRL_SIMPLE.id, name="namedEntity__id", curie=ODRL_SIMPLE.curie('id'),
                   model_uri=ODRL_SIMPLE.namedEntity__id, domain=None, range=URIRef)

slots.namedEntity__name = Slot(uri=ODRL_SIMPLE.name, name="namedEntity__name", curie=ODRL_SIMPLE.curie('name'),
                   model_uri=ODRL_SIMPLE.namedEntity__name, domain=None, range=str)

slots.party__type = Slot(uri=ODRL_SIMPLE.type, name="party__type", curie=ODRL_SIMPLE.curie('type'),
                   model_uri=ODRL_SIMPLE.party__type, domain=None, range=Union[str, "PartyType"])

slots.policy__rules = Slot(uri=ODRL_SIMPLE.rules, name="policy__rules", curie=ODRL_SIMPLE.curie('rules'),
                   model_uri=ODRL_SIMPLE.policy__rules, domain=None, range=Union[Union[str, RuleId], List[Union[str, RuleId]]])

slots.rule__actions = Slot(uri=ODRL_SIMPLE.actions, name="rule__actions", curie=ODRL_SIMPLE.curie('actions'),
                   model_uri=ODRL_SIMPLE.rule__actions, domain=None, range=Union[str, ActionId])

slots.rule__constraints = Slot(uri=ODRL_SIMPLE.constraints, name="rule__constraints", curie=ODRL_SIMPLE.curie('constraints'),
                   model_uri=ODRL_SIMPLE.rule__constraints, domain=None, range=Optional[Union[str, ConstraintId]])

slots.rule__assignee = Slot(uri=ODRL_SIMPLE.assignee, name="rule__assignee", curie=ODRL_SIMPLE.curie('assignee'),
                   model_uri=ODRL_SIMPLE.rule__assignee, domain=None, range=Optional[Union[str, PartyId]])

slots.action__target = Slot(uri=ODRL_SIMPLE.target, name="action__target", curie=ODRL_SIMPLE.curie('target'),
                   model_uri=ODRL_SIMPLE.action__target, domain=None, range=Optional[Union[str, "ActionTargetType"]])

slots.constraint__type = Slot(uri=ODRL_SIMPLE.type, name="constraint__type", curie=ODRL_SIMPLE.curie('type'),
                   model_uri=ODRL_SIMPLE.constraint__type, domain=None, range=Union[Union[str, "ConstraintType"], List[Union[str, "ConstraintType"]]])
