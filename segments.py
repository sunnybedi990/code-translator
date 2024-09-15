import re
from typing import List, Tuple, Dict


language_patterns = {
        "python": {
         "class": [re.compile(r'class\s+(\w+)')],  # List of patterns to match class definitions in Python
        "method": [re.compile(r'def\s+(\w+)\(')],  # List of patterns to match method definitions in Python
        "variable": [re.compile(r'^(\w+)\s*=')],  # List of patterns to match global variable declarations in Python


        },
        "java": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in Java
            "method": r'(public|private|protected)?\s+\w+\s+(\w+)\(',  # Pattern to match method definitions in Java
            "variable": r'(\w+)\s+\w+\s*;',  # Pattern to match variable declarations in Java
        },
        "csharp": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in C#
            "method": r'(public|private|protected)?\s+\w+\s+(\w+)\(',  # Pattern to match method definitions in C#
            "variable": r'(\w+)\s+\w+\s*;',  # Pattern to match variable declarations in C#
        },
        "javascript": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in JavaScript
            "method": r'function\s+(\w+)\(',  # Pattern to match function definitions in JavaScript
            "variable": r'(let|const|var)\s+(\w+)',  # Pattern to match variable declarations in JavaScript
        },
        "typescript": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in TypeScript
            "method": r'(\w+)\s*\(.*?\)\s*{',  # Pattern to match function definitions in TypeScript
            "variable": r'(let|const|var)\s+(\w+)',  # Pattern to match variable declarations in TypeScript
        },
        "php": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in PHP
            "method": r'function\s+(\w+)\(',  # Pattern to match function definitions in PHP
            "variable": r'\$(\w+)\s*=',  # Pattern to match variable declarations in PHP
        },
        "ruby": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in Ruby
            "method": r'def\s+(\w+)\(',  # Pattern to match method definitions in Ruby
            "variable": r'@(\w+)\s*=',  # Pattern to match instance variable declarations in Ruby
        },
        "go": {
            "class": r'type\s+(\w+)\s+struct',  # Pattern to match struct definitions in Go (Go does not use classes)
            "method": r'func\s+(\w+)\(',  # Pattern to match method/function definitions in Go
            "variable": r'var\s+(\w+)',  # Pattern to match variable declarations in Go
        },
        "swift": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in Swift
            "method": r'func\s+(\w+)\(',  # Pattern to match method definitions in Swift
            "variable": r'(let|var)\s+(\w+)',  # Pattern to match variable declarations in Swift
        },
        "kotlin": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in Kotlin
            "method": r'fun\s+(\w+)\(',  # Pattern to match method definitions in Kotlin
            "variable": r'(val|var)\s+(\w+)',  # Pattern to match variable declarations in Kotlin
        },
        "c": {
            "class": None,  # C does not have classes
            "method": r'\w+\s+(\w+)\s*\(',  # Pattern to match function definitions in C
            "variable": r'\w+\s+(\w+)\s*;',  # Pattern to match variable declarations in C
        },
        "cpp": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in C++
            "method": r'\w+\s+(\w+)\s*\(',  # Pattern to match function definitions in C++
            "variable": r'\w+\s+(\w+)\s*;',  # Pattern to match variable declarations in C++
        },
        "r": {
            "class": None,  # R does not use classes in the same way as OOP languages
            "method": r'(\w+)\s*<- function',  # Pattern to match function definitions in R
            "variable": r'(\w+)\s*<-',  # Pattern to match variable assignments in R
        },
        "scala": {
            "class": r'class\s+(\w+)',  # Pattern to match class definitions in Scala
            "method": r'def\s+(\w+)\(',  # Pattern to match method definitions in Scala
            "variable": r'val\s+(\w+)',  # Pattern to match value declarations in Scala
        },
        "rust": {
            "class": r'struct\s+(\w+)',  # Pattern to match struct definitions in Rust
            "method": r'fn\s+(\w+)\(',  # Pattern to match function definitions in Rust
            "variable": r'let\s+(\w+)',  # Pattern to match variable declarations in Rust
        },
        "perl": {
            "class": r'package\s+(\w+)',  # Pattern to match package definitions (Perl does not have classes natively)
            "method": r'sub\s+(\w+)\s*{',  # Pattern to match function definitions in Perl
            "variable": r'my\s+\$(\w+)',  # Pattern to match variable declarations in Perl
        },
        "bash": {
            "class": None,  # Bash does not have classes
            "method": r'function\s+(\w+)\s*\(\)',  # Pattern to match function definitions in Bash
            "variable": r'(\w+)=',  # Pattern to match variable assignments in Bash
        },
        "haskell": {
            "class": r'data\s+(\w+)',  # Pattern to match data type definitions (equivalent to classes) in Haskell
            "method": r'(\w+)\s*::',  # Pattern to match function signatures in Haskell
            "variable": r'(\w+)\s*=',  # Pattern to match variable declarations in Haskell
        },
        "elixir": {
            "class": r'defmodule\s+(\w+)',  # Pattern to match module definitions (equivalent to classes) in Elixir
            "method": r'def\s+(\w+)\(',  # Pattern to match function definitions in Elixir
            "variable": r'(\w+)\s*=',  # Pattern to match variable declarations in Elixir
        },
        "erlang": {
            "class": None,  # Erlang does not have classes
            "method": r'(\w+)\s*\(',  # Pattern to match function definitions in Erlang
            "variable": r'(\w+)\s*=',  # Pattern to match variable assignments in Erlang
        },
        "fortran": {
            "class": r'module\s+(\w+)',  # Pattern to match module definitions (equivalent to classes) in Fortran
            "method": r'subroutine\s+(\w+)',  # Pattern to match subroutine definitions in Fortran
            "variable": r'(\w+)\s*::',  # Pattern to match variable declarations in Fortran
        },
        "lua": {
            "class": None,  # Lua does not have classes natively
            "method": r'function\s+(\w+)\(',  # Pattern to match function definitions in Lua
            "variable": r'local\s+(\w+)',  # Pattern to match local variable declarations in Lua
        },
        "prolog": {
            "class": None,  # Prolog does not have classes
            "method": r'(\w+)\s*\(',  # Pattern to match predicate definitions in Prolog
            "variable": r'(\w+)\s*=',  # Pattern to match variable assignments in Prolog
        },
        "tcl": {
            "class": None,  # Tcl does not have classes
            "method": r'proc\s+(\w+)\s*\{',  # Pattern to match procedure definitions in Tcl
            "variable": r'set\s+(\w+)',  # Pattern to match variable assignments in Tcl
        },
        "racket": {
            "class": r'(module\s+(\w+))',  # Pattern to match module definitions in Racket
            "method": r'define\s+\(\s*(\w+)\s+',  # Pattern to match function definitions in Racket
            "variable": r'define\s+(\w+)',  # Pattern to match variable definitions in Racket
        },
        "cobol": {
            "class": None,  # COBOL does not have classes
            "method": r'PROCEDURE\s+DIVISION',  # Pattern to match the start of a method in COBOL
            "variable": r'(\w+)\s+PIC',  # Pattern to match variable declarations in COBOL
        },
        "objectivec": {
            "class": r'@interface\s+(\w+)',  # Pattern to match class definitions in Objective-C
            "method": r'[-|+]\s*\(.*?\)\s*(\w+)',  # Pattern to match method definitions in Objective-C
            "variable": r'(\w+)\s*=\s*',  # Pattern to match variable declarations in Objective-C
        },
        "sql": {
            "class": None,  # SQL does not have classes
            "method": r'CREATE\s+PROCEDURE\s+(\w+)',  # Pattern to match stored procedure definitions in SQL
            "variable": r'(\w+)\s+(INT|VARCHAR|CHAR|TEXT|DATE)',  # Pattern to match variable declarations in SQL
        },
    }
