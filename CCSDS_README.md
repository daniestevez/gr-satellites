# CCSDS Documentation
The CCSDS stack is a series of standard protocols for space communications covering all
the layers of the network stack, from the physical layer to the application layer. Each of the
CCSDS protocols is described in a Blue Book (recommended standards). More
information about design decisions for each protocol can be found in its Green Book
(informational report).

## Space Packet Protocol and a flowgraph without a timestamp
In this flowgraph, the Message Strobe block triggers every 1 second the Random PDU Generator that generates random bytes (payload). That is feeded to the Space Packet Primary Header Adder block.
That block is directly connected to the Space Packet Parser block, which in turn prints the whole packet.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.
* The Space Packet Parser receives the packet and by choosing "No" in the Time Header option, it prints the packet showing just the Primary Header(every attribute) and the payload (as bytes).

## Space Packet Protocol and a flowgraph with a timestamp
In this flowgraph, the Message Strobe block triggers every 1 second the Random PDU Generator that generates random bytes (payload). That is feeded to the Space Packet Primary Header Adder block.
That block is directly connected to the Space Packet Parser block, which in turn prints the whole packet.

* The Space Packet Time Stamp Adder block adds a timestamp as a Secondary Header between the payload and the Primary Header. The various formats are describe din the Time Code Formats Blue Book (CCSDS 301.0-B-4). The existence of a PField and Time Format has to be chosen here and in the Space Packet Parser.

* The Time Format Parameters block is a global variable struct that defines the variables needed for each time format used in this flowgraph. The id of this block needs to be added both in the Space Packet Time Stamp Adder block and in the Space Packet Parser block.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.

* The Space Packet Parser receives the packet and by choosing "Yes" in the Time Header option, defining the time format and defining the use or not of the PField, it prints the packet showing the Primary Header(every attribute) the timestamp(every attribute) and the (optionally) PField and the payload (as bytes).
