from pydantic import BaseModel, Field
from typing import Optional, List

# Core Entity Classes

class Party(BaseModel):
    """
    Represents a party in the contract.
    
    Attributes:
    - name: The name of the party (either provider or consumer).
    - role: The role of the party, either 'Provider' or 'Consumer'.
    """
    name: str = Field(..., description="The name of the party (e.g., 'Service Provider Inc.', 'John Doe').")
    role: str = Field(..., description="The role of the party (either 'Provider' or 'Consumer').")


class Law(BaseModel):
    """
    Represents a specific legal code governing the contract.
    
    Attributes:
    - name: The name of the law (e.g., 'US Federal Law').
    - country: The country or jurisdiction where the law applies.
    """
    name: str = Field(..., description="The name of the law (e.g., 'US Federal Law').")
    country: str = Field(..., description="The country or jurisdiction where the law is applicable (e.g., 'USA').")


class Jurisdiction(BaseModel):
    """
    Represents the jurisdiction or geographic area that holds legal authority over the contract.
    
    Attributes:
    - name: The name of the jurisdiction (e.g., 'State of California').
    - country: The country where the jurisdiction exists.
    """
    name: str = Field(..., description="The name of the jurisdiction (e.g., 'State of California').")
    country: str = Field(..., description="The country where the jurisdiction is located.")


class Notice(BaseModel):
    """
    Represents a notice that must be provided to a party (consumer or provider) before certain actions.
    
    Attributes:
    - method: The method of communication (e.g., 'Email', 'Postal Mail').
    - period: The notice period before the action can take place (e.g., '30 days').
    """
    method: str = Field(..., description="The method of communication used for notice (e.g., 'Email', 'Postal Mail').")
    period: Optional[str] = Field(None, description="The notice period before action can take place (e.g., '30 days').")


class Damages(BaseModel):
    """
    Represents the types of damages mentioned in the limitation of liability clauses.
    
    Attributes:
    - malware_damage: Indicates if damages related to malware are covered.
    - physical_injury: Indicates if physical injuries are covered.
    - health_issue: Indicates if health issues are covered.
    - loss_of_life: Indicates if loss of life is covered.
    - gross_negligence: Indicates if gross negligence is covered.
    - intentional_damage: Indicates if intentional damage is covered.
    """
    malware_damage: bool = Field(False, description="Specifies if the provider is liable for damages related to malware.")
    physical_injury: bool = Field(False, description="Specifies if the provider is liable for physical injuries.")
    health_issue: bool = Field(False, description="Specifies if the provider is liable for health-related issues.")
    loss_of_life: bool = Field(False, description="Specifies if the provider is liable for the loss of life.")
    gross_negligence: bool = Field(False, description="Specifies if the provider is exempt from liability for gross negligence.")
    intentional_damage: bool = Field(False, description="Specifies if the provider is exempt from liability for intentional damage.")


class ConsentMethod(BaseModel):
    """
    Represents the methods by which a consumer provides consent to the contract.
    
    Attributes:
    - method: A description of how consent is provided (e.g., 'Clickwrap', 'Browsewrap').
    """
    method: str = Field(..., description="The method by which the consumer provides consent to the contract (e.g., 'Clickwrap', 'Browsewrap').")


class ArbitrationProcess(BaseModel):
    """
    Represents the arbitration process that may be required before legal proceedings.
    
    Attributes:
    - arbitration_location: The location where arbitration takes place (optional).
    - arbitrator_discretion: Whether the arbitrator has full discretion over the process.
    - based_on_law: Indicates if the arbitration process is based on established law.
    """
    arbitration_location: Optional[Jurisdiction] = Field(None, description="The location where arbitration takes place, if specified.")
    arbitrator_discretion: bool = Field(..., description="Indicates whether the arbitrator has full discretion over the arbitration process.")
    based_on_law: bool = Field(..., description="Indicates if the arbitration process is based on established law.")


class Penalty(BaseModel):
    """
    Represents a penalty imposed on a party for certain actions.
    
    Attributes:
    - description: Description of the penalty (e.g., monetary fine, service suspension).
    """
    description: str = Field(..., description="The description of the penalty imposed for certain actions (e.g., 'Monetary fine', 'Service suspension').")


