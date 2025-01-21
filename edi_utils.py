from loguru import logger
import re

def split_edi_line(line: str, field_separator: str = "*", segment_terminator: str = "~") -> list[str]:
    """Splits an EDI line into its constituent fields.

    Handles empty fields and preserves trailing delimiters if specified.
    """
    if not line:
        return []

    if line.endswith(segment_terminator):
        line = line[:-1] #Remove segment terminator before split

    fields = line.split(field_separator)
    return fields

def split_edi_to_segments(edi_content):
    """
    Splits EDI content into newline-delimited segments.

    Args:
        edi_content: The EDI content as a string.

    Returns:
        A string where each segment is on a new line, or None if an error occurs.
    """
    if not edi_content:
        return None

    try:
        # Normalize line endings (replace \r\n and \r with \n)
        edi_content = edi_content.replace('\r\n', '\n').replace('\r', '\n')

        # Split by segment terminator (~) while handling escaped terminators (\~)
        segments = re.split(r'(?<!\\)~', edi_content)

        # Remove empty strings from the list of segments
        segments = [s.strip() for s in segments if s.strip()]

        # Replace escaped terminators with regular terminators
        segments = [s.replace('\\~', '~') for s in segments]


        return "\n".join(segments)

    except Exception as e:
        print(f"An error occurred during splitting: {e}")
        return None


def split_edi_file_to_segments_file(input_filepath, output_filepath):
    """
    Splits an EDI file into newline-delimited segments and writes to a new file.

    Args:
        input_filepath: Path to the input EDI file.
        output_filepath: Path to the output file.
    """
    try:
        with open(input_filepath, 'r') as infile:
            edi_content = infile.read()

        segmented_content = split_edi_to_segments(edi_content)

        if segmented_content:
            with open(output_filepath, 'w') as outfile:
                outfile.write(segmented_content)
            print(f"EDI file split and saved to: {output_filepath}")
        else:
            print("Failed to split the EDI file.")

    except FileNotFoundError:
        print(f"Input file not found: {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


def split_edi_to_segments(edi_content):
    """
    Splits EDI content into newline-delimited segments.

    Args:
        edi_content: The EDI content as a string.

    Returns:
        list of segments, or None if an error occurs.
    """
    if not edi_content:
        return None

    try:
        # Normalize line endings (replace \r\n and \r with \n)
        edi_content = edi_content.replace('\r\n', '\n').replace('\r', '\n')

        # Split by segment terminator (~) while handling escaped terminators (\~)
        segments = re.split(r'(?<!\\)~', edi_content)

        # Remove empty strings from the list of segments
        segments = [s.strip() for s in segments if s.strip()]

        # Replace escaped terminators with regular terminators
        segments = [s.replace('\\~', '~') for s in segments]

        return segments

    except Exception as e:
        print(f"An error occurred during splitting: {e}")
        return None


def split_edi_file_to_segments(input_filepath):
    """
    Splits an EDI file into newline-delimited segments and writes to a new file.

    Args:
        input_filepath: Path to the input EDI file.
    return: Segmented content as a list of segments
    """
    try:
        logger.debug(f"Input File Path: {input_filepath}")
        with open(input_filepath, 'r') as infile:
            edi_content = infile.read()

        segmented_content = split_edi_to_segments(edi_content)
        return segmented_content
    except FileNotFoundError:
        print(f"Input file not found: {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

