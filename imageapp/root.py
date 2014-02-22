from quixote import get_response
from quixote.directory import Directory, export, subdir

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return "Hello, world"
