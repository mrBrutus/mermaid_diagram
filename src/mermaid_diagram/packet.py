"""
Class for creating a Mermaid packet diagram.
Diagram type:`packet-beta`.
"""


class Packet:
    """
    Class for creating a Mermaid packet diagram.
    Diagram type:`packet-beta`.
    """

    def __init__(self, title: str = None, use_number_prefix: bool = False):
        """Class for creating a Mermaid packet diagram.
        Diagram type:`packet-beta`.

        Args:
            title (str, optional):
                Title for the packet diagram. Defaults to None.
            use_number_prefix (bool, optional):
                Add a number prefix to every segment in the packet diagram. Defaults to False.
        """
        self._title = title
        self._use_number_prefix = use_number_prefix
        self._header = ""
        self._segment_content = ""
        self._nr_of_segments = 0
        self._bit_offset = 0

    def _create_header(self):
        """Create the header of the mermaid diagram."""
        if self.title:
            self._header += "---"
            self._header += f'\ntitle: "{self.title}"'
            self._header += "\n---"
        self._header += "\npacket-beta"

    @property
    def header(self):
        """Header of the mermaid diagram."""
        self._create_header()
        return self._header

    @property
    def segment_content(self):
        """Segment content of the mermaid diagram."""
        return self._segment_content

    @property
    def diagram(self):
        """The mermaid diagram."""
        return f"{self.header}{self.segment_content}"

    @property
    def diagram_markdown(self):
        """The mermaid diagram as a markdown codeblock."""
        return f"```mermaid\n{self.diagram}\n```\n"

    @property
    def title(self):
        """Title of the mermaid diagram."""
        return self._title

    @title.setter
    def title(self, title: str):
        """Title of the mermaid diagram."""
        self._title = title

    @property
    def nr_of_segments(self):
        """Number of segments in the mermaid diagram."""
        return self._nr_of_segments

    @property
    def size_in_bits(self):
        """Total size of the segments in `bits`"""
        return self._bit_offset

    @property
    def size_in_bytes(self):
        """Total size of the segments as `bytes.bits`"""
        return self._bits_to_bytes_bits(self.size_in_bits)

    @property
    def use_number_prefix(self):
        """Segments using a numbering prefix."""
        return self._use_number_prefix

    @use_number_prefix.setter
    def use_number_prefix(self, value: bool):
        """Segments using a numbering prefix."""
        self._use_number_prefix = value

    def add_segment_bits(self, nr_of_bits: int, text: str = None):
        """Append a segment with size specified in `bits` to the mermaid diagram.

        Args:
            nr_of_bits (int): Size of the segment in `bits`.
            text (str): Text displayed inside the segment.
        """

        address = f"\n{self._bit_offset}"
        if nr_of_bits > 1:
            address += f"-{self._bit_offset + nr_of_bits - 1}"
        self._bit_offset += nr_of_bits
        self._nr_of_segments += 1

        name = ""
        if self.use_number_prefix:
            name += f"{self.nr_of_segments})"

        if name:
            name += " "

        if text:
            name += f"{text}"

        self._segment_content += f'{address} : "{name}"'

    def add_segment_bytes(self, nr_of_bytes: int | float, text: str = None):
        """Append a segment with size specified in `bytes` or `bytes.bits` to the mermaid diagram.

        Args:
            nr_of_bytes (int | float): Size of the segment in `bytes` or `bytes.bits`.
            nr_of_bits (int): Size of the segment in `bits`.
            text (str): Text displayed inside the segment. Defaults to None.
        """

        nr_of_bits = self._bytes_bits_to_bits(nr_of_bytes)
        self.add_segment_bits(nr_of_bits, text)

    @staticmethod
    def _bits_to_bytes_bits(bits: int):
        """Convert a number of bits into `bytes.bits`"""
        bytes_part = bits // 8
        bits_part = bits % 8

        if bits_part == 0:
            return int(bytes_part)
        else:
            return float(f"{bytes_part}.{bits_part}")

    @staticmethod
    def _bytes_bits_to_bits(bytes_dot_bits: int | float):
        """Convert a size in `bytes.bits` to a number of bits"""
        integer_part = int(bytes_dot_bits)
        fractional_part = bytes_dot_bits - integer_part

        bits = integer_part * 8 + int(fractional_part * 10)
        return bits
