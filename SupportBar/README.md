# Lottery  

![Screenshot](/SupportBar/lib/samples/demo.png)
# Version 1.0
tested and working in Stable Build TouchDesigner 14360

---

SupportBarExt drives a global component for quickly assembling and visualizing 
financial support data from an arbitrary number of incoming sources. Designed
to be driven from Twitch triggers, it can be assembled via changing input DAT
or explicitly with python arguments via Addentry()

It was commissioned by [DandiDoesIt](https://www.patreon.com/DandiDoesIt), 
powering [The Dandi Line](https://www.twitch.tv/dandidoesit), a
Live Performance Video Game (LPVG) leveraging the 
Twitch platform as a vehicle for interactive theater. 

---
### Quickstart

SupportBar can be accessed remotely via global shortcut op.SUPPORTBAR or locally
via an inputDAT, expecting event_type, event_username and event_amount columns in the header  

SupportBar provides a variety of ways to access output data, including customPar 
refereneces, CHOP/DAT outputs of that par data, a chopbreakout by type, and the
complete support table itself.

---

### Public Methods  
  
**Addentry(user : str, type : str, units : float, value : float):**  
	specify a user, event type, and number of units to add a time stamped entry to the table. 
	if the type is specified in the user editable table_supportDict and assigned a value,
	that value will be used for incoming events of this type, and a subtotal will be
	calculated for that entry

**Cleartable():**
	remove all entrants from the table

**Edittable():**
	open floating popup to edit table entries

**Editsupportdict():**
	open floating popup to edit key/value schedule

**Exporttable():**
	timestamped method if "Export on Exit" parameter is enabled

**Exporttableas(fileName : str):**
	save table as method for exporting lotto entrants

**Importtable():**
	method for importing an externalized lotto table

---

### Dependencies

**op.TABLEPOPUP**   
	if the hive op.TABLEPOPUP tox is present in the session, it will be used as the 
	preferred DAT editor for above Edit* methods, otherwise it will default to standard openViewer()

---
#### TODO

* Changes based on feedback

#### Completed

* ~~samples and documentation~~
* ~~python methods for Addentry()~~
* ~~inputDAT method for Addentry()~~
* ~~implement table storage for entries~~
* ~~implement table import/export~~
  
#### Backlog 
* stylized charts'n'graphs




