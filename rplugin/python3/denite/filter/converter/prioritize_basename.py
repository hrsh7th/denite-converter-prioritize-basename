from pathlib import Path
from os.path import split, commonprefix
from denite.base.filter import Base
from denite.util import path2project

class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'converter/prioritize_basename'
        self.description = 'convert to prioritize action path base name.'
        self.vars = {
            'root_markers': ['package.json', 'composer.json']
        }

    def filter(self, context):
        root_dir = self.root_dir(context)
        for candidate in context['candidates']:
            if 'action__path' in candidate:
                words = split(candidate['action__path'])
                file = words[1]
                path = str(Path(words[0]).relative_to(root_dir))
                path = './' + path if path is not '.' else './'
                candidate['abbr'] = "{} - {}".format(file, path)
        return context['candidates']

    def root_dir(self, context):
        prefix = commonprefix([ x['action__path'] for x in context['candidates'] if x['action__path'] ])

        # detect project root.
        sample = context['candidates'][0]
        if 'action__path' in sample:
            project_root = path2project(self.vim, sample['action__path'], ','.join(self.vars['root_markers']))
            if len(project_root) < len(prefix):
                return project_root

        return prefix

