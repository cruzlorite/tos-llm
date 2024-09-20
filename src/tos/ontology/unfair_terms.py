# ToS: A tool to analyze Terms of Service.
# Copyright (C) 2024 José María Cruz Lorite
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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


linkml_meta = LinkMLMeta({'default_prefix': 'unfair_terms_ontology/',
     'default_range': 'string',
     'description': 'Deontic logic ontology for unfair terms in contracts.',
     'id': 'unfair_terms_ontology',
     'imports': ['linkml:types'],
     'name': 'unfair_terms_ontology',
     'prefixes': {'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'source_file': './src/tos/resources/ontologies/unfair_terms.yaml'} )


class Agent(ConfiguredBaseModel):
    """
    A general agent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'unfair_terms_ontology'})

    name: str = Field(..., description="""The name of the agent.""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent']} })


class Provider(Agent):
    """
    The provider of a service.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    name: str = Field(..., description="""The name of the agent.""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent']} })


class Consumer(Agent):
    """
    The consumer of a service.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    name: str = Field(..., description="""The name of the agent.""", json_schema_extra = { "linkml_meta": {'alias': 'name', 'domain_of': ['Agent']} })


class Action(ConfiguredBaseModel):
    """
    Describes an action that can be taken.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'unfair_terms_ontology'})

    pass


class LitigationCondition(ConfiguredBaseModel):
    """
    A property or condition imposed by the contract that affects litigation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'unfair_terms_ontology'})

    pass


class Arbitration(LitigationCondition):
    """
    Conditions under which arbitration takes place.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    is_fully_optional: bool = Field(..., description="""Is arbitration fully optional for the consumer?""", json_schema_extra = { "linkml_meta": {'alias': 'is_fully_optional', 'domain_of': ['Arbitration']} })
    is_required_before_court: bool = Field(..., description="""Is arbitration required before going to court?""", json_schema_extra = { "linkml_meta": {'alias': 'is_required_before_court', 'domain_of': ['Arbitration']} })
    is_in_consumer_location: bool = Field(..., description="""Is arbitration in the consumer's location, or it has to take place in a location chosen by the service provider?""", json_schema_extra = { "linkml_meta": {'alias': 'is_in_consumer_location', 'domain_of': ['Arbitration']} })
    is_based_on_law: bool = Field(..., description="""Is arbitration based on law or on the arbiter's discretion?""", json_schema_extra = { "linkml_meta": {'alias': 'is_based_on_law', 'domain_of': ['Arbitration']} })


class Jurisdiction(LitigationCondition):
    """
    Jurisdiction where litigation takes place.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    is_consumer_jurisdiction: bool = Field(..., description="""Is dispute resolution required to be in a different city, state, or country from the consumer's residence?""", json_schema_extra = { "linkml_meta": {'alias': 'is_consumer_jurisdiction', 'domain_of': ['Jurisdiction']} })


class GoverningLaw(LitigationCondition):
    """
    Governing law of the contract.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    is_consumer_law: bool = Field(..., description="""Is the governing law in the consumer's location, or it is chosen by the service provider?""", json_schema_extra = { "linkml_meta": {'alias': 'is_consumer_law', 'domain_of': ['GoverningLaw']} })


class LimitationOfLiability(LitigationCondition):
    """
    Limitation of liability.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    provider_liability: bool = Field(..., description="""Is the provider liable for any damages or losses?""", json_schema_extra = { "linkml_meta": {'alias': 'provider_liability', 'domain_of': ['LimitationOfLiability']} })
    malware_liability: bool = Field(..., description="""Is the provider not liable for damages incurred by malware or harmful software?""", json_schema_extra = { "linkml_meta": {'alias': 'malware_liability', 'domain_of': ['LimitationOfLiability']} })
    blanket_phrases: bool = Field(..., description="""Does the contract contain blanket phrases like \"to the fullest extent permissible by law\" to limit liability?""", json_schema_extra = { "linkml_meta": {'alias': 'blanket_phrases', 'domain_of': ['LimitationOfLiability']} })
    physical_injuries: bool = Field(..., description="""Are there provisions in the contract where the provider disclaims liability for physical injuries, health issues, or loss of life?""", json_schema_extra = { "linkml_meta": {'alias': 'physical_injuries', 'domain_of': ['LimitationOfLiability']} })
    gross_negligence: bool = Field(..., description="""Does the contract attempt to exempt the provider from liability for gross negligence or intentional damage?""", json_schema_extra = { "linkml_meta": {'alias': 'gross_negligence', 'domain_of': ['LimitationOfLiability']} })


