# Review Cursor Find

* NVDA compatibility: 2024.4 and beyond.
* Download: [Stable version](https://github.com/Emil-18/reviewCursorFind/releases/download/v1.0/reviewCursorFind-1.0.nvda-addon).

This add-on adds find functionality for the review cursor, like find (NVDA+Control+f) does in browse mode. You can find any text accessible with the review cursor reading commands, (numbpad 6, numbpad 9, etc), before opening the find dialog, for example if the review cursor is in  a document and you open the dialog, the text within that document will be searched

This add-on is specially useful in:

* terminal programs
* screen review
* situations where you want to search for text, but doesn't want to move the caret
* Situations where the program you are using doesn't implement its own search functionality

## Gestures

* NVDA+Control+Shift+g: Finds a text string from the review cursor position
* NVDA+g: Moves the review cursor to the next Occurrence of previously entered search text
* NVDA+Shift+g: Moves the review cursor to the previous Occurrence of previously entered search text

## settings:

All the settings are in the find dialog for the review cursor

* Case sensitive check box: self explanatory.
* Move caret check box: If checked, the caret will be moved along with the review cursor when searching.

## Change log

### v1.0

* Initial release