def get_segments(source_code, language):
    segment_functions = {
    'python': segment_python_code,
    'java': segment_java_code,
    'c': segment_c_code,
    'cpp': segment_cpp_code,
    'javascript': segment_javascript_code,
    'php': segment_php_code,
    'csharp': segment_csharp_code,
    'typescript': segment_typescript_code,
    'kotlin': segment_kotlin_code,
    'swift': segment_swift_code,
    'go': segment_go_code,
    'ruby': segment_ruby_code,
    'r': segment_r_code,
    'scala': segment_scala_code,
    'rust': segment_rust_code,
    'objectivec': segment_objectivec_code,
    'lua': segment_lua_code,
    'groovy': segment_groovy_code,
    'jshell': segment_jshell_code,
    'haskell': segment_haskell_code,
    'tcl': segment_tcl_code,
    'ocaml': segment_ocaml_code,
    'elixir': segment_elixir_code,
    'erlang': segment_erlang_code,
    'fsharp': segment_fsharp_code,
    'ada': segment_ada_code,
    'commonlisp': segment_common_lisp_code,
    'd': segment_d_code,
    'prolog': segment_prolog_code,
    'racket': segment_racket_code,
    'fortran': segment_fortran_code,
    'assembly': segment_assembly_code,
    }

    segment_function = segment_functions.get(language.lower())
    if segment_function:
        return segment_function(source_code)
    else:
        # Default segmentation behavior
        return {"Code": source_code}  # If the language is unsupported, return the whole code as a single segment


