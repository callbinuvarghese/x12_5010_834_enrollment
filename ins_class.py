import re
from typing import Optional,List,Literal
from pydantic import BaseModel, Field, validator, ValidationError
from loguru import logger
from edi_utils import split_edi_line


class DTP(BaseModel):
    """Date/Time/Period"""
    date_time_qualifier: str = Field(..., description="Date/Time Qualifier", min_length=3, max_length=3)
    date_time_format_qualifier: str = Field(..., description="Date Time Format Qualifier", min_length=2, max_length=2)
    date_time_period: str = Field(..., description="Date Time Period (CCYYMMDD)", min_length=8, max_length=8)
    @staticmethod
    def from_line_ins_dtp_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_DTP fields length: {len(fields)}")
        logger.debug(f"INS_DTP fields: {fields}")
        ins_dtp_data = {
            "date_time_qualifier": fields[1],
            "date_time_format_qualifier": fields[2],
            "date_time_period":  fields[3]}
        logger.debug(f"INS_DTP fields data: {ins_dtp_data}")
        ins_dtp_data_cls=DTP(**ins_dtp_data)
        return ins_dtp_data_cls

                              
class REF(BaseModel):
    """Reference Identification"""
    reference_identification_qualifier: str = Field(...,description="Reference Identification Qualifier",min_length=2,max_length=3, optional=False, pos=1)
    reference_identification: str = Field(...,description="Reference Identification",min_length=1,max_length=50, optional=False, pos=2)
    description: Optional[str] = Field(None,description="Description",max_length=80, optional=False, pos=3)
    @staticmethod
    def from_line_ins_ref_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_REF fields length: {len(fields)}")
        logger.debug(f"INS_REF fields: {fields}")
        ins_ref_data = {
            "reference_identification_qualifier": fields[1],
            "reference_identification": fields[2],
            "description": None}
        logger.debug(f"INS_REF fields data: {ins_ref_data}")
        ins_ref_data_cls=REF(**ins_ref_data)
        return ins_ref_data_cls

class NM1(BaseModel):
    """Individual or Organizational Name"""
    entity_identifier_code: str = Field(..., description="Entity Identifier Code", min_length=2, max_length=2)
    entity_type_qualifier: str = Field(..., description="Entity Type Qualifier", min_length=1, max_length=1)
    name_last_or_organization_name: str = Field(..., description="Name Last or Organization Name", min_length=1, max_length=60)
    name_first: Optional[str] = Field(None, description="Name First", max_length=35)
    name_middle: Optional[str] = Field(None, description="Name Middle", max_length=35)
    identification_code_qualifier: Optional[str] = Field(None, description="Identification Code Qualifier", max_length=2)
    identification_code: Optional[str] = Field(None, description="Identification Code", max_length=80)
    entity_relationship_code: Optional[str] = Field(None, description="Entity Relationship Code", max_length=2)
    entity_identifier_code_2: Optional[str] = Field(None, description="Entity Identifier Code 2", max_length=9)

    @staticmethod
    def from_line_ins_nm1_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_NM1 fields length: {len(fields)}")
        logger.debug(f"INS_NM1 fields: {fields}")
        ins_nm1_data = {
            "entity_identifier_code": fields[1],
            "entity_type_qualifier": fields[2],
            "name_last_or_organization_name": fields[3],
            "name_first": fields[4]
            }
        ins_nm1_data_cls=NM1(**ins_nm1_data)
        try:
            if len(fields) >= 6:
                ins_nm1_data = ins_nm1_data_cls.model_copy(update={"name_middle": fields[5]})
            if len(fields) >= 7:
                ins_nm1_data = ins_nm1_data_cls.model_copy(update={"identification_code_qualifier": fields[6]}) #This will raise error because name is too short
            if len(fields) >= 8:
                ins_nm1_data = ins_nm1_data_cls.model_copy(update={"identification_code": fields[7]}) #This will raise error because name is too short
            if len(fields) >= 9:
                ins_nm1_data = ins_nm1_data_cls.model_copy(update={"entity_relationship_code": fields[8]}) #This will raise error because name is too short
            if len(fields) >= 10:
                ins_nm1_data = ins_nm1_data_cls.model_copy(update={"entity_identifier_code_2": fields[9]}) #This will raise error because name is too short
        except ValidationError as e:
            print("Validation Error: {e}")
        logger.debug(f"INS_NM1 fields data: {ins_nm1_data}")
        return ins_nm1_data_cls

