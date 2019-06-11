from pathlib import Path
from os.path import split
from denite.base.filter import Base
from denite.util import path2project, path2dir, relpath

class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'converter/prioritize_basename'
        self.description = 'convert to prioritize action path base name.'
        self.vars = {
            'root_markers': ['package.json', 'composer.json']
        }

    def filter(self, context):
        root_dirs = []
        for candidate in context['candidates']:
            if 'action__path' in candidate:
                candidate['abbr'] = self.get_abbr(candidate, root_dirs)
        return context['candidates']

    def get_abbr(self, candidate, root_dirs):
        root_dir = self.get_root_dir(candidate, root_dirs)
        path, basename = split(candidate['action__path'])
        path = Path(path).relative_to(root_dir)
        path = path if path != '.' else ''
        return "{} - {}".format(basename, path)

    def get_root_dir(self, candidate, root_dirs):
        candidate_dir = path2dir(candidate['action__path'])

        for root_dir in root_dirs:
            if candidate_dir.startswith(root_dir):
                return root_dir

        root_dir = path2project(self.vim, candidate_dir, ','.join(self.vars['root_markers']))
        if root_dir == candidate_dir:
            return '/'

        root_dir = str(Path(root_dir).parent)
        root_dirs.append(root_dir)
        return root_dir

