# Review Cursor Find

* NVDA compatibility: 2024.4 and beyond.
* Download: [Stable version](https://github.com/Emil-18/reviewCursorFind/releases/download/v1.1/reviewCursorFind-1.1.nvda-addon).

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

If you are in an editable control (a control where you can navigate its text with the arrow keys) you can use the normal find commands you are used to from browse mode.
NVDA+control+f for find, NVDA+f3 for find next, and NVDA+shift+f3 for find previous. These gestures behave in the same way as the global gestures, except they will move the navigator object to the object with focus before searching. This is done because it is assumed that you want to search within the object with focus.

## settings:

All the settings are in the find dialog for the review cursor

* Case sensitive check box: self explanatory.
* Use Regular expressions when searching check box: If checked, the add-on will search by using regular expressions. [A guide on what they are and how they ccan be used can be found here.](https://coderpad.io/blog/development/the-complete-guide-to-regular-expressions-regex/)
* Move caret check box: If checked, the caret will be moved along with the review cursor when searching.

## Change log

### v1.1

* Added the abillity to use regular expressions when searching.
* Added the find gestures from browse mode in editable controls.
* Fixed a bug that sometimes caused NVDA to read the entire search text when using the read current character gesture after a search

### v1.0

* Initial release