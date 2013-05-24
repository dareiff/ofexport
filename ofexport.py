'''
Copyright 2013 Paul Sidnell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import codecs
import getopt
import sys
from treemodel import traverse_list
from omnifocus import build_model, find_database
from datetime import date
from of_to_tp import PrintTaskpaperVisitor
from of_to_text import PrintTextVisitor
from of_to_md import PrintMarkdownVisitor
from of_to_opml import PrintOpmlVisitor
from of_to_html import PrintHtmlVisitor
from visitors import AnyNameFilterVisitor, AnyFlaggedFilterVisitor, FolderNameFilterVisitor, ProjectNameFilterVisitor, ProjectFlaggedFilterVisitor, FolderNameSortingVisitor, ProjectDueFilterVisitor, ProjectStartFilterVisitor, ContextNameFilterVisitor, TaskDueFilterVisitor, TaskNameFilterVisitor, TaskStartFilterVisitor, TaskCompletionFilterVisitor, ProjectCompletionFilterVisitor, TaskCompletionSortingVisitor, TaskFlaggedFilterVisitor, PruningFilterVisitor, FlatteningVisitor

VERSION = "1.0.4 (2013-04-15)" 
     
def print_structure (visitor, root_projects_and_folders, root_contexts, project_mode):
    if project_mode:
        traverse_list (visitor, root_projects_and_folders)
    else:
        traverse_list (visitor, root_contexts, project_mode=False)

class CustomPrintTaskpaperVisitor (PrintTaskpaperVisitor):
    def __init__(self, out, project_mode):
        PrintTaskpaperVisitor.__init__(self, out, project_mode)
    def tags (self, item):
        if item.date_completed != None:
            return item.date_completed.strftime(" @%Y-%m-%d-%a")
        else:
            return ""
        
def print_help ():
    print 'Version ' + VERSION
    print 
    print 'Usage:'
    print
    print 'ofexport [options...] -o file_name'
    print
    print
    print 'options:'
    print '  -h,-?,--help'
    print '  -C: context mode (as opposed to project mode)'
    print '  -P: project mode - the default (as opposed to context mode)'
    print '  -o file_name: the output file name, must end in a recognised suffix - see documentation'
    print '  --open: open the output file with the registered application (if one is installed)'
    print
    print 'filters:'
    
    print '  -i regexp: include anything matching regexp'
    print '  -e regexp: exclude anything matching regexp'
    
    print '  --Fi regexp: include anything flagged'
    print '  --Fe regexp: exclude anything flagged'
    
    print '  --pi regexp: include projects matching regexp'
    print '  --pe regexp: exclude projects matching regexp'
    
    print '  --pci regexp: include projects with completion matching regexp'
    print '  --pce regexp: exclude projects with completion matching regexp'
    
    print '  --pdi regexp: include projects with due matching regexp'
    print '  --pde regexp: exclude projects with due matching regexp'
    
    print '  --psi regexp: include projects with start matching regexp'
    print '  --pse regexp: exclude projects with start matching regexp'
    
    print '  --pfi: include flagged projects'
    print '  --pfe: exclude flagged projects'
    
    print '  --fi regexp: include folders matching regexp'
    print '  --fe regexp: exclude folders matching regexp'
    
    print '  --ti regexp: include tasks matching regexp'
    print '  --te regexp: exclude tasks matching regexp'
    
    print '  --ci regexp: include contexts matching regexp'
    print '  --ce regexp: exclude contexts matching regexp'
     
    print '  --tci regexp: include tasks with completion matching regexp'
    print '  --tce regexp: exclude tasks with completion matching regexp'
    
    print '  --tsi regexp: include tasks with start matching regexp'
    print '  --tse regexp: exclude tasks with start matching regexp'
    
    print '  --tdi regexp: include tasks with due matching regexp'
    print '  --tde regexp: exclude tasks with due matching regexp'
    
    print '  --tfi: include flagged tasks'
    print '  --tfe: exclude flagged tasks'
    
    print '  --tsc: sort tasks by completion'
    print '  --fsa: sort folders/projects alphabetically'
    
    print '  -F: flatten project/task structure'
    print '  --prune: prune empty projects or folders'

if __name__ == "__main__":
    
    today = date.today ()
    time_fmt='%Y-%m-%d'
    opn=False
    project_mode=True
    file_name = None
    paul = False
        
    opts, args = getopt.optlist, args = getopt.getopt(sys.argv[1:], 'hFCP?o:i:e:',
                                                      ['fi=','fe=',
                                                       'ci=','ce=',
                                                       'pi=','pe=',
                                                       'pci=','pce=',
                                                       'psi=','pse=',
                                                       'pdi=','pde=',
                                                       'pfi','pfe',
                                                       'ti=','te=',
                                                       'tci=','tce=',
                                                       'tsi=','tse=',
                                                       'tdi=','tde=',
                                                       'tfi','tfe',
                                                       'Fi','Fe',
                                                       'tsc',
                                                       'fsa',
                                                       'help',
                                                       'open',
                                                       'prune',
                                                       'paul'])
    for opt, arg in opts:
        if '--open' == opt:
            opn = True
        elif '--paul' == opt:
            paul = True
        elif '-o' == opt:
            file_name = arg;
            print 'Generating', file_name
        elif opt in ('-?', '-h', '--help'):
            print_help ()
            sys.exit()
    
    if file_name == None:
            print_help ()
            sys.exit()
    
    dot = file_name.index ('.')
    if dot == -1:
        print 'output file name must have suffix'
        sys.exit()
    
    fmt = file_name[dot+1:]
    
    root_projects_and_folders, root_contexts = build_model (find_database ())
    items = root_projects_and_folders
        
    for opt, arg in opts:
        
        # PROJECT MODE
        if '-P' == opt:
            project_mode = True
            items = root_contexts
        # CONTEXT MODE
        elif '-C' == opt:
            project_mode = False
            items = root_contexts
        
        # ANYTHING
        if '-i' == opt:
            visitor = AnyNameFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '-e' == opt:
            visitor = AnyNameFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--Fi' == opt:
            visitor = AnyFlaggedFilterVisitor (include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--Fe' == opt:
            visitor = AnyFlaggedFilterVisitor (include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        
        # FOLDER
        elif '--fi' == opt:
            visitor = FolderNameFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--fe' == opt:
            visitor = FolderNameFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        
        # PROJECT
        elif '--pi' == opt:
            visitor = ProjectNameFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pe' == opt:
            visitor = ProjectNameFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--psi' == opt:
            visitor = ProjectStartFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pse' == opt:
            visitor = ProjectStartFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pdi' == opt:
            visitor = ProjectDueFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--psc' == opt:
            visitor = ProjectDueFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pci' == opt:
            visitor = ProjectCompletionFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pce' == opt:
            visitor = ProjectCompletionFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pfi' == opt:
            visitor = ProjectFlaggedFilterVisitor (include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--pfe' == opt:
            visitor = ProjectFlaggedFilterVisitor (include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--fsa' == opt:
            visitor = FolderNameSortingVisitor ()
            print opt + '\t= ' + str (visitor)
            root_projects_and_folders.sort(key=lambda item:item.name) # Have to sort the top level list too
            traverse_list (visitor, items, project_mode=project_mode)
            
        # CONTEXT
        elif '--ci' == opt:
            visitor = ContextNameFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--ce' == opt:
            visitor = ContextNameFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        
        # TASK
        elif '--ti' == opt:
            visitor = TaskNameFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--te' == opt:
            visitor = TaskNameFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tci' == opt:
            visitor = TaskCompletionFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tce' == opt:
            visitor = TaskCompletionFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tsi' == opt:
            visitor = TaskStartFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tse' == opt:
            visitor = TaskStartFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tdi' == opt:
            visitor = TaskDueFilterVisitor (arg, include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tde' == opt:
            visitor = TaskDueFilterVisitor (arg, include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tfi' == opt:
            visitor = TaskFlaggedFilterVisitor (include=True)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tfe' == opt:
            visitor = TaskFlaggedFilterVisitor (include=False)
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '--tsc' == opt:
            visitor = TaskCompletionSortingVisitor ()
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        
        # MISC
        elif '--prune' == opt:
            visitor = PruningFilterVisitor ()
            print opt + '\t= ' + str (visitor)
            traverse_list (visitor, items, project_mode=project_mode)
        elif '-F' == opt:
            visitor = FlatteningVisitor ()
            print opt + '\t= ' + str (visitor)
            if project_mode:
                traverse_list (visitor, root_projects_and_folders, project_mode=project_mode)
                root_projects_and_folders = visitor.projects # Really?
                items = visitor.projects
            else:
                traverse_list (visitor, root_contexts, project_mode=project_mode)
                root_contexts = visitor.contexts # Really?
                items = visitor.contexts

    file_name_base = os.environ['HOME']+'/Desktop/'
    date_str = today.strftime (time_fmt)
    
    if fmt == 'txt' or fmt == 'text':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintTextVisitor (out), root_projects_and_folders, root_contexts, project_mode)
        
    # MARKDOWN
    elif fmt == 'md' or fmt == 'markdown':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, root_contexts, project_mode)
        
    # FOLDING TEXT
    elif fmt == 'ft' or fmt == 'foldingtext':
        out=codecs.open(file_name, 'w', 'utf-8')
        
        print_structure (PrintMarkdownVisitor (out), root_projects_and_folders, root_contexts, project_mode)
                
    # TASKPAPER            
    elif fmt == 'tp' or fmt == 'taskpaper':
        out=codecs.open(file_name, 'w', 'utf-8')
        visitor = None
        if paul:
            visitor = CustomPrintTaskpaperVisitor (out, project_mode)
        else:
            visitor = PrintTaskpaperVisitor (out, project_mode)
        print_structure (visitor, root_projects_and_folders, root_contexts, project_mode)
    
    # OPML
    elif fmt == 'opml':
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        print >>out, '<opml version="1.0">'
        print >>out, '  <head>'
        print >>out, '    <title>OmniFocus</title>'
        print >>out, '  </head>'
        print >>out, '  <body>'
        
        print_structure (PrintOpmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
        
        print >>out, '  </body>'
        print >>out, '</opml>'
    
    # Let's try JSON!
    
    # elif fmt =='json':
    #     out=codexs.open(file_name, 'w', 'utf-8')
    #     print >>out, ''
        
        
    # Statusboard HTML
    elif fmt =='html':
        out=codecs.open(file_name, 'w', 'utf-8')
        print >>out, '  <table id="projects">'
        
        print_structure (PrintHtmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
        
        print >>out, '  </table>'
        
    # HTML
    # elif fmt == 'html' or fmt == 'htm':
    #     out=codecs.open(file_name, 'w', 'utf-8')
    #     print >>out, '<html>'
    #     print >>out, '  <head>'
    #     print >>out, '    <title>OmniFocus</title>'
    #     print >>out, '  </head>'
    #     print >>out, '  <body>'
    #     
    #     print_structure (PrintHtmlVisitor (out, depth=1), root_projects_and_folders, root_contexts, project_mode)
    #     
    #     print >>out, '  </body>'
    #     print >>out, '<html>'
    else:
        raise Exception ('unknown format ' + fmt)
    
    # Close the file and open it
    out.close()
    
    if opn:
        os.system("open '" + file_name + "'")