# Python segmentation
def segment_python_code(source_code):
    # Capture imports, global variables, classes, functions, and the main block
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*(import.*|from.*import.*)', source_code, flags=re.MULTILINE)),

        "Global Variables": '\n'.join(re.findall(r'^(?!.*def|.*class|if __name__|^\s*import|from.*import)(.*=.*)', source_code, flags=re.MULTILINE)),

        "Classes": re.findall(r'^\s*class\s+\w+\s*.*?:\s*(?:[\s\S]+?(?=^\s*class\s+|^\s*$))', source_code, flags=re.MULTILINE),

        "Functions": re.findall(r'^\s*def\s+[\w]+\s*\(.*?\):\s*(?:[\s\S]+?(?=^\s*def\s+|^\s*class\s+|^\s*$))', source_code, flags=re.MULTILINE),

        "Main Block": '\n'.join(re.findall(r'if __name__ == ["\']__main__["\']:\s*([\s\S]+)', source_code)),
    }

    # Now we handle methods inside classes
    class_methods = {}
    for class_segment in segments["Classes"]:
        class_name = re.findall(r'class\s+(\w+)', class_segment)[0]  # Get the class name
        methods_in_class = re.findall(r'^\s*def\s+[\w]+\s*\(.*?\):\s*(?:[\s\S]+?(?=^\s*def\s+|^\s*$))', class_segment, flags=re.MULTILINE)
        class_methods[class_name] = methods_in_class

    # Return segments with class methods captured separately
    return segments, class_methods