class PER(BaseModel):
    """Individual Name or Organizational Contact"""
    contact_function_code: str = Field(..., description="Contact Function Code", min_length=2, max_length=2)
    contact_enumeration_code: Optional[str] = Field(None, description="Contact Enumeration Code", max_length=2)
    contact_communication_number_qualifier: str = Field(..., description="Contact Communication Number Qualifier", min_length=1, max_length=2)
    contact_communication_number: str = Field(..., description="Contact Communication Number")
    # Additional optional fields are omitted for brevity
    @staticmethod
    def from_line_ins_per_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_PER fields length: {len(fields)}")
        logger.debug(f"INS_PER fields: {fields}")
        ins_per_data = {
            "contact_function_code": fields[1],
            "contact_enumeration_code": fields[2],
            "contact_communication_number_qualifier": fields[3],
            "contact_communication_number": fields[4]
            }
        logger.debug(f"INS_PER fields data: {ins_per_data}")
        ins_per_data_cls=PER(**ins_per_data)
        return ins_per_data_cls

class N3(BaseModel):
    """Party Location"""
    address_information_1: str = Field(..., description="Address Information 1", min_length=1, max_length=55)
    address_information_2: Optional[str] = Field(None, description="Address Information 2", max_length=55)
    @staticmethod
    def from_line_ins_n3_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_N3 fields length: {len(fields)}")
        logger.debug(f"INS_N3 fields: {fields}")
        ins_n3_data = {
            "address_information_1": fields[1]
            }
        logger.debug(f"INS_N3 fields data: {ins_n3_data}")
        ins_n3_data_cls=N3(**ins_n3_data)
        try:
            if len(fields) >= 3:
                ins_n3_data_cls = ins_n3_data_cls.model_copy(update={"address_information_2": fields[2]}) #This will raise error because name is too short
        except ValidationError as e:
            print("Validation Error: {e}")
        return ins_n3_data_cls
    

class N4(BaseModel):
    """Geographic Location"""
    city_name: str = Field(..., description="City Name", min_length=2, max_length=30)
    state_or_province_code: str = Field(..., description="State or Province Code", min_length=2, max_length=2)
    postal_code: str = Field(..., description="Postal Code", min_length=3, max_length=15)
    country_code: Optional[str] = Field(None, description="Country Code", min_length=2, max_length=3)
    location_identifier: Optional[str] = Field(None, description="Location Identifier", max_length=30)
    @staticmethod
    def from_line_ins_n4_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_N4 fields length: {len(fields)}")
        logger.debug(f"INS_N4 fields: {fields}")
        ins_n4_data = {
            "city_name": fields[1],
            "state_or_province_code": fields[2],
            "postal_code": fields[3],
            "country_code": None,
            "location_identifier": None
            }
        logger.debug(f"INS_N4 fields data: {ins_n4_data}")
        ins_n4_data_cls=N4(**ins_n4_data)
        try:
            if len(fields) >= 5:
                ins_n4_data_cls = ins_n4_data_cls.model_copy(update={"country_code": fields[4]}) #This will raise error because name is too short
            if len(fields) >= 6:
                ins_n4_data_cls = ins_n4_data_cls.model_copy(update={"location_identifier": fields[5]}) #This will raise error because name is too short
        except ValidationError as e:
            print("Validation Error: {e}")
        return ins_n4_data_cls

class DMG(BaseModel):
    """Demographic Information"""
    date_time_format_qualifier: Literal["D8"] = Field("D8", description="Date Time Format Qualifier")
    date_time_period: str = Field(..., description="Date Time Period (CCYYMMDD)", max_length=8)
    gender_code: str = Field(..., description="Gender Code", max_length=1)# M: Male, F: Female, U: Unknown
    race_or_ethnicity_code: Optional[str] = Field(None, description="Race or Ethnicity Code", max_length=1)
    @staticmethod
    def from_line_ins_dmg_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_DMG fields length: {len(fields)}")
        logger.debug(f"INS_DMG fields: {fields}")
        ins_dmg_data = {
            "date_time_period": fields[2],
            "gender_code": fields[3],
        }
        logger.debug(f"INS_DMG fields data: {ins_dmg_data}")
        ins_dmg_data_cls=DMG(**ins_dmg_data)
        try:
            if len(fields) >= 5:
                ins_dmg_data_cls = ins_dmg_data_cls.model_copy(update={"race_or_ethnicity_code": fields[4]})
        except ValidationError as e:
            print("Validation Error: {e}")
        logger.debug(f"INS_DMG fields data: {ins_dmg_data_cls}")
        return ins_dmg_data_cls

