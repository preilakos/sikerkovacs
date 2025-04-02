class Languages:
    VUE3_COMPOSITION = 1
    JAVASCRIPT = 2
    JAVA = 3
    PYTHON = 4
    HTML = 5
    JAVAFX_WITH_FXML = 6

    def getLanguageById(self, id):
        if id == self.VUE3_COMPOSITION:
            return "Vue3 Composition API"
        elif id == self.JAVASCRIPT:
            return "JavaScript"
        elif id == self.JAVA:
            return "Java"
        elif id == self.PYTHON:
            return "Python"
        elif id == self.HTML:
            return "HTML"
        elif id == self.JAVAFX_WITH_FXML:
            return "JavaFX with FXML"
        else:
            return "HTML"