# Java segmentation
def segment_java_code(source_code):
    segments = {
        "Package": '\n'.join(re.findall(r'^\s*package\s+.*;', source_code, flags=re.MULTILINE)),
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*;', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'(public\s+class\s+[\w]+\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Methods": re.findall(r'(public|protected|private)\s+[\w<>\[\]]+\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
    }
    return segments


# C segmentation
def segment_c_code(source_code):
    segments = {
        "Includes": '\n'.join(re.findall(r'^\s*#include\s+.*', source_code, flags=re.MULTILINE)),
        "Defines": '\n'.join(re.findall(r'^\s*#define\s+.*', source_code, flags=re.MULTILINE)),
        "Global Variables": '\n'.join(re.findall(r'^[\w\s\*]+\s+\w+\s*(=\s*.*)?;', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'^[\w\s\*]+\s+\w+\s*\(.*\)\s*{[\s\S]+?^}', source_code, flags=re.MULTILINE),
    }
    return segments


# C++ segmentation (similar to C, but with classes)
def segment_cpp_code(source_code):
    segments = {
        "Includes": '\n'.join(re.findall(r'^\s*#include\s+.*', source_code, flags=re.MULTILINE)),
        "Defines": '\n'.join(re.findall(r'^\s*#define\s+.*', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'(class\s+[\w]+\s*{[\s\S]+?};)', source_code, flags=re.MULTILINE),
        "Global Variables": '\n'.join(re.findall(r'^[\w\s\*]+\s+\w+\s*(=\s*.*)?;', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'^[\w\s\*]+\s+\w+\s*\(.*\)\s*{[\s\S]+?^}', source_code, flags=re.MULTILINE),
    }
    return segments


# JavaScript segmentation
def segment_javascript_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*(import\s+.*;|const\s+.*\s*=\s*require\(.*\);)', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'(function\s+[\w]+\s*\(.*\)\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Classes": re.findall(r'(class\s+[\w]+\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*(var|let|const)\s+.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


# PHP segmentation
def segment_php_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*require.*;|^\s*include.*;', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'function\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Classes": re.findall(r'class\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'\$\w+\s*=\s*.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_csharp_code(source_code):
    segments = {
        "Using Statements": '\n'.join(re.findall(r'^\s*using\s+.*;', source_code, flags=re.MULTILINE)),
        "Namespaces": re.findall(r'^\s*namespace\s+[\w\.]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Classes": re.findall(r'(public|private|protected)\s+class\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Methods": re.findall(r'(public|protected|private)\s+[\w<>\[\]]+\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_typescript_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*;', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'(function\s+[\w]+\s*\(.*\)\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Classes": re.findall(r'(class\s+[\w]+\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*(let|const|var)\s+.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_kotlin_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'(class\s+[\w]+\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'fun\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*(val|var)\s+[\w]+\s*.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_swift_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'(class\s+[\w]+\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'func\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*(var|let)\s+.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_swift_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'(class\s+[\w]+\s*{[\s\S]+?})', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'func\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*(var|let)\s+.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_go_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'func\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Structs": re.findall(r'type\s+[\w]+\s+struct\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*(var|const)\s+.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_ruby_code(source_code):
    segments = {
        "Classes": re.findall(r'class\s+[\w]+\s*<*\s*[\w]*\s*[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Methods": re.findall(r'def\s+[\w]+\s*\(.*\)\s*[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Modules": re.findall(r'module\s+[\w]+\s*[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*[@\w]+\s*=\s*.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_r_code(source_code):
    segments = {
        "Libraries": '\n'.join(re.findall(r'^\s*library\s*\(.*\)', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'^\s*(\w+)\s*<- function\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*\w+\s*<-.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_scala_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'class\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Objects": re.findall(r'object\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Traits": re.findall(r'trait\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'def\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_rust_code(source_code):
    segments = {
        "Modules": '\n'.join(re.findall(r'^\s*mod\s+.*', source_code, flags=re.MULTILINE)),
        "Structs": re.findall(r'struct\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'fn\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Enums": re.findall(r'enum\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Traits": re.findall(r'trait\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_objectivec_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*#import\s+.*', source_code, flags=re.MULTILINE)),
        "Interfaces": re.findall(r'@interface\s+[\w]+\s*{[\s\S]+?}@end', source_code, flags=re.MULTILINE),
        "Implementations": re.findall(r'@implementation\s+[\w]+\s*{[\s\S]+?}@end', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'^\s*[-+]\s*\([\w\s\*]+\)\s*[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_lua_code(source_code):
    segments = {
        "Requires": '\n'.join(re.findall(r'^\s*require\s*\(.*\)', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'function\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}[\s]*end', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*local\s+[\w]+\s*=\s*.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_ada_code(source_code):
    segments = {
        "Packages": '\n'.join(re.findall(r'^\s*with\s+.*;', source_code, flags=re.MULTILINE)),
        "Imports": '\n'.join(re.findall(r'^\s*use\s+.*;', source_code, flags=re.MULTILINE)),
        "Procedures": re.findall(r'procedure\s+\w+\s*is\s*[\s\S]+?end\s+\w+;', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'function\s+\w+\s*return\s+\w+\s*is\s*[\s\S]+?end\s+\w+;', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*\w+\s*:\s*.*\s*:=\s*.*;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_common_lisp_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*\(require\s+.*\)', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'\(defun\s+\w+\s*\(.*?\)\s*[\s\S]*?\)', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'\(defvar\s+\w+\s*.*?\)', source_code, flags=re.MULTILINE)),
        "Macros": re.findall(r'\(defmacro\s+\w+\s*\(.*?\)\s*[\s\S]*?\)', source_code, flags=re.MULTILINE),
        "Classes": re.findall(r'\(defclass\s+\w+\s*\(.*?\)\s*[\s\S]*?\)', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_d_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*;', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'class\s+\w+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'^\w+\s+\w+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Global Variables": '\n'.join(re.findall(r'^\s*\w+\s+\w+\s*(=\s*.*)?;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_elixir_code(source_code):
    segments = {
        "Modules": re.findall(r'defmodule\s+\w+\s*do\s*[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'def\s+\w+\s*\(.*\)\s*do[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Macros": re.findall(r'defmacro\s+\w+\s*\(.*\)\s*do[\s\S]+?end', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_erlang_code(source_code):
    segments = {
        "Modules": re.findall(r'-module\(\w+\)\.', source_code, flags=re.MULTILINE),
        "Exports": re.findall(r'-export\(\[.*\]\)\.', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'^\w+\s*\(.*?\)\s*->\s*[\s\S]+?\.', source_code, flags=re.MULTILINE),
        "Includes": '\n'.join(re.findall(r'-include\([^\)]+\)\.', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_fsharp_code(source_code):
    segments = {
        "Modules": re.findall(r'module\s+\w+\s*=\s*', source_code, flags=re.MULTILINE),
        "Imports": '\n'.join(re.findall(r'^\s*open\s+.*', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'let\s+\w+\s*=\s*fun\s*\(.*\)\s*->[\s\S]+?(?=\s*let|$)', source_code, flags=re.MULTILINE),
        "Classes": re.findall(r'type\s+\w+\s*=\s*class\s*[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'let\s+\w+\s*=\s*.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_fortran_code(source_code):
    segments = {
        "Modules": re.findall(r'module\s+\w+\s*[\s\S]+?end\s+module\s+\w+', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'function\s+\w+\s*\(.*\)\s*[\s\S]+?end\s+function\s+\w+', source_code, flags=re.MULTILINE),
        "Subroutines": re.findall(r'subroutine\s+\w+\s*\(.*\)\s*[\s\S]+?end\s+subroutine\s+\w+', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*\w+\s*::\s*\w+.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_assembly_code(source_code):
    segments = {
        "Directives": '\n'.join(re.findall(r'^\s*\..*', source_code, flags=re.MULTILINE)),
        "Instructions": '\n'.join(re.findall(r'^\s*[a-zA-Z]+\s+.*', source_code, flags=re.MULTILINE)),
        "Labels": '\n'.join(re.findall(r'^\w+:\s*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_groovy_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Classes": re.findall(r'class\s+[\w]+\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Methods": re.findall(r'(def|void|[\w<>\[\]]+)\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*def\s+[\w]+\s*=.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_jshell_code(source_code):
    segments = {
        "Variables": '\n'.join(re.findall(r'^\s*\w+\s+[\w]+\s*=\s*.*', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'^\s*void\s+[\w]+\s*\(.*\)\s*{[\s\S]+?}', source_code, flags=re.MULTILINE),
        "Expressions": '\n'.join(re.findall(r'^\s*[\w\W]+;', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_haskell_code(source_code):
    segments = {
        "Imports": '\n'.join(re.findall(r'^\s*import\s+.*', source_code, flags=re.MULTILINE)),
        "Functions": re.findall(r'^\s*\w+\s*::\s*.*\n\s*\w+\s*=\s*.*', source_code, flags=re.MULTILINE),
        "Types": re.findall(r'^\s*data\s+[\w]+\s*=\s*.*', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'^\s*\w+\s*=\s*.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_tcl_code(source_code):
    segments = {
        "Procedures": re.findall(r'proc\s+[\w]+\s*\{.*\}\s*\{[\s\S]+?\}', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'set\s+[\w]+\s+.*', source_code, flags=re.MULTILINE)),
        "Comments": '\n'.join(re.findall(r'#.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_ocaml_code(source_code):
    segments = {
        "Modules": re.findall(r'module\s+\w+\s+=\s+struct[\s\S]+?end', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'let\s+[\w]+\s*\(.*\)\s*=\s*[\s\S]+?(?=let|$)', source_code, flags=re.MULTILINE),
        "Types": re.findall(r'type\s+[\w]+\s*=\s*[\s\S]+?;', source_code, flags=re.MULTILINE),
        "Variables": '\n'.join(re.findall(r'let\s+[\w]+\s*=\s*.*', source_code, flags=re.MULTILINE)),
    }
    return segments


def segment_prolog_code(source_code):
    segments = {
        "Facts": re.findall(r'^\s*\w+\(.*\)\s*\.', source_code, flags=re.MULTILINE),
        "Rules": re.findall(r'^\s*\w+\(.*\)\s*:-\s*[\s\S]+?\.', source_code, flags=re.MULTILINE),
        "Queries": re.findall(r'^\s*\?-?\s*\w+\(.*\)\s*\.', source_code, flags=re.MULTILINE),
    }
    return segments


def segment_racket_code(source_code):
    
    segments = {
        "Definitions": re.findall(r'^\s*\(define\s+\w+\s*.*\)', source_code, flags=re.MULTILINE),
        "Functions": re.findall(r'^\s*\(define\s+\(\w+\s*.*\)\s*[\s\S]+?\)', source_code, flags=re.MULTILINE),
        "Modules": re.findall(r'^\s*\(module\s+\w+\s*[\s\S]+?\)', source_code, flags=re.MULTILINE),
    }
    return segments
def extract_code_skeleton(source_code: str, language: str) -> str:
    """
    Extracts the skeleton structure (classes, methods, global variables) from the source code
    using language-specific patterns.
    
    Args:
        source_code (str): The source code to analyze.
        language (str): The programming language of the source code (e.g., 'python', 'java').
    
    Returns:
        str: The skeleton of the code.
    """
    skeleton = ""
    
    # Fetch patterns for the specific language
    patterns = get_language_patterns(language)
    
    # Extract class definitions
    if 'class' in patterns:
        for class_pattern in patterns['class']:
            classes = class_pattern.findall(source_code)
            for class_name in classes:
                skeleton += f"class {class_name} {{ ... }}\n"

    # Extract method definitions
    if 'method' in patterns:
        for method_pattern in patterns['method']:
            methods = method_pattern.findall(source_code)
            for method_name in methods:
                skeleton += f"def {method_name}(...): ...\n"
    
    # Extract global variable definitions
    if 'variable' in patterns:
        for variable_pattern in patterns['variable']:
            variables = variable_pattern.findall(source_code)
            for variable_name in variables:
                skeleton += f"{variable_name} = ...\n"

    return skeleton.strip()


def get_language_patterns(language: str) -> Dict[str, List[re.Pattern]]:

    return language_patterns.get(language.lower(), {})