class TerminationReason(BaseModel):
    """
    Represents a reason for the termination of the contract.
    
    Attributes:
    - description: A description of the cause for termination (e.g., breach of contract, violation of terms).
    """
    description: str = Field(..., description="A description of the reason for contract termination (e.g., 'Breach of contract').")


class Action(BaseModel):
    """
    Represents an action that occurs as part of the contract (e.g., termination, content removal).
    
    Attributes:
    - description: The action taken.
    - party_involved: The party performing the action.
    """
    description: str = Field(..., description="The description of the action (e.g., 'Content removal', 'Service suspension').")
    party_involved: Party = Field(..., description="The party responsible for performing the action (e.g., 'Provider').")


class ContentRemovalConditions(BaseModel):
    """
    Represents conditions under which content provided by the consumer can be removed.
    
    Attributes:
    - specific_reasons: Indicates if specific reasons for content removal are provided in the contract.
    - notice_required: Indicates if prior notice is required before content removal.
    - full_discretion: Whether the provider has full discretion to remove content without providing reasons.
    """
    specific_reasons: bool = Field(..., description="Indicates whether the contract specifies explicit reasons for content removal.")
    notice_required: bool = Field(..., description="Indicates whether notice must be given before content is removed.")
    full_discretion: bool = Field(..., description="Indicates whether the provider has full discretion to remove content without giving a reason.")


# Clause Classes (Specialized)

class Clause(BaseModel):
    """
    Base class for contract clauses.
    
    Attributes:
    - clause_type: The type of the clause (e.g., Arbitration, LimitationOfLiability).
    """
    clause_type: str = Field(..., description="The type of the clause (e.g., 'ArbitrationClause', 'LimitationOfLiabilityClause').")


class ArbitrationClause(Clause):
    """
    Represents an arbitration clause in the contract.
    
    Attributes:
    - participation_optional: Whether arbitration is optional for both parties.
    - mandatory_before_court_action: Whether arbitration is mandatory before court action.
    - arbitration_process: Details of the arbitration process.
    - penalties_for_choosing_court: Whether there are penalties for opting for court instead of arbitration.
    """
    participation_optional: bool = Field(..., description="Indicates whether participation in arbitration is optional.")
    mandatory_before_court_action: bool = Field(..., description="Indicates whether arbitration is mandatory before any court proceedings.")
    arbitration_process: ArbitrationProcess = Field(..., description="Details about the arbitration process.")
    penalties_for_choosing_court: Optional[Penalty] = Field(None, description="Penalties imposed for opting to go to court instead of arbitration.")


class GoverningLawClause(Clause):
    """
    Represents the governing law clause.
    
    Attributes:
    - governing_law: The law that governs the contract.
    - is_same_as_consumer_residence: Indicates whether the governing law is the same as the consumer's place of residence.
    """
    governing_law: Law = Field(..., description="The governing law that applies to the contract.")
    is_same_as_consumer_residence: bool = Field(..., description="Indicates whether the governing law matches the consumer's place of residence.")


class JurisdictionClause(Clause):
    """
    Represents the jurisdiction clause, indicating where disputes will be resolved.
    
    Attributes:
    - jurisdiction: The jurisdiction applicable to the contract.
    - is_same_as_consumer_residence: Whether the jurisdiction is the same as the consumer's residence.
    """
    jurisdiction: Jurisdiction = Field(..., description="The jurisdiction that applies for dispute resolution.")
    is_same_as_consumer_residence: bool = Field(..., description="Indicates whether the jurisdiction is the same as the consumer's place of residence.")


class ContentRemovalClause(Clause):
    """
    Represents the content removal clause.
    
    Attributes:
    - conditions_for_removal: The conditions under which content can be removed.
    """
    conditions_for_removal: ContentRemovalConditions = Field(..., description="The conditions that apply to content removal.")


class LimitationOfLiabilityClause(Clause):
    """
    Represents the limitation of liability clause.
    
    Attributes:
    - provider_liable_for_damages: Whether the provider is liable for damages.
    - damages: Specific damages for which the provider is not liable.
    - blanket_phrases_to_limit_liability: Whether blanket phrases (e.g., 'to the fullest extent permissible by law') are used to limit liability.
    - disclaims_liability_for_severe_damages: Whether the provider disclaims liability for physical injury, health issues, or loss of life.
    - exempts_liability_for_gross_negligence: Whether the contract exempts the provider from liability for gross negligence or intentional damage.
    """
    provider_liable_for_damages: bool = Field(..., description="Indicates whether the provider is liable for any damages.")
    damages: Damages = Field(..., description="Specifies the types of damages for which the provider is not liable.")
    blanket_phrases_to_limit_liability: bool = Field(..., description="Indicates whether blanket phrases are used to limit liability.")
    disclaims_liability_for_severe_damages: bool = Field(..., description="Indicates if the provider disclaims liability for serious issues like physical injury or loss of life.")
    exempts_liability_for_gross_negligence: bool = Field(..., description="Indicates whether the provider is exempt from liability for gross negligence.")


