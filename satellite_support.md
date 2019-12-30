# Satellite support in gr-satellites v3

This table gives an overview of the status of the decoders in gr-satellites v3
compared to v2. Fully supported means that the v3 decoder has at least the same
functionality as the v2 decoder. Partially supported means that there is some
functionality available in v2 but not implemented yet in v3 (but the decoder
can decode packets). Unsupported means there is no decoder in v3 yet.

| Satellite 	    | Unsupported | Partially supported | Fully supported |
| ----------------- |:-----------:|:-------------------:|:---------------:|
| 1KUNS-PF	    |		  | Image dec. miss.	|		  |
| 3CAT-1	    |		  | 	       		| x		  |
| 3CAT-2	    |		  | Tlm decode miss.	| 		  |
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
| JY1-Sat	    |		  | Tlm decode miss.	| 		  |
| K2SAT		    |		  | 	       		| In examples/	  |
| KR01 (LINK)	    |		  | AX.25 addr. check.	|    		  |
| KS-1Q		    |		  | CSP CRC check miss.	| 		  |
| LilacSat-1	    |		  | Image dec. miss.	|		  |
| LilacSat-2	    |		  | Subaudio dec. miss.	|		  |
| Lucky-7	    |		  | 	     	  	| x		  |
| LUME-1	    |		  |			| Untested	  |
| Luojia-1	    |		  |			| x		  |
| MYSAT 1	    |		  | AX.25 addr. check.	| 		  |
| Nayif-1	    |		  | Tlm decode miss.	|		  |
| ÑuSat 1, 2	    |		  | 	       		| x		  |
| OPS-SAT  	    |		  |			| x		  |
| PicSat	    |		  | AX.25 addr. check.	| 		  |
| PW-Sat2	    |		  | AX.25 addr. check.	|		  |
| QO-100	    |		  | 	  		| x		  |
| Reaktor Hello W   |		  |			| x		  |
| Shaonian Xing	    |		  | AX.25 addr. check.	| 		  |
| SMOG-P   	    |		  | Spectrum save miss.	|		  |
| S-NET		    |		  | classifier miss.	|		  |
| Sokrat	    | x		  | 	       		|		  |
| SpooQy-1	    | 		  |			| x		  |
| Suomi 100	    |		  |			| x		  |
| Światowid	    |		  | Image dec. miss.	| 		  |
| TANUSHA-3	    | x		  | 	       		|		  |
| Taurus-1	    | 		  |			| Untested	  |
| TW-1A, B, C	    |		  |			| x		  |
| TY-2, TY 4-01,... |		  |			| x		  |
| UA01	   	    | x		  |			| 		  |
| UKube-1	    | 		  | Tlm decode miss.	|		  |
| Zhou Enlai	    |		  | AX.25 addr. check.	|		  |
