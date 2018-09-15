"""
Code to analyze dictionary entries
"""

import os
import codecs
import re
from xml.etree import ElementTree
from constants import dheads, postags


def clean(text):
    if text is not None:
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", "", text)
        return text
    return text


class DictionaryDSL:
    """
    Extracts the dictionary from a list of files where entries are
    """
    def __init__(self, path):
        self.path = path
        self.filenames = os.listdir(path)
        self.entries = []
        self.chapters = []

    def get_first_letter_files(self):
        self.chapters = {}
        for filename in self.filenames:
            with codecs.open(os.path.join(self.path, filename), "r", encoding="utf8") as f:
                self.chapters[dheads[filename]] = FirstLetterFile(f.read())

    def find(self, word):
        if len(self.chapters) == 0:
            self.get_first_letter_files()
        if len(word) > 0:
            for entry in self.chapters[word[0].lower()].entries:
                # for value in entry:
                # print(repr(clean(entry.text)))
                if entry.word == word:
                    # print(entry.text)
                    return entry
                    # return entry.findtext(word)
        # for chapter in self.chapters:
        #     chapter.tree.find(word)


class FirstLetterFile:
    """
    Extract entries from a file
    """
    def __init__(self, text):
        self.text = text
        self.entries = []
        # self.extract_entries()
        # print(self.text[:100])
        self.tree = ElementTree.fromstring(self.text)

        for entry in self.tree:
            self.entries.append(Entry(entry))

    # def extract_entries(self):
    #     # print(self.text[:100])
    #
    #     # print(tree.text)
    #     return tree

        # entry_texts = []
        # i = -1
        # for line in self.text.split("\n"):
        #     if len(line) > 0:
        #         if line[0] == "\t":
        #             if len(entry_texts[i]) > 0:
        #                 entry_texts[i].append(line)
        #             else:
        #                 print("problem", line)
        #         else:
        #             entry_texts.append([line])
        #             i += 1
        # for entry_text in entry_texts:
        #     self.entries.append(Entry(entry_text))


class Entry:
    """
    Extract features of en entry
    \[m[0-9]*\] -> meaning
    \[i\] ->
    \[trn\] -> translation
    \[p\] -> grammatical features in abbreviations variable
    \[ref\]
    \[b\]
    """

    def __init__(self, entry_xml):
        self.word = entry_xml.get("word")
        # self.word = self.lines[0]
        # print(self.word)
        # self.description = repr("".join(entry_xml.itertext()))
        self.description = re.sub(r"\t", "", "".join(entry_xml.itertext()))
        self.pos = [postags[pos.text] for pos in entry_xml.iter("p")]
        self.declensions = []
        self.definition = []
        # self.description = entry_xml.text
        # if len(lines) > 1:
        #     self.description = self.lines[1:]
        #     for line in self.description:
        #         print(repr(line))
        #         line = line.replace("&", "")
        #         line_tree = ElementTree.fromstring(line)
        #         # print(line_tree)
        #         print(str(line_tree.text))
        #         # m = re.search(r"\[m", line)
        #         # if m is not None:
        #         #     print(line[m.end()])
        #
        #     # self.description = [line.strip() for line in self.description]
        #     # self.description = [re.sub(r"\[m[0-9]*\]", "", line) for line in self.description]
        #     # self.description = [re.sub(r"\[/m\]", "", line) for line in self.description]
        # else:
        #     self.description = []

    def extract_pos(self):
        pass


if __name__ == "__main__":
    d = DictionaryDSL("entries")
    # print("".join(d.find("sær").itertext()))
    print(d.find("sær").description)
    print(d.find("sær").pos)
    # print(d.find("sær"))
    # the_chapters = d.get_first_letter_files()
    # print(the_chapters[0].entries[0].lines)
    # print(the_chapters[0].entries[0].description)
