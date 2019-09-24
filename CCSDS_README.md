# CCSDS Documentation
The CCSDS stack is a series of standard protocols for space communications covering all
the layers of the network stack, from the physical layer to the application layer. Each of the
CCSDS protocols is described in a Blue Book (recommended standards). More
information about design decisions for each protocol can be found in its Green Book
(informational report).

In every example framework the initial setup is the following:
* There is a Message Strobe block that creates a trigger every 1k ms (1s)
* The Message Strobe sends this trigger to a Random PDU Generator block
* Random PDU Generator block generates random bytes in the defined size spectum that are used as a payload

Blue Books used in this implementation:
* TC Space Data Link Protocol (CCSDS 232.1-B-2)
* Space Packet Protocol (CCSDS 133.0-B-1)
* TM Space Data Link Protocol (CCSDS 132.0-B-2)
* Time Code Formats (CCSDS 301.0-B-4) 
* TM Synchronization and Channel Coding (CCSDS 131.0-B-3)

## Space Packet Protocol and a flowgraph without a timestamp
In this flowgraph, the payload is feeded to the Space Packet Primary Header Adder block.
That block is directly connected to the Space Packet Parser block, which in turn prints the whole packet.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.
* The Space Packet Parser receives the packet and by choosing "No" in the Time Header option, it prints the packet showing just the Primary Header(every attribute) and the payload (as bytes).

## Space Packet Protocol and a flowgraph with a timestamp
In this flowgraph, the payload is feeded to the Message Strobe block triggers every 1 second the Random PDU Generator that generates random bytes (payload). That is feeded to the Space Packet Primary Header Adder block.
That block is directly connected to the Space Packet Parser block, which in turn prints the whole packet.

* The Space Packet Time Stamp Adder block adds a timestamp as a Secondary Header between the payload and the Primary Header. The various formats are describe din the Time Code Formats Blue Book (CCSDS 301.0-B-4). The existence of a PField and Time Format has to be chosen here and in the Space Packet Parser.

* The Time Format Parameters block is a global variable struct that defines the variables needed for each time format used in this flowgraph. The id of this block needs to be added both in the Space Packet Time Stamp Adder block and in the Space Packet Parser block.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.

* The Space Packet Parser receives the packet and by choosing "Yes" in the Time Header option, defining the time format and defining the use or not of the PField, it prints the packet showing the Primary Header(every attribute) the timestamp(every attribute) and the (optionally) PField and the payload (as bytes).

## Space Packet Protocol and a flowgraph with a Path ID demux
In this flowgraph, the payload is feeded to the Space Packet Primary Header Adder block.
That block is directly connected to the Path ID Demultiplexer. That block is connected to 3 Space Packet Parser blocks. It directs the packet to the appropriate block taking account the packet's APID. If the packet's APID is not defined in the vector of the Path ID Demultiplexer block, then it is redirected to the last output (discarded). The Space Packet Parser block, in turn, prints the whole packet.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.
* The Space Packet Parser receives the packet and by choosing "No" in the Time Header option, it prints the packet showing just the Primary Header(every attribute) and the payload (as bytes).

## TC Packet 
In this flowgraph, the payload is feeded to the Telecommand Primary Header Adder block. That block is directly connected to the Telecommand Parser block, which prints the whole packet.
* The Telecommand Primary Header Adder block adds the necessary bytes that are described in the Blue Book. The users can input the data per the needed configuration.
* The Telecommand Parser blokc prints out the data; every attribute of the Primary Header as well as the payload (as bytes).

 
