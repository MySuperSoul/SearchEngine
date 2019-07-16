class ContentProcessHandler():
    def __init__(self):
        self.change = False

    def GetNewContent(self, content):
        self.change = False
        new_content = str(content)
        position = new_content.find('\n\n')

        # process the title with digit
        if position != -1 and new_content[:position].isdigit():
            new_content = new_content[position + 2:]
            self.change = True

        position = new_content.find('Your Answer')
        if position != -1:
            new_content = new_content[:position]
            self.change = True

        return (self.change, new_content)

