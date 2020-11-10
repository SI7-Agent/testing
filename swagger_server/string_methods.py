class StringsMethods:
    @staticmethod
    def cut_from(string, prefix):
        return string[string.find(prefix) + len(prefix):]

    @staticmethod
    def cut_to(string, suffix='\0'):
        return string[:string.find(suffix)] if suffix != '\0' else string[:]

    @staticmethod
    def user_by_url(album_url):
        return album_url.split('/')[-1].split('_')[0].replace('album', '')

    @staticmethod
    def album_by_url(album_url):
        return album_url.split('/')[-1].split('_')[1]