class HD(BaseModel):
    """Health Coverage Dates"""
    maintenance_reason_code: str = Field(..., description="Maintenance Reason Code", min_length=3, max_length=3)
    maintenance_type_code: Optional[str] = Field(None, description="Maintenance Type Code", max_length=3)
    source_of_submission_code: Literal["HLT"] = Field("HLT", description="Source of Submission Code")
    plan_coverage_description: str = Field(..., description="Plan Coverage Description", min_length=1, max_length=80)
    employee_status_code: Optional[str] = Field(None, description="Employee Status Code")
    @staticmethod
    def from_line_ins_hd_segment(line: str):
        fields=split_edi_line(line)
        logger.debug(f"INS_HD fields length: {len(fields)}")
        logger.debug(f"INS_HD fields: {fields}")
        ins_hd_data = {
            "maintenance_reason_code": fields[1],
            "maintenance_type_code": None,
            "source_of_submission_code": fields[3],
            "plan_coverage_description": fields[4]
        }
        logger.debug(f"INS_HD fields data: {ins_hd_data}")
        ins_hd_data_cls=HD(**ins_hd_data)
        try:
            if len(fields) >= 6:
                ins_hd_data_cls = ins_hd_data_cls.model_copy(update={"employee_status_code": fields[5]})
            if len(fields) >= 7:
                ins_hd_data_cls = ins_hd_data_cls.model_copy(update={"maintenance_type_code": fields[6]})
        except ValidationError as e:
            print("Validation Error: {e}")
        logger.debug(f"INS_HD fields data: {ins_hd_data_cls}")
        return ins_hd_data_cls


class INS(BaseModel):
    """Member Information"""
    yes_no_response_code: str = Field(..., min_length=1, max_length=1, optional=False, pos=1, description="Yes/No Response Y or N")
    dependent_code: str = Field(..., min_length=2, max_length=3, optional=False, pos=2, description="Relatiship to subscriber")
    maintenance_type_code: str = Field(..., min_length=2, max_length=3, optional=False, pos=3, description="Maintenance Type Code 3 digits")
    maintenance_reason_code: Optional[str] = Field(None, max_length=3, optional=True, pos=4, description="Dependent or Relationship Code")  # Increased max length to 3
    benefit_status_code: Optional[str] = Field(None, min_length=1, max_length=1, optional=True, pos=6, description="benefit status code")
    medicare_status_code: Optional[str] = Field(None, min_length=1, max_length=1, optional=True, pos=7, description="medicare status code")
    occ_length_code: Optional[str] = Field(None, min_length=1, max_length=2, optional=True, pos=7, description="Fulltime Parttime etc")
    handicap_ind: Optional[str] = Field(None, min_length=1, max_length=1, optional=True, pos=7, description="Handicap Indicator")
    model_config = {
        "validate_assignment": False  # Disable validation on assignment
    }
    ref_segments: List[REF] = Field([], description="List of REF Segments") #REF as a list inside INS
    dtp_segments: List[REF] = Field([], description="List of DTP Segments") #REF as a list inside INS
    nm1_segment: NM1 = Field(None, description="NM1 Segment") #NM1 as a list inside INS
    per_segment: PER = Field(None, description="PER Segment") #PER as a list inside INS
    n3_segment: N3 = Field(None, description="N3 Segment") #N3 as a list inside INS
    n4_segment: N4 = Field(None, description="N4 Segment") #N4 as a list inside INS
    dmg_segment: DMG = Field(None, description="DMG Segment") #DMG as a list inside INS
    hd_segment: HD = Field(None, description="HD Segment") #HD as a list inside INS


    def init_INS_HD(self):
        self.ref_segments=[]
        self.dtp_segments=[]
        self.nm1_segment=None
        self.per_segment=None
        self.n3_segment=None
        self.n4_segment=None
        self.dmg_segment=None
        self.hd_segment=None

    @staticmethod
    def from_line_ins_segment(line: str):
        fields=split_edi_line(line)
        ins_data = {
            "yes_no_response_code": fields[1],
            "dependent_code": fields[2],
            "maintenance_type_code": fields[3],
            "maintenance_reason_code": fields[4] or None,
            "benefit_status_code": fields[5] or None,
            "medicare_status_code": fields[6] or None,
            "occ_length_code": None,     
            "handicap_ind": None,   
        }
        logger.debug(f"Fields length: {len(fields)}")
        logger.debug(f"INS fields: {ins_data}")
        ins_data_cls=INS(**ins_data)
        try:
            if len(fields) >= 9:
                ins_data_cls = ins_data_cls.model_copy(update={"occ_length_code": fields[8]}) #This will raise error because name is too short
            if len(fields) >= 10:
                ins_data_cls = ins_data_cls.model_copy(update={"handicap_ind": fields[9]}) #This will raise error because name is too short
        except ValidationError as e:
            print("Validation Error: {e}")

        return ins_data_cls

