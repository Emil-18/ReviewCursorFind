# coding: utf-8
# Copyright 2025-2026 Emil-18
# An add-on that allows you to find text with the review cursor
# Apparently, if you call addonHandler.initTranslation, the line (_) function can't access NVDA's own translations.
#So asign it to a variable before calling initTranslation
translate = _
import addonHandler
addonHandler.initTranslation()
import api
import config
import controlTypes
import globalCommands
import globalPluginHandler
import gui
import textInfos
import ui
import wx
from NVDAObjects import NVDAObject, behaviors
from scriptHandler import script
from gui.settingsDialogs import SettingsDialog
from speech.speech import speakTextInfo, cancelSpeech
# NVDA 2026.2 and onwerds has the regex module built in.
# Regex adds support for lookbehinds with none fixed string length, as well as fuzzy searching
# as some functions in re and regex has the same name as some python builtin functions:
try:
	import regex as re
except:
	import re
def navigatorToFocus():
	nav = api.getNavigatorObject()
	focus = api.getFocusObject()
	if nav != focus:
		api.setNavigatorObject(focus)
class Find(NVDAObject):
	scriptCategory = globalCommands.SCRCAT_TEXTREVIEW
	@script(
		# Translators: the description for a script
		description = _("Finds a text string from the review cursor position. Moves the navigator object to the object with focus first"),
		gesture = "kb:nvda+control+f"
	)
	def script_find(self, gesture, reverse = False):
		navigatorToFocus()
		reviewPosition = api.getReviewPosition().copy()
		gui.mainFrame.popupSettingsDialog(FindDialog, reviewPosition = reviewPosition, reverse = reverse)
	@script(
		# Translators: the description for a script
		description = _("Moves the review cursor to the next Occurrence of previously entered search text. Moves the navigator object to the object with focus first"),
		gesture = "kb:NVDA+f3"
	)
	def script_findNext(self, gesture):
		navigatorToFocus()
		if lastText:
			find(None, api.getReviewPosition(), lastText, config.conf["reviewCursorFind"]["caseSensitive"], False, config.conf["reviewCursorFind"]["moveCaret"])
			return
		self.script_find(gesture)
	@script(
		# Translators: the description for a script
		description = _("Moves the review cursor to the previous Occurrence of previously entered search text. Moves the navigator object to the object with focus first"),
		gesture = "kb:NVDA+shift+F3"
	)
	def script_findPrevious(self, gesture):
		navigatorToFocus()
		if lastText:
			find(None, api.getReviewPosition(), lastText, config.conf["reviewCursorFind"]["caseSensitive"], True, config.conf["reviewCursorFind"]["moveCaret"])
			return
		self.script_find(gesture, reverse = True)

lastText = ""
def findWithRegexAndMove(reviewPosition, text, caseSensitive, reverse, shouldReportFoundText = False):
	expandableReviewPosition = reviewPosition.copy()
	if reverse:
		tempReviewPosition = reviewPosition.copy()
		res = tempReviewPosition.move(textInfos.UNIT_CHARACTER, -1)
		if not res:
			return(False)
		expandableReviewPosition.move(textInfos.UNIT_STORY, -1, endPoint = "start")
		found = [*re.finditer(text, expandableReviewPosition.text, (re.IGNORECASE if not caseSensitive else 0) + re.MULTILINE)]
		if not found:
			return(False)
		found = found[-1]
		movableReviewPosition = expandableReviewPosition.copy()
		try:
			movableReviewPosition = movableReviewPosition.moveToCodepointOffset(found.start())
		except:
			return(False)
		reviewPosition.setEndPoint(movableReviewPosition, "startToStart")
		
	else:
		res = expandableReviewPosition.move(textInfos.UNIT_CHARACTER, 1)
		if not res:
			return(False)
		expandableReviewPosition.move(textInfos.UNIT_STORY, 1, endPoint = "end")
		found = re.search(text, expandableReviewPosition.text, (re.IGNORECASE if not caseSensitive else 0) + re.MULTILINE)
		if not found:
			return(False)
		movableReviewPosition = expandableReviewPosition.copy()
		try:
			movableReviewPosition = movableReviewPosition.moveToCodepointOffset(found.start())
		except:
			return(False)
		reviewPosition.setEndPoint(movableReviewPosition, "startToStart")
	endInfo = None
	if shouldReportFoundText:
		endInfo = expandableReviewPosition.moveToCodepointOffset(found.end())
	return((movableReviewPosition, endInfo))
