import sublime, sublime_plugin
import re

class CloudTransformListCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for selectedRegion in self.view.sel():

			# Include my own strip HTML later
			# selectedContent = self.view.substr(selectedRegion)
			# strippedText = re.sub('<[^>]*>', '', selectedContent)
			# self.view.replace(edit, selectedRegion, strippedText)
			
			# Default strip HTML
			# self.view.run_command("strip_html")
			insertPoint = selectedRegion.begin()
			selectedContent = self.view.substr(selectedRegion)
			print(selectedContent)
			self.view.erase(edit, selectedRegion)
			selectedContent = selectedContent.split('\n')
			abbreviationList = [None]
			for i, listItem in enumerate(selectedContent):
				listItem = listItem.strip()
				if listItem[:1] in '- •'.split(): listItem = listItem[1:]
				listItem = listItem.strip()
				if len(listItem) == 0 : continue
				listItem = 'li{%s}%s' % (listItem, ('', '+')[i < len(selectedContent) - 1])
				abbreviationList.insert(i, listItem)
			abbreviationList.insert(0, 'ul.list>')
			abbreviationList = [x for x in abbreviationList if x is not None]
			abbreviationList = ''.join(abbreviationList)
			self.view.insert(edit, insertPoint, abbreviationList)
			insertPoint = insertPoint + len(abbreviationList)
			self.view.sel().add(insertPoint)
			self.view.run_command("run_emmet_action", {"action": "expand_abbreviation"})