class UnilateralModificationClause(Clause):
    """
    Represents a unilateral modification clause, where the provider can make changes without the consumer's consent.
    
    Attributes:
    - circumstances_allowed: The circumstances under which modifications are allowed.
    - requires_notice_before_changes: Whether notice is required before changes are made.
    - minimum_notice_period: The minimum period before changes take effect.
    - consumer_can_terminate_if_disagree: Whether the consumer can terminate the contract if they disagree with the changes.
    - provider_obligations_to_inform: Obligations of the provider to inform the consumer of modifications.
    """
    circumstances_allowed: Optional[str] = Field(None, description="The circumstances under which the provider is allowed to modify the contract unilaterally.")
    requires_notice_before_changes: bool = Field(..., description="Indicates whether the provider must give notice before making any changes to the contract.")
    minimum_notice_period: Optional[str] = Field(None, description="The minimum notice period required before modifications take effect.")
    consumer_can_terminate_if_disagree: bool = Field(..., description="Indicates whether the consumer can terminate the contract if they disagree with the changes.")
    provider_obligations_to_inform: Optional[str] = Field(None, description="Specifies the obligations of the provider to inform the consumer about modifications.")


class UnilateralTerminationClause(Clause):
    """
    Represents a unilateral termination clause, where the provider can terminate the contract.
    
    Attributes:
    - can_terminate_unilaterally: Whether the provider can terminate the contract unilaterally.
    - termination_reasons: Reasons for termination, if specified.
    - termination_without_justified_cause: Whether the provider can terminate without justified cause.
    - notice_required_before_termination: Whether notice is required before termination.
    - notice_period: The period of notice given before termination.
    """
    can_terminate_unilaterally: bool = Field(..., description="Indicates whether the provider can terminate the contract unilaterally.")
    termination_reasons: Optional[List[TerminationReason]] = Field(None, description="The reasons specified for terminating the contract.")
    termination_without_justified_cause: bool = Field(..., description="Indicates whether the provider can terminate the contract without providing a justified cause.")
    notice_required_before_termination: bool = Field(..., description="Indicates whether the provider is required to give notice before terminating the contract.")
    notice_period: Optional[str] = Field(None, description="The notice period provided to the consumer before termination takes effect.")


class ContractByUsingClause(Clause):
    """
    Represents a clause that defines when a consumer is bound by the contract simply by using the service.
    
    Attributes:
    - conditions_binding_consumer: The conditions under which the consumer is bound.
    - consumer_made_aware_before_use: Whether the consumer was made aware of the contract before using the service.
    - consent_methods: Methods by which the consumer consents to the contract.
    - bound_by_using_service: Whether the consumer is legally bound just by using the service.
    """
    conditions_binding_consumer: Optional[str] = Field(None, description="The conditions under which the consumer is legally bound to the contract.")
    consumer_made_aware_before_use: bool = Field(..., description="Indicates whether the consumer was made aware of the contract before using the service.")
    consent_methods: List[ConsentMethod] = Field(..., description="The methods by which the consumer provides consent to the contract.")
    bound_by_using_service: bool = Field(..., description="Indicates whether the consumer is legally bound by the contract simply by using the service.")

class Contract(BaseModel):
    """
    Represents the entire contract, bringing together all parties and clauses.
    
    Attributes:
    - provider: The service provider.
    - consumer: The consumer or user of the service.
    - clauses: A list of all clauses in the contract.
    - consent: The method by which consent is provided.
    """
    provider: Party = Field(..., description="The service provider (party who offers the service).")
    consumer: Party = Field(..., description="The consumer or user of the service.")
    clauses: List[Clause] = Field(..., description="A list of clauses that form part of the contract.")
    consent: Optional[ConsentMethod] = Field(None, description="The method by which the consumer provides consent to the contract.")

