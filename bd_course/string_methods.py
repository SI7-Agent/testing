class StringsMethods:
    @staticmethod
    def cut_from(string, prefix):
        return string[string.find(prefix) + len(prefix):]

    @staticmethod
    def cut_to(string, suffix='\0'):
        return string[:string.find(suffix)] if suffix != '\0' else string[:]
