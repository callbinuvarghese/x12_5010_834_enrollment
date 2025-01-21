import re
from typing import Optional,List,Literal
from loguru import logger
from edi_utils import split_edi_file_to_segments
from ins_class import INS,REF,DTP,NM1,PER,N3,N4,DMG,HD
from ins_excel import create_excel

# Example usage (splitting from a file):
input_file = "edi_x834.edi"  # Replace with your input file

def parse_ins_segment(edi_segments:List[str])->List[INS]:
    ins_segments=[]
    ins_segments_count=0
    current_ins_segment:INS=None

    for segment in edi_segments:
        if segment.startswith("INS*"):
            logger.info(f"INS Segment: {segment}")
            seg_INS=INS.from_line_ins_segment(segment)
            seg_INS.init_INS_HD()
            logger.info(seg_INS)
            if current_ins_segment:
                ins_segments.append(current_ins_segment)
                ins_segments_count += 1
                logger.info(f"Appended INS Segment: {ins_segments_count}")
            current_ins_segment=seg_INS
            # if ins_segments_count>10:
            #     break
        elif segment.startswith("REF*"):
            logger.info(f"REF Segment: {segment}")
            seg_INS_REF=REF.from_line_ins_ref_segment(segment)
            logger.info(seg_INS_REF)
            current_ins_segment.ref_segments.append(seg_INS_REF)
        elif segment.startswith("DTP*"):
            logger.info(f"DTP Segment: {segment}")
            if not current_ins_segment:
                logger.error("DTP Segment found without INS Segment. Ignoring it as it may be a header segment.")
                continue
            seg_INS_DTP=DTP.from_line_ins_dtp_segment(segment)
            logger.info(seg_INS_DTP)
            current_ins_segment.dtp_segments.append(seg_INS_DTP)
        elif segment.startswith("NM1*"):
            logger.info(f"NM1 Segment: {segment}")
            seg_INS_NM1=NM1.from_line_ins_nm1_segment(segment)
            logger.info(seg_INS_NM1)
            if current_ins_segment.nm1_segment:
                logger.info(f"Aleady an NM1 Segment exists. Overwitring it with new one.{ins_segments_count}")
                current_ins_segment.nm1_segment.append(seg_INS_NM1)
            else:
                current_ins_segment.nm1_segment=seg_INS_NM1
        elif segment.startswith("PER*"):
            logger.info(f"PER Segment: {segment}")
            seg_INS_PER=PER.from_line_ins_per_segment(segment)
            logger.info(seg_INS_PER)
            if current_ins_segment.per_segment:
                logger.info(f"Aleady an PER Segment exists. Overwitring it with new one.{ins_segments_count}")
                current_ins_segment.per_segment=seg_INS_PER
            else:
                current_ins_segment.per_segment=seg_INS_PER
        elif segment.startswith("N3*"):
            logger.info(f"N3 Segment: {segment}")
            seg_INS_N3=N3.from_line_ins_n3_segment(segment)
            logger.info(seg_INS_N3)
            if current_ins_segment.n3_segment:
                logger.info(f"Aleady an N3 Segment exists. Overwitring it with new one.{ins_segments_count}")
                current_ins_segment.n3_segment=seg_INS_N3
            else:
                current_ins_segment.n3_segment=seg_INS_N3
        elif segment.startswith("N4*"):
            logger.info(f"N4 Segment: {segment}")
            seg_INS_N4=N4.from_line_ins_n4_segment(segment)
            logger.info(seg_INS_N4)
            if current_ins_segment.n4_segment:
                logger.info(f"Aleady an N4 Segment exists. Overwitring it with new one.{ins_segments_count}")
                current_ins_segment.n4_segment=seg_INS_N4
            else:
                current_ins_segment.n4_segment=seg_INS_N4
        elif segment.startswith("DMG*"):
            logger.info(f"DMG Segment: {segment}")
            seg_INS_DMG=DMG.from_line_ins_dmg_segment(segment)
            logger.info(seg_INS_DMG)
            if current_ins_segment.dmg_segment:
                logger.info(f"Aleady an DMG Segment exists. Overwitring it with new one.{ins_segments_count}")
                current_ins_segment.dmg_segment=seg_INS_DMG
            else:
                current_ins_segment.dmg_segment=seg_INS_DMG
        elif segment.startswith("HD*"):
            logger.info(f"HD Segment: {segment}")
            seg_INS_HD=HD.from_line_ins_hd_segment(segment)
            logger.info(seg_INS_HD)
            if current_ins_segment.hd_segment:
                logger.info(f"Aleady an HD Segment exists. Overwitring it with new one.{ins_segments_count}")
                current_ins_segment.hd_segment=seg_INS_HD
            else:
                current_ins_segment.hd_segment=seg_INS_HD
        else:
            if segment.startswith("ISA*"):
                logger.info(f"ISA Segment: {segment}")
            elif segment.startswith("GS*"):
                logger.info(f"GS Segment: {segment}")
            elif segment.startswith("ST*"):
                logger.info(f"ST Segment: {segment}")
            elif segment.startswith("SE*"):
                logger.info(f"SE Segment: {segment}")
            elif segment.startswith("GE*"):
                logger.info(f"GE Segment: {segment}")
            elif segment.startswith("IEA*"):
                logger.info(f"IEA Segment: {segment}")
            elif segment.startswith("BGN*"):
                logger.info(f"BGN Segment: {segment}")
            else:
                logger.info(f"Unknown Segment: {segment}")
    return ins_segments


if __name__=="main":
    edi_segments=split_edi_file_to_segments("../edi_x834.edi")
    logger.info(f"total count of segments: {len(edi_segments)}")
    ins_segments=parse_ins_segment(edi_segments)
    logger.info(f"total count of segments: {len(ins_segments)}")
    create_excel(ins_segments)