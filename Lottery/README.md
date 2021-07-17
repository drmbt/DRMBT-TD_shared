# Lottery  

---

![Screenshot](/ValueLadder/lib/samples/demo.gif) ![Screenshot](/ValueLadder/lib/samples/icon.jpg)

# Version 1.0
tested and working in Stable Build TouchDesigner 14360

Lottery is a global component for quickly adding entrants to a
lottery pool and selecting a random winner by rotating through the entrants wheel of fortune style. 

It was commissioned by [DandiDoesIt](https://www.patreon.com/DandiDoesIt), powering [The Dandi Line](https://www.twitch.tv/dandidoesi), a Live Performance Video Game (LPVG) leveraging the
Twitch platform as a vehicle for interactive theater. 

---
### Quickstart

Add entrants to the lottery pool with op.LOTTERY.Addentrent('username') or
built by adding an Entrant Name and pulsing customPar['Addentrant']

Select a winner with op.LOTTERY.Selectwinner()) or by defining
a Selectlength and pulsing customPar['Selectwinner']

---

### Public Methods

**Addentrant(user : str):**  
	specify a user and add a time stamped entry to the table. 
	if no user is specified, add entry from ownerComp customPar['Entrantname']  

**Selectwinner(length : float):**
	trigger for winner selection process. if no length is specified,
	get length from ownerComp customPar['Selectionlength']

**Cleartable():**
	remove all entrants from the table

**Exporttable():**
	timestamped method if "Export on Exit" parameter is enabled

**Exporttableas(fileName : str):**
	save table as method for exporting lotto entrants
**Importtable():**
	method for importing an externalized lotto table

---

### Dependencies

**click.wav** 
an audio sample for sonifying item change. Can be changed via "Audio"
page 'File' parameter

---
#### TODO

* Changes based on feedback.

#### Completed
* ~~samples and documentation~~
* ~~implement table storage for entrant pool~~
* ~~implement table import/export~~
* ~~create trigger based random selection network~~
* ~~create audio sample and sonic feedback treatment~~
  
#### Backlog 
* animation treatments for selection rotation