def findUsingRegex(reviewPosition, text, caseSensitive, reverse):
	info = reviewPosition.copy()
	if reverse:
		res = info.move(textInfos.UNIT_CHARACTER, -1)
		if not res:
			return
		expandableInfo = info.copy()
		expandableInfo.move(textInfos.UNIT_STORY, -1, endPoint = "start")
		found = list(re.finditer(text, expandableInfo.text, (re.IGNORECASE if not caseSensitive else 0)+re.MULTILINE))
		if not found:
			return
		return(found[-1].group())
	res = info.move(textInfos.UNIT_CHARACTER, 1)
	if not res:
		return
	info.move(textInfos.UNIT_STORY, 1, endPoint = "end")
	found = re.search(text, info.text, (re.IGNORECASE if not caseSensitive else 0
)+re.MULTILINE)
	if not found:
		return
	return(found.group())
def findManualy(reviewPosition, text, caseSensitive, reverse):
	if not text:
		return(False)
	info = reviewPosition.copy()
	if not caseSensitive:
		text = text.lower()
	if reverse:
		text = text[::-1]
		res = info.move(textInfos.UNIT_CHARACTER, -1)
		expandableInfo = info.copy()
		expandableInfo.move(textInfos.UNIT_STORY, -1, endPoint = "start")
		searchableText = expandableInfo.text[::-1]
	else:
		res = info.move(textInfos.UNIT_CHARACTER, 1)
		expandableInfo = info.copy()
		expandableInfo.move(textInfos.UNIT_STORY, 1, endPoint = "end")
		searchableText = expandableInfo.text
	if not caseSensitive:
		searchableText = searchableText.lower()
	index = searchableText.find(text)
	if index <0:
		return(False)
	if reverse:
		res = reviewPosition.move(textInfos.UNIT_CHARACTER, -index-len(text)-1)
	else:
		res = reviewPosition.move(textInfos.UNIT_CHARACTER, index+1)
	if not res:
		return(False)
	return(True)
# TextInfo.obj is stored as a weak reference for some reason, so that if TextInfo.obj is the only variable pointing to obj, obj will be deleted.
# So store obj as its own variable.
def find(obj, reviewPosition, text, caseSensitive, reverse, moveCaret):
	wasFoundWithRegex = False
	shouldReportFoundText = config.conf["reviewCursorFind"]["shouldReportFoundText"]
	oldReview = reviewPosition.copy()
	res = False
	if config.conf["reviewCursorFind"]["regex"]:
		if config.conf["reviewCursorFind"]["trueRegex"]:
			res = findWithRegexAndMove(reviewPosition, text, caseSensitive, reverse, shouldReportFoundText = shouldReportFoundText)
			wasFoundWithRegex = True
		else:
			text = findUsingRegex(reviewPosition, text, caseSensitive, reverse)
			caseSensitive = True
	if not wasFoundWithRegex:
		try:
			res = reviewPosition.find(text, caseSensitive = caseSensitive, reverse = reverse)
		except:
			pass
		if not res:
			res = findManualy(reviewPosition, text, caseSensitive, reverse)
	if not res:
		# Translators: Message when no text is found
		message = _("Not found")
		cancelSpeech()
		ui.message(message)
		return
	if moveCaret:
		try:
			reviewPosition.updateCaret()
		except:
			pass
	# In some implementations, TextInfo.find expands the textInfo, so collapse it just in case
	reviewPosition.collapse()
	api.setReviewPosition(reviewPosition)
	info = reviewPosition.copy()
	if shouldReportFoundText and isinstance(res, tuple):
		info.setEndPoint(res[1], "endToStart")
	else:
		lineInfo = info.copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		oldReview.expand(textInfos.UNIT_LINE)
		if lineInfo == oldReview:
			info.move(textInfos.UNIT_LINE, 1, endPoint = "end")
		else:
			info.expand(textInfos.UNIT_LINE)
	cancelSpeech()
	speakTextInfo(info, reason = controlTypes.OutputReason.CARET)
