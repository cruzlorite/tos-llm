import getpass
import os

os.environ["OPENAI_API_KEY"] = "sk-Vn416fJ5l5gRRNoQnaIIMEbepS7T_EyaxWv8d3eTqIT3BlbkFJfReJ5s0y1hv82SWyit1aaKwM_PkX_Fx6c4GZjvsqoA"

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

from tos.ontology.unfair_terms import DeonticProposition

structured_llm = llm.with_structured_output(DeonticProposition)

output = structured_llm.invoke("""
You are an expert Knowledge Engineer and you are working on a project to build a knowledge graph.
YGiven the input ontology in LinkML format, you are required to generate a deontic proposition that captures the input text.

Ontology: '''
id: unfair_terms_ontology
name: unfair_terms_ontology
description: Deontic logic ontology for unfair terms in contracts.
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Agent:
    abstract: true
    description: A general agent.
    attributes:
      name:
        range: string
        required: true
        description: The name of the agent.

  Provider:
    is_a: Agent
    description: The provider of a service.

  Consumer:
    is_a: Agent
    description: The consumer of a service.

  Action:
    abstract: true
    description: Describes an action that can be taken.

  LitigationCondition:
    abstract: true
    description: A property or condition imposed by the contract that affects litigation.

  Arbitration:
    is_a: LitigationCondition
    description: Conditions under which arbitration takes place.
    attributes:
      is_fully_optional:
        range: boolean
        required: true
        description: Is arbitration fully optional for the consumer?
      is_required_before_court:
        range: boolean
        required: true
        description: Is arbitration required before going to court?
      is_in_consumer_location:
        range: boolean
        required: true
        description: Is arbitration in the consumer's location, or it has to take place in a location chosen by the service provider?
      is_based_on_law:
        range: boolean
        required: true
        description: Is arbitration based on law or on the arbiter's discretion?

  Jurisdiction:
    is_a: LitigationCondition
    description: Jurisdiction where litigation takes place.
    attributes:
      is_consumer_jurisdiction:
        range: boolean
        required: true
        description: Is dispute resolution required to be in a different city, state, or country from the consumer's residence?

  GoverningLaw:
    is_a: LitigationCondition
    description: Governing law of the contract.
    attributes:
      is_consumer_law:
        range: boolean
        required: true
        description: Is the governing law in the consumer's location, or it is chosen by the service provider?

  LimitationOfLiability:
    is_a: LitigationCondition
    description: Limitation of liability.
    attributes:
      provider_liability:
        range: boolean
        required: true
        description: Is the provider liable for any damages or losses?
      malware_liability:
        range: boolean
        required: true
        description: Is the provider not liable for damages incurred by malware or harmful software?
      blanket_phrases:
        range: boolean
        required: true
        description: Does the contract contain blanket phrases like "to the fullest extent permissible by law" to limit liability?
      physical_injuries:
        range: boolean
        required: true
        description: Are there provisions in the contract where the provider disclaims liability for physical injuries, health issues, or loss of life?
      gross_negligence:
        range: boolean
        required: true
        description: Does the contract attempt to exempt the provider from liability for gross negligence or intentional damage?

  RemoveUserContent:
    is_a: Action
    description: The action of removing user content.
    attributes:
      unilaterally:
        range: boolean
        required: true
        description: Can the service provider remove consumer's content?
      full_discretion:
        range: boolean
        required: true
        description: Does the service provider have full discretion to remove content?
      no_reason_required:
        range: boolean
        required: true
        description: Can the service provider remove content without giving a justified reason?
      prior_notice_required:
        range: boolean
        required: true
        description: Does the service provider have to give prior notice before removing content?
      retrieval_posibility:
        range: boolean
        required: true
        description: Can the consumer retrieve the content before it is removed?
        
  TerminateContract:
    is_a: Action
    description: The action of terminating the contract.
    attributes:
      unilaterally:
        range: boolean
        required: true
        description: Can the service provider terminate the contract unilateraly?
      no_reason_required:
        range: boolean
        required: true
        description: Can the service provider terminate the contract without giving a justified reason?
      prior_notice_required:
        range: boolean
        required: true
        description: Does the service provider have to give prior notice before terminating the contract?

  ModifyContract:
    is_a: Action
    description: THe action of modifying the contract.
    attributes:
      unilaterally:
        range: boolean
        required: true
        description: Can the service provider modify the contract unilateraly?
      no_reason_required:
        range: boolean
        required: true
        description: Can the service provider modify the contract without giving a justified reason?
      prior_notice_required:
        range: boolean
        required: true
        description: Does the service provider have to give prior notice before modifying the contract?

  ConsentToContract:
    is_a: Action
    description: The action of consenting to the contract.
    attributes:
      consent_by_usage:
        range: boolean
        required: true
        description: Is the user legally bound by the contract just by using the service?
      no_explicit_consent_required:
        range: boolean
        required: true
        description: Is the user legally bound by the contract without giving explicit consent?

  Litigate:
    is_a: Action
    description: The action of initiating litigation against the service provider.
    attributes:
      conditions:
        range: LitigationCondition
        required: true
        multivalued: true
        description: Conditions under which litigation takes place.

  DeonticProposition:
    description: A deontic modal.
    abstract: true
    attributes:
      agent:
        range: Agent 
        required: true
        description: The agent to which the proposition applies.
      action:
        range: Action
        required: true
        description: The action that is permitted, prohibited, or obligated.
        
  Obligation:
    is_a: DeonticProposition
    description: An obligation.
    
  Right:
    is_a: DeonticProposition
    description: A right or permission.

  Prohibition:
    is_a: DeonticProposition
    description: A prohibition.
'''

The text is as follows: '''
GitHub has the right to suspend or terminate your access to all or any part of the Website at any time, with or without cause, with or without notice, effective immediately. GitHub reserves the right to refuse service to anyone for any reason at any time.
'''
""")