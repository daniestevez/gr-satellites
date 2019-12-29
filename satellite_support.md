# Satellite support in gr-satellites v3

This table gives an overview of the status of the decoders in gr-satellites v3
compared to v2. Fully supported means that the v3 decoder has at least the same
functionality as the v2 decoder. Partially supported means that there is some
functionality available in v2 but not implemented yet in v3 (but the decoder
can decode packets). Unsupported means there is no decoder in v3 yet.

| Satellite 	    | Unsupported | Partially supported | Fully supported |
| ----------------- |:-----------:|:-------------------:|:---------------:|
| AAUSAT-4          |             |                     | x               |
| AISAT		    |		  | CSP CRC check miss.	| 		  |
| AISTECHSAT-2      |             | 	    	  	| Untested  	  |
| AISTECHSAT-3	    |		  |			| x   	  	  |
| AmGU-1	    | x		  |			| 		  |
| AO-40		    | 		  |			| x		  |
| AO-73		    |		  | Tlm decode miss.	| 		  |
| Astrocast 0.1	    |		  | 	       		| x		  |
| AT03 Pegasus	    |		  |			| x		  |
| ATHENOXAT-1	    | 		  |			| x		  |
| ATL-1		    |		  | Spectrum save miss.	| 		  |
| AU02 (UNSW-EC0)   |		  | 	     	  	| x		  |
| AU03 		    |		  |			| x		  |
| BEESAT-1	    | x		  |			| 		  |
| BEESAT-2	    | x		  |			| 		  |
| BEESAT-3	    | x		  |			| 		  |
| BEESAT-4	    | x		  |			| 		  |
| TECHNOSAT	    | x		  |			| 		  |
| BY70-1	    | 		  | Image dec. miss.	|		  |
| CA03 (ExAlta-1)   |		  | 	       		| x		  |
| CZ02 (VZLUSAT-1)  |		  |			| x		  |
| Delphini-1	    |		  |			| Untested	  |
| D-SAT		    |		  | Image dec. miss.	| 		  |
| D-STAR One	    | x		  | 	       		|		  |
| DUCHIFAT-3	    | 		  | AX.25 addr. check.	| 		  |
| EntrySat	    |		  | AX.25 addr. check.	| 		  |
| EQUiSat	    | x		  | 	  		|		  |
| ESEO		    | 		  |			| x		  |
| FACSAT-1	    |		  |			| x		  |
| FloripaSat-1	    |		  |			| x		  |
| FMN-1		    |		  |			| x		  |
| GALASSIA	    |		  |			| x		  |
| GOMX-1	    |		  | Tlm decode miss.	| 		  |
| GOMX-3	    |		  | 	       		| x		  |
| GR01 (DUTHSat)    |		  | AX.25 addr. check.	|  		  |
| IL01 (DUCHIFAT-2) |		  | AX.25 addr. check.	|		  |
| INNOSAT-2	    |		  | 	  		| x		  |
| ITASAT 1	    |		  |			| x		  |

