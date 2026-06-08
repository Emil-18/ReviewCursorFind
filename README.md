# Review Cursor Find

* NVDA compatibility: 2024.4 and beyond.
* Download: [Stable version](https://github.com/Emil-18/reviewCursorFind/releases/download/v1.2/reviewCursorFind-1.2.nvda-addon).

This add-on adds find functionality for the review cursor, like find (NVDA+Control+f) does in browse mode. You can find any text accessible with the review cursor reading commands, (numbpad 6, numbpad 9, etc), before opening the find dialog, for example if the review cursor is in  a document and you open the dialog, the text within that document will be searched.
You can optionally use regular expressions. [A guide on what they are and how they can be used can be found here.](https://coderpad.io/blog/development/the-complete-guide-to-regular-expressions-regex/)

This add-on is specially useful in:

* terminal programs
* screen review
* situations where you want to search for text, but doesn't want to move the caret
* Situations where the program you are using doesn't implement its own search functionality


## A few notes on the regular expression support

* On NVDA 2026.2 or later, it will use the regex module. This allows you to use lookbehinds with strings that doesn't have fixed length.
	This also allow you to use fuzzy searching. On earlier NVDA versions, it will fall back to the re module
* Lookaheads and lookbehinds will always be based on the normal direction of the text, regardless if you are using next or previous search.
	For instance, if you have the string "asdf", an your regex is currantly between s and d, a lookahead will always point Towards d and f.

## Gestures

* NVDA+Control+Shift+g: Finds a text string from the review cursor position
* NVDA+g: Moves the review cursor to the next Occurrence of previously entered search text
* NVDA+Shift+g: Moves the review cursor to the previous Occurrence of previously entered search text

If you are in an editable control (a control where you can navigate its text with the arrow keys) you can use the normal find commands you are used to from browse mode.
NVDA+control+f for find, NVDA+f3 for find next, and NVDA+shift+f3 for find previous. These gestures behave in the same way as the global gestures, except they will move the navigator object to the object with focus before searching. This is done because it is assumed that you want to search within the object with focus.

## settings:

All the settings are in the find dialog for the review cursor

* Case sensitive check box: self explanatory
* Use Regular expressions when searching check box: If checked, the add-on will search by using regular expressions.
* Support all regular expressions. Turn off if you experience problems using the add-on, such as lag or the review cursor moving to the wrong text:
	When this is checked, you can reliably use regular expressions that uses criteria not based on the actual text that is searched after, such as lookaheads/lookbehinds, word bounderies, etc
	When unchecked, the add-on will return to its old behavior. This causes it to find the Desired string using regex, and feeding the result into NVDA's regular find algorithm. This Algorithm does not use regex.
	This setting should always be on, but you have the ability to turn it off just in case.
* Speak the found text, instead of the line where the review cursor ends up:
	When checked, only the text you searched after will be spoken. This can be useful if you want to skip over repeated text.
	For example, if you have a list that always starts with the same string, you can make a regular expression that captures everything between the instance of this string and the next one
* Move caret check box: If checked, the caret will be moved along with the review cursor when searching.

## Change log

### v1.2

* It is now possible to use all regular expressions
* When using NVDA 2026.2 or later, the regex module will be used, instead of re

### v1.1.1

* Added compatibility with NVDA 2026.1
* Moved the addon gestures to the text review category in the input gestures dialog

### v1.1

* Added the ability to use regular expressions when searching.
* Added the find gestures from browse mode in editable controls.
* Fixed a bug that sometimes caused NVDA to read the entire search text when using the read current character gesture after a search

### v1.0

* Initial release