class RemoveUserContent(Action):
    """
    The action of removing user content.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    unilaterally: bool = Field(..., description="""Can the service provider remove consumer's content?""", json_schema_extra = { "linkml_meta": {'alias': 'allowed',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    full_discretion: bool = Field(..., description="""Does the service provider have full discretion to remove content?""", json_schema_extra = { "linkml_meta": {'alias': 'full_discretion', 'domain_of': ['RemoveUserContent']} })
    no_reason_required: bool = Field(..., description="""Can the service provider remove content without giving a justified reason?""", json_schema_extra = { "linkml_meta": {'alias': 'no_reason_required',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    prior_notice_required: bool = Field(..., description="""Does the service provider have to give prior notice before removing content?""", json_schema_extra = { "linkml_meta": {'alias': 'prior_notice_required',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    retrieval_posibility: bool = Field(..., description="""Can the consumer retrieve the content before it is removed?""", json_schema_extra = { "linkml_meta": {'alias': 'retrieval_posibility', 'domain_of': ['RemoveUserContent']} })


class TerminateContract(Action):
    """
    The action of terminating the contract.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    unilaterally: bool = Field(..., description="""Can the service provider terminate the contract unilateraly?""", json_schema_extra = { "linkml_meta": {'alias': 'allowed',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    no_reason_required: bool = Field(..., description="""Can the service provider terminate the contract without giving a justified reason?""", json_schema_extra = { "linkml_meta": {'alias': 'no_reason_required',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    prior_notice_required: bool = Field(..., description="""Does the service provider have to give prior notice before terminating the contract?""", json_schema_extra = { "linkml_meta": {'alias': 'prior_notice_required',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })


class ModifyContract(Action):
    """
    THe action of modifying the contract.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    unilaterally: bool = Field(..., description="""Can the service provider modify the contract unilateraly?""", json_schema_extra = { "linkml_meta": {'alias': 'allowed',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    no_reason_required: bool = Field(..., description="""Can the service provider modify the contract without giving a justified reason?""", json_schema_extra = { "linkml_meta": {'alias': 'no_reason_required',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })
    prior_notice_required: bool = Field(..., description="""Does the service provider have to give prior notice before modifying the contract?""", json_schema_extra = { "linkml_meta": {'alias': 'prior_notice_required',
         'domain_of': ['RemoveUserContent', 'TerminateContract', 'ModifyContract']} })


class ConsentContract(Action):
    """
    The action of consenting to the contract.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    consent_by_usage: bool = Field(..., description="""Is the user legally bound by the contract just by using the service?""", json_schema_extra = { "linkml_meta": {'alias': 'consent_by_usage', 'domain_of': ['ConsentContract']} })
    no_explicit_consent_required: bool = Field(..., description="""Is the user legally bound by the contract without giving explicit consent?""", json_schema_extra = { "linkml_meta": {'alias': 'no_explicit_consent_required', 'domain_of': ['ConsentContract']} })


class Litigate(Action):
    """
    The action of initiating litigation against the service provider.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    conditions: List[LitigationCondition] = Field(..., description="""Conditions under which litigation takes place.""", json_schema_extra = { "linkml_meta": {'alias': 'conditions', 'domain_of': ['Litigate']} })


class DeonticProposition(ConfiguredBaseModel):
    """
    A deontic modal.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'unfair_terms_ontology'})

    agent: Agent = Field(..., description="""The agent to which the proposition applies.""", json_schema_extra = { "linkml_meta": {'alias': 'agent', 'domain_of': ['DeonticProposition']} })
    action: Action = Field(..., description="""The action that is permitted, prohibited, or obligated.""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['DeonticProposition']} })


class Obligation(DeonticProposition):
    """
    An obligation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    agent: Agent = Field(..., description="""The agent to which the proposition applies.""", json_schema_extra = { "linkml_meta": {'alias': 'agent', 'domain_of': ['DeonticProposition']} })
    action: Action = Field(..., description="""The action that is permitted, prohibited, or obligated.""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['DeonticProposition']} })


class Right(DeonticProposition):
    """
    A right or permission.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    agent: Agent = Field(..., description="""The agent to which the proposition applies.""", json_schema_extra = { "linkml_meta": {'alias': 'agent', 'domain_of': ['DeonticProposition']} })
    action: Action = Field(..., description="""The action that is permitted, prohibited, or obligated.""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['DeonticProposition']} })


class Prohibition(DeonticProposition):
    """
    A prohibition.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'unfair_terms_ontology'})

    agent: Agent = Field(..., description="""The agent to which the proposition applies.""", json_schema_extra = { "linkml_meta": {'alias': 'agent', 'domain_of': ['DeonticProposition']} })
    action: Action = Field(..., description="""The action that is permitted, prohibited, or obligated.""", json_schema_extra = { "linkml_meta": {'alias': 'action', 'domain_of': ['DeonticProposition']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Agent.model_rebuild()
Provider.model_rebuild()
Consumer.model_rebuild()
Action.model_rebuild()
LitigationCondition.model_rebuild()
Arbitration.model_rebuild()
Jurisdiction.model_rebuild()
GoverningLaw.model_rebuild()
LimitationOfLiability.model_rebuild()
RemoveUserContent.model_rebuild()
TerminateContract.model_rebuild()
ModifyContract.model_rebuild()
ConsentContract.model_rebuild()
Litigate.model_rebuild()
DeonticProposition.model_rebuild()
Obligation.model_rebuild()
Right.model_rebuild()
Prohibition.model_rebuild()