spec = {
	"caseSensitive": "boolean(default=False)",
	"moveCaret": "boolean(default=False)",
	"regex": "boolean(default=False)",
	"trueRegex": "boolean(default=True)",
	"shouldReportFoundText": "boolean(default=False)"
}
config.conf.spec["reviewCursorFind"] = spec
class FindDialog(SettingsDialog):
	title = translate("Find")
	def __init__(self, *args, reviewPosition = None, text = "", reverse = False, **kwargs):
		super(FindDialog, self).__init__(*args, **kwargs)
		if not reviewPosition:
			reviewPosition = api.getReviewPosition()
		self.reviewPosition = reviewPosition
		self.obj = reviewPosition.obj
		self.text = text
		self.reverse = reverse
	def onRegexChange(self, evt):
		selection = evt.GetSelection()
		self.trueRegex.Enable(selection)
		self.shouldReportFoundText.Enable(selection and self.trueRegex.GetValue())
	def onTrueRegexChange(self, evt):
		selection = evt.GetSelection()
		self.shouldReportFoundText.Enable(selection and self.regex.GetValue())
	
	def makeSettings(self, settingsSizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer = settingsSizer)
		label = translate("Type the text you wish to find")
		self.findText = helper.addLabeledControl(label, wx.TextCtrl,)
		self.findText.SetValue(lastText)
		label = translate("Case &sensitive")
		self.caseSensitive = helper.addItem(wx.CheckBox(self, label = label))
		self.caseSensitive.SetValue(config.conf["reviewCursorFind"]["caseSensitive"])
		# Translators: The label for a check box
		label = _("Use Regular expressions when searching")
		self.regex = helper.addItem(wx.CheckBox(self, label = label))
		self.regex.SetValue(config.conf["reviewCursorFind"]["regex"])
		self.regex.Bind(wx.EVT_CHECKBOX, self.onRegexChange)
		# Translators: A label for a check box
		label = _("Support all regular expressions. Turn off if you experience problems using the add-on, such as lag or the review cursor moving to the wrong text")
		self.trueRegex = helper.addItem(wx.CheckBox(self, label = label))
		self.trueRegex.SetValue(config.conf["reviewCursorFind"]["trueRegex"])
		self.trueRegex.Enable(config.conf["reviewCursorFind"]["regex"])
		self.trueRegex.Bind(wx.EVT_CHECKBOX, self.onTrueRegexChange)
		# Translators: A label for a check box
		label = _("Speak the found text, instead of the line where the review cursor ends up")
		self.shouldReportFoundText = helper.addItem(wx.CheckBox(self, label = label))
		self.shouldReportFoundText.SetValue(config.conf["reviewCursorFind"]["shouldReportFoundText"])
		self.shouldReportFoundText.Enable(self.regex.GetValue() and self.trueRegex.GetValue())
		# Translators: a label for a check box
		label = _("Move caret (if possible)")
		self.moveCaret = helper.addItem(wx.CheckBox(self, label = label))
		self.moveCaret.SetValue(config.conf["reviewCursorFind"]["moveCaret"])
	def postInit(self):
		self.findText.SetFocus()
	def onOk(self, *args, **kwargs):
		if self.regex.GetValue():
			try:
				re.compile(self.findText.GetValue())
			except re.error:
				# Translators: The message reported when the regular expression entered is invalid
				message = _("Invalid regular expression")
				ui.message(message)
				return
		global lastText
		lastText = self.findText.GetValue()
		config.conf["reviewCursorFind"]["caseSensitive"] = self.caseSensitive.GetValue()
		config.conf["reviewCursorFind"]["regex"] = self.regex.GetValue()
		config.conf["reviewCursorFind"]["trueRegex"] = self.trueRegex.GetValue()
		config.conf["reviewCursorFind"]["shouldReportFoundText"] = self.shouldReportFoundText.GetValue()
		config.conf["reviewCursorFind"]["moveCaret"] = self.moveCaret.GetValue()
		
		wx.CallLater(500, find, self.obj, self.reviewPosition, lastText, self.caseSensitive.GetValue(), self.reverse, self.moveCaret.GetValue())
		super(FindDialog, self).onOk(*args, **kwargs)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = globalCommands.SCRCAT_TEXTREVIEW
	@script(
		# Translators: the description for a script
		description = _("Finds a text string from the review cursor position"),
		gesture = "kb:nvda+control+shift+g"
	)
	def script_find(self, gesture, reverse = False):
		reviewPosition = api.getReviewPosition().copy()
		gui.mainFrame.popupSettingsDialog(FindDialog, reviewPosition = reviewPosition, reverse = reverse)
	@script(
		# Translators: the description for a script
		description = _("Moves the review cursor to the next Occurrence of previously entered search text"),
		gesture = "kb:NVDA+g"
	)
	def script_findNext(self, gesture):
		if lastText:
			find(None, api.getReviewPosition(), lastText, config.conf["reviewCursorFind"]["caseSensitive"], False, config.conf["reviewCursorFind"]["moveCaret"])
			return
		self.script_find(gesture)
	@script(
		# Translators: the description for a script
		description = _("Moves the review cursor to the previous Occurrence of previously entered search text"),
		gesture = "kb:NVDA+shift+g"
	)
	def script_findPrevious(self, gesture):
		if lastText:
			find(None, api.getReviewPosition(), lastText, config.conf["reviewCursorFind"]["caseSensitive"], True, config.conf["reviewCursorFind"]["moveCaret"])
			return
		self.script_find(gesture, reverse = True)
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		for i in clsList:
			if issubclass(i, behaviors.EditableTextBase) or isinstance(obj, behaviors.EditableTextBase):
				clsList.insert(0, Find)
				break