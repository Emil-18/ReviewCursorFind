# coding: utf-8
# Copyright 2025 Emil-18
# An add-on that allows you to find text with the review cursor
# Apparently, if you call addonHandler.initTranslation, the line (_) function can't access NVDA's own translations.
So asign it to a variable before calling initTranslation
translate = _
import addonHandler
addonHandler.initTranslation()
import api
import config
import controlTypes
import globalPluginHandler
import gui
import textInfos
import ui
import wx
from scriptHandler import script
from gui.settingsDialogs import SettingsDialog
from speech.speech import speakTextInfo, cancelSpeech

lastText = ""
def findManualy(reviewPosition, text, caseSensitive, reverse):
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
	
	oldReview = reviewPosition.copy()
	res = False
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
	api.setReviewPosition(reviewPosition)
	info = reviewPosition.copy()
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
	"moveCaret": "boolean(default=False)"
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
	def makeSettings(self, settingsSizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer = settingsSizer)
		label = translate("Type the text you wish to find")
		self.findText = helper.addLabeledControl(label, wx.TextCtrl,)
		self.findText.SetValue(lastText)
		label = translate("Case &sensitive")
		self.caseSensitive = helper.addItem(wx.CheckBox(self, label = label))
		self.caseSensitive.SetValue(config.conf["reviewCursorFind"]["caseSensitive"])
		# Translators: a label for a check box
		label = _("Move caret (if possible)")
		self.moveCaret = helper.addItem(wx.CheckBox(self, label = label))
		self.moveCaret.SetValue(config.conf["reviewCursorFind"]["moveCaret"])
	def postInit(self):
		self.findText.SetFocus()
	def onOk(self, *args, **kwargs):
		global lastText
		lastText = self.findText.GetValue()
		config.conf["reviewCursorFind"]["caseSensitive"] = self.caseSensitive.GetValue()
		config.conf["reviewCursorFind"]["moveCaret"] = self.moveCaret.GetValue()
		
		wx.CallLater(500, find, self.obj, self.reviewPosition, lastText, self.caseSensitive.GetValue(), self.reverse, self.moveCaret.GetValue())
		super(FindDialog, self).onOk(*args, **kwargs)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	
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