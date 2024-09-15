// List of programming languages
export const languages = [
    // Programming Languages
    { name: 'Java', value: 'java', category: 'Programming Languages' },
    { name: 'Python', value: 'python', category: 'Programming Languages' },
    { name: 'C', value: 'c', category: 'Programming Languages' },
    { name: 'C++', value: 'cpp', category: 'Programming Languages' },
    { name: 'JavaScript', value: 'javascript', category: 'Programming Languages' },
    { name: 'TypeScript', value: 'typescript', category: 'Programming Languages' },
    { name: 'Ruby', value: 'ruby', category: 'Programming Languages' },
    { name: 'Go', value: 'go', category: 'Programming Languages' },
    { name: 'Swift', value: 'swift', category: 'Programming Languages' },
    { name: 'PHP', value: 'php', category: 'Programming Languages' },
    { name: 'C#', value: 'csharp', category: 'Programming Languages' },
    { name: 'Kotlin', value: 'kotlin', category: 'Programming Languages' },
    { name: 'Scala', value: 'scala', category: 'Programming Languages' },
    { name: 'Rust', value: 'rust', category: 'Programming Languages' },
    { name: 'Perl', value: 'perl', category: 'Programming Languages' },
    { name: 'Lua', value: 'lua', category: 'Programming Languages' },
    { name: 'Haskell', value: 'haskell', category: 'Programming Languages' },
    { name: 'Erlang', value: 'erlang', category: 'Programming Languages' },
    { name: 'Elixir', value: 'elixir', category: 'Programming Languages' },
    { name: 'F#', value: 'fsharp', category: 'Programming Languages' },
    { name: 'Fortran', value: 'fortran', category: 'Programming Languages' },
    { name: 'R', value: 'r', category: 'Programming Languages' },
    { name: 'Objective-C', value: 'objectivec', category: 'Programming Languages' },
    { name: 'Groovy', value: 'groovy', category: 'Programming Languages' },
    { name: 'D', value: 'd', category: 'Programming Languages' },
    { name: 'Common Lisp', value: 'commonlisp', category: 'Programming Languages' },
    { name: 'OCaml', value: 'ocaml', category: 'Programming Languages' },
    { name: 'Racket', value: 'racket', category: 'Programming Languages' },
    { name: 'Pascal', value: 'pascal', category: 'Programming Languages' },
    { name: 'Ada', value: 'ada', category: 'Programming Languages' },
    { name: 'Prolog', value: 'prolog', category: 'Programming Languages' },
    { name: 'Assembly', value: 'assembly', category: 'Programming Languages' },
    { name: 'Bash', value: 'bash', category: 'Scripting Languages' },
    { name: 'Shell Script', value: 'sh', category: 'Scripting Languages' },
    { name: 'PowerShell', value: 'powershell', category: 'Scripting Languages' },
    { name: 'Python2', value: 'python2', category: 'Programming Languages' },
    { name: 'NodeJS', value: 'nodejs', category: 'Programming Languages' },
    { name: 'CoffeeScript', value: 'coffeescript', category: 'Programming Languages' },
    { name: 'Clojure', value: 'clojure', category: 'Programming Languages' },
    { name: 'Visual Basic (VB.NET)', value: 'vb', category: 'Programming Languages' },
    { name: 'Basic', value: 'basic', category: 'Programming Languages' },
    { name: 'Brainfuck', value: 'brainfk', category: 'Esoteric Languages' },
  
    // Database Languages
    { name: 'MySQL', value: 'mysql', category: 'Database Languages' },
    { name: 'Oracle Database', value: 'oracle', category: 'Database Languages' },
    { name: 'PostgreSQL', value: 'postgresql', category: 'Database Languages' },
    { name: 'MongoDB', value: 'mongodb', category: 'Database Languages' },
    { name: 'SQLite', value: 'sqlite', category: 'Database Languages' },
    { name: 'Redis', value: 'redis', category: 'Database Languages' },
    { name: 'MariaDB', value: 'mariadb', category: 'Database Languages' },
    { name: 'Oracle PL/SQL', value: 'plsql', category: 'Database Languages' },
    { name: 'Microsoft SQL Server', value: 'sqlserver', category: 'Database Languages' },
  
    // Markup and Other Languages
    { name: 'HTML', value: 'html', category: 'Markup Languages' },
    { name: 'XML', value: 'xml', category: 'Markup Languages' },
    { name: 'JSON', value: 'json', category: 'Data Formats' },
    { name: 'YAML', value: 'yaml', category: 'Data Formats' },
    { name: 'Markdown', value: 'markdown', category: 'Markup Languages' },
    { name: 'Plain Text', value: 'text', category: 'Others' },
  ];
  
  
  export const languageMappings = {
    python: ['java', 'javascript', 'c', 'cpp', 'ruby', 'go', 'swift', 'php', 'csharp', 'kotlin', 'typescript', 'r', 'perl', 'rust', 'scala'],
    java: ['python', 'javascript', 'c', 'cpp', 'ruby', 'go', 'swift', 'php', 'csharp', 'kotlin', 'typescript', 'scala', 'groovy', 'r'],
    javascript: ['python', 'java', 'ruby', 'go', 'swift', 'php', 'csharp', 'kotlin', 'typescript', 'lua'],
    c: ['python', 'java', 'cpp', 'go', 'rust', 'scala', 'csharp', 'swift', 'javascript'],
    cpp: ['python', 'java', 'c', 'go', 'rust', 'csharp', 'scala'],
    ruby: ['python', 'java', 'javascript', 'php', 'go', 'swift', 'typescript'],
    go: ['python', 'java', 'c', 'cpp', 'rust', 'javascript'],
    swift: ['python', 'java', 'javascript', 'ruby', 'php', 'go', 'csharp', 'kotlin', 'typescript'],
    php: ['python', 'java', 'javascript', 'ruby', 'go', 'swift', 'typescript'],
    csharp: ['python', 'java', 'javascript', 'ruby', 'swift', 'php', 'go', 'typescript'],
    kotlin: ['java', 'swift', 'csharp', 'python', 'go', 'javascript', 'php', 'typescript'],
    typescript: ['javascript', 'python', 'java', 'php', 'csharp', 'go', 'ruby', 'swift'],
    r: ['python', 'java', 'scala', 'go'],
    rust: ['python', 'java', 'cpp', 'c', 'go', 'swift'],
    perl: ['python', 'ruby', 'php'],
    scala: ['java', 'python', 'csharp', 'go'],
    haskell: ['ocaml', 'fsharp'],
    lua: ['python', 'javascript'],
    groovy: ['java', 'kotlin'],
    tcl: ['python', 'perl'],
    ocaml: ['haskell', 'fsharp'],
    fsharp: ['ocaml', 'haskell', 'scala'],
    elixir: ['erlang'],
    erlang: ['elixir'],
    fortran: ['c', 'cpp', 'assembly'],
    prolog: ['commonlisp'],
    commonlisp: ['prolog', 'scheme'],
    d: ['c', 'cpp', 'rust'],
    ada: ['pascal'],
    assembly: ['c', 'fortran'],
    objectivec: ['swift', 'c'],
    racket: ['scheme', 'lisp'],
    bash: ['python', 'perl'],
    
    // SQL and database-related mappings
    mysql: ['oracle', 'postgresql', 'sqlite', 'mariadb', 'sqlserver'],
    oracle: ['mysql', 'postgresql', 'sqlite', 'mariadb', 'sqlserver'],
    postgresql: ['mysql', 'oracle', 'sqlite', 'mariadb', 'sqlserver'],
    mongodb: ['mysql', 'postgresql', 'oracle', 'mariadb', 'sqlserver'],
    sqlite: ['mysql', 'oracle', 'postgresql', 'mariadb', 'sqlserver'],
    redis: ['mysql', 'oracle', 'postgresql', 'mariadb', 'sqlserver'],
    mariadb: ['mysql', 'oracle', 'postgresql', 'sqlite', 'sqlserver'],
    plsql: ['sqlserver', 'mysql', 'postgresql', 'oracle', 'sqlite'],
    sqlserver: ['mysql', 'oracle', 'postgresql', 'mariadb', 'sqlite'],
  
    cobol: ['vb', 'pascal'],
    vb: ['csharp', 'java'],
    pascal: ['ada'],
    brainfuck: ['c'],
    clojure: ['lisp', 'scala'],
  };
  
  
  // Function to get file extension based on language
  export const getFileExtension = (language) => {
    switch (language) {
      case 'python':
      case 'python2':
        return '.py';
      case 'javascript':
      case 'nodejs':
        return '.js';
      case 'java':
        return '.java';
      case 'c':
        return '.c';
      case 'cpp':
        return '.cpp';
      case 'groovy':
        return '.groovy';
      case 'jshell':
        return '.jsh';
      case 'haskell':
        return '.hs';
      case 'tcl':
        return '.tcl';
      case 'lua':
        return '.lua';
      case 'ada':
        return '.adb';
      case 'commonlisp':
        return '.lisp';
      case 'd':
        return '.d';
      case 'elixir':
        return '.ex';
      case 'erlang':
        return '.erl';
      case 'fsharp':
        return '.fs';
      case 'fortran':
        return '.f90';
      case 'assembly':
        return '.asm';
      case 'scala':
        return '.scala';
      case 'php':
        return '.php';
      case 'csharp':
        return '.cs';
      case 'perl':
        return '.pl';
      case 'ruby':
        return '.rb';
      case 'go':
        return '.go';
      case 'r':
        return '.r';
      case 'racket':
        return '.rkt';
      case 'ocaml':
        return '.ml';
      case 'vb':
      case 'basic':
        return '.vb';
      case 'bash':
        return '.sh';
      case 'clojure':
        return '.clj';
      case 'typescript':
        return '.ts';
      case 'cobol':
        return '.cob';
      case 'kotlin':
        return '.kt';
      case 'pascal':
        return '.pas';
      case 'prolog':
        return '.pl';
      case 'rust':
        return '.rs';
      case 'swift':
        return '.swift';
      case 'objectivec':
        return '.m';
      case 'octave':
        return '.m';
      case 'text':
        return '.txt';
      case 'brainfk':
        return '.bf';
      case 'coffeescript':
        return '.coffee';
      case 'ejs':
        return '.ejs';
      case 'mysql':
      case 'oracle':
      case 'postgresql':
      case 'mongodb':
      case 'sqlite':
      case 'redis':
      case 'mariadb':
      case 'plsql':
      case 'sqlserver':
        return '.sql';
      default:
        return '.txt'; // Default extension for any unknown language
    }
  };
  
  // Supported modes in AceEditor
  export const supportedModes = [
    'javascript',
    'java',
    'python',
    'ruby',
    'csharp',
    'php',
    'c_cpp',
    'go',
    'typescript',
    'sql',
    'swift',
    'bash',
    'cobol',
    'perl',
    'rust',
    'scala',
    'kotlin',
    'objectivec',
  ];
  
  // Function to map language to AceEditor mode
  export const getEditorMode = (language) => {
    // Map certain languages to AceEditor modes
    const languageMap = {
      'c': 'c_cpp',
      'cpp': 'c_cpp',
      'csharp': 'csharp',
      'fsharp': 'fsharp',
      'objectivec': 'objectivec',
      'mysql': 'sql',
      'oracle': 'sql',
      'postgresql': 'sql',
      'mongodb': 'sql',
      'sqlite': 'sql',
      'redis': 'sql',
      'mariadb': 'sql',
      'plsql': 'sql',
      'sqlserver': 'sql',
      'typescript': 'typescript',
      'javascript': 'javascript',
      'nodejs': 'javascript',
      'sh': 'bash',
      'bash': 'bash',
      'perl': 'perl',
      'kotlin': 'kotlin',
      'rust': 'rust',
      'scala': 'scala',
      'php': 'php',
    };
  
    const mode = languageMap[language] || language;
    return supportedModes.includes(mode) ? mode : 'text';
  };
  