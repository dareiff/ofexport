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

from fmt_template import Formatter

def escape (val):
    return val.replace('"','&quot;').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def format_note (lines):
    return '&#10;'.join([escape (line) for line in lines])
        
class PrintOpmlVisitor(Formatter):
    def __init__ (self, out, template):
        attrib_conversions = {
                      'id'             : lambda x: escape(x),
                      'name'           : lambda x: escape(x),
                      'link'           : lambda x: x,
                      'status'         : lambda x: x,
                      'flagged'        : lambda x: str(x) if x else None,
                      'context'        : lambda x: escape(''.join (x.name.split ())),
                      'project'        : lambda x: escape(''.join (x.name.split ())),
                      'date_to_start'  : lambda x: x.strftime(template.date_format),
                      'date_due'       : lambda x: x.strftime(template.date_format),
                      'date_completed' : lambda x: x.strftime(template.date_format),
                      'note'           : lambda x: format_note (x.get_note_lines ())
                      }
        Formatter.__init__(self, out, template, attrib_conversions = attrib_conversions)