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

from treemodel import traverse_list, Visitor
from omnifocus import build_model, find_database
import os
import codecs

class PrintHtmlVisitor(Visitor):
    def __init__ (self, out, depth=2, indent=4):
        self.depth = depth
        self.out = out
        self.indent = indent
    def begin_folder (self, folder):
        self.print_link ('folder', folder)
        self.depth+=1
    def end_folder (self, folder):
        self.depth-=1
    def begin_project (self, project):
        self.print_link ('task', project)
        self.depth+=1
    def end_project (self, project):
        self.depth-=1
    def begin_task (self, task):
        self.print_link ('task', task)
        self.depth+=1
    def end_task (self, task):
        self.depth-=1
    def begin_context (self, context):
        self.print_link ('context', context)
        self.depth+=1
    def end_context (self, context):
        self.depth-=1
    def print_link (self, link_type, item):
<<<<<<< HEAD
        ident = item.ofattribs['persistentIdentifier']
        print >>self.out, '<tr><td class="projectIcon"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" width="30px" height="30px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><g id="Your_Icon"><path fill="none" stroke="#B473FC" stroke-width="4" stroke-miterlimit="10" d="M90,20L30,80L10,60"/></g></svg></td><td class="taskName">' + self.escape(item.name) + '</td></tr>'
        # print >>self.out, self.spaces() + item.type + ': <a href="omnifocus:///' + link_type + '/' + ident + '">' + self.escape(item.name) + '</a><br>'
=======
        # This happens on "No Context" - we fabricate it and it has no persistentIdentifier
        if 'persistentIdentifier' in item.ofattribs:
            ident = item.ofattribs['persistentIdentifier']
            print >>self.out, self.spaces() + item.type + ': <a href="omnifocus:///' + link_type + '/' + ident + '">' + self.escape(item.name) + '</a><br>'
>>>>>>> 683f3a37e3c42604471c2937ef1783cb5a1696c2
    def spaces (self):
        return '&nbsp' * self.depth * self.indent
    def escape (self, val):
        return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

if __name__ == "__main__":
    root_projects_and_folders, root_contexts = build_model (find_database ())
    
    file_name=os.environ['HOME'] + '/Desktop/OF.html'
    
    out=codecs.open(file_name, 'w', 'utf-8')
    print >>out, '<head><title>Omnifocus</title></head><body>'
    traverse_list (PrintHtmlVisitor (out), root_projects_and_folders)
    print >>out, '<hr/>'
    
    traverse_list (PrintHtmlVisitor (out), root_contexts, project_mode=False)
    print >>out, '<hr/>'
    print >>out, '</body>'
    out.close()
    
    os.system("open '" + file_name + "'")