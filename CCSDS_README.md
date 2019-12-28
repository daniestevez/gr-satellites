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

The flowgraphs can be found in the /examples folder.

## Space Packet Protocol and a flowgraph without a timestamp
In this [Space_Packet_without_TimeStamp](examples/Space_Packet_without_TimeStamp.grc), the payload is fed to the Space Packet Primary Header Adder block.
That block is directly connected to the Space Packet Parser block, which in turn prints the whole packet.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.
* The Space Packet Parser receives the packet and by choosing "No" in the Time Header option, it prints the packet showing just the Primary Header(every attribute) and the payload (as bytes).

## Space Packet Protocol and a flowgraph with a timestamp
In this [Space_Packet_with_TimeStamp](examples/Space_Packet_with_TimeStamp.grc), the payload is fed to the Message Strobe block triggers every 1 second the Random PDU Generator that generates random bytes (payload). That is feeded to the Space Packet Primary Header Adder block.
That block is directly connected to the Space Packet Parser block, which in turn prints the whole packet.

* The Space Packet Time Stamp Adder block adds a timestamp as a Secondary Header between the payload and the Primary Header. The various formats are describe din the Time Code Formats Blue Book (CCSDS 301.0-B-4). The existence of a PField and Time Format has to be chosen here and in the Space Packet Parser.

* The Time Format Parameters block is a global variable struct that defines the variables needed for each time format used in this flowgraph. The id of this block needs to be added both in the Space Packet Time Stamp Adder block and in the Space Packet Parser block.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.

* The Space Packet Parser receives the packet and by choosing "Yes" in the Time Header option, defining the time format and defining the use or not of the PField, it prints the packet showing the Primary Header(every attribute) the timestamp(every attribute) and the (optionally) PField and the payload (as bytes).

## Space Packet Protocol and a flowgraph with a Path ID demux
In this [Space_Packet_with_PathID_Demux](examples/Space_Packet_with_PathID_Demux.grc), the payload is fed to the Space Packet Primary Header Adder block.
That block is directly connected to the Path ID Demultiplexer. That block is connected to 3 Space Packet Parser blocks. It directs the packet to the appropriate block taking account the packet's APID. If the packet's APID is not defined in the vector of the Path ID Demultiplexer block, then it is redirected to the last output (discarded). The Space Packet Parser block, in turn, prints the whole packet.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.
* The Space Packet Parser receives the packet and by choosing "No" in the Time Header option, it prints the packet showing just the Primary Header(every attribute) and the payload (as bytes).
* The PAth ID Demultiplexer block redirects to one of the possible outputs. It redirects in the last output "Discard", if the APID doesn't match any given ID in the block.
## TC Packet and a simple flowgraph
In this [TC_Packet](examples/TC_Packet.grc), the payload is feeded to the Telecommand Primary Header Adder block. That block is directly connected to the Telecommand Parser block, which prints the whole packet.
* The Telecommand Primary Header Adder block adds the necessary bytes that are described in the Blue Book. The users can input the data per the needed configuration.
* The Telecommand Parser block prints out the data; every attribute of the Primary Header as well as the payload (as bytes).

## TM Packet and a simple flowgraph
In this [TM_Packet](examples/TM_Packet.grc), the payload is fed to the Telemetry Primary Header Adder block. That block is direclty connected to the Telemetry Parser block, which prints the whole packet.
* The Telemetry Primary Header Adder block adds the necessary bytes that are described in the Blue Book. The users can input the data per the needed configuration.
* The Telemetry Parser block prints out the data, once the segmentation is complete; every attribute of the Primary Header as well as the payload (as bytes). The user has to define the Coding and the size of the received packet.

## TM Packet and a flowgraph with OCF
In this [TM_Packet_with_OCF](examples/TM_Packet_with_OCF.grc), the payload is fed to the Telemetry Primary Header Adder block. That block is direclty connected to the Telemetry OCF Adder block, which is connected to the Telemetry Parser block, which, in turn, prints the whole packet.
* The Telemetry Primary Header Adder block adds the necessary bytes that are described in the Blue Book. The users can input the data per the needed configuration.
* The Telemetry Parser block prints out the data, once the segmentation is complete; every attribute of the Primary Header as well as the payload (as bytes). The user has to define the Coding and the size of the received packet.
* The Telemetry OCF Adder block adds an OCF trailer to the packet. The user has to define the OCF attributes.

## TM Packet and a flowgraph with Virtual Channel demux
In this [TM_Packet_with_VC_demux](examples/TM_Packet_with_VC_demux.grc), the payload is fed to the Telemetry Primary Header Adder block.
That block is directly connected to the Virtual Channel Demultiplexer. That block is connected to 3 Telemetry Parser blocks. It directs the packet to the appropriate block taking account the packet's Virtual Channel. If the packet's Virtual Channel is not defined in the vector of the Virtual Channel Demultiplexer block, then it is redirected to the last output (discarded). The Telemetry Parser block, in turn, prints the whole packet.

* The Telemetry Primary Header Adder block adds the necessary bytes that are described in the CCSDS 132.0-B-2, in the Primary Header section. The user can input the data per the needed configuration.
* The Telemetry Parser receives the packet and it prints it showing just the Primary Header(every attribute) and the payload (as bytes).
* The Virtual Channel Demultiplexer block redirects to one of the possible outputs. It redirects in the last output "Discard", if the VC doesn't match any given ID in the block.

## TM Packet containing a Space Packet
In this [TM_Packet_with_Space_Packet](examples/TM_Packet_with_Space_Packet.grc), the payload is fed to the Space Packet Primary Header Adder. That block is directly connected to the Telemetry Primary Header Adder (which takes care of the segmentation). Then the TM packet containing the Space Packet is printed in the Telemetry Parser, is sent to the Telemetry Packet Reconstruction block, to remove the TM headers and rebuild the Space Packets. When a Space Packet is complete, it is sent to the Space Packet Parser Block to be printed.

* The Space Packet Primary Header Adder block adds the necessary bytes that are described in the CCSDS 133.0-B-1, in the Primary Header section. The user can input the data per the needed configuration.
* The Space Packet Parser receives the packet and by choosing "No" in the Time Header option, it prints the packet showing just the Primary Header(every attribute) and the payload (as bytes).
* The Telemetry Primary Header Adder block adds the necessary bytes that are described in the Blue Book. The users can input the data per the needed configuration.
* The Telemetry Parser block prints out the data, once the segmentation is complete; every attribute of the Primary Header as well as the payload (as bytes). The user has to define the Coding and the size of the received packet.
* The Telemetry Packet Reconstruction block is in charge of removing the TM headers and reconstructing the Space Packet. Important Note: This block is specifically made for the Space Packet.

