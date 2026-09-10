% filkomproposal.cls -- unofficial FILKOM UB proposal class
% Copyright 2026 Pande Kadek Nathan Prabhaswara Sudiara Putra
% Distributed under the LPPL 1.3c or later.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{filkomproposal}[2026/09/02 v0.1.0 Unofficial FILKOM proposal class]

\RequirePackage{kvoptions}
\SetupKeyvalOptions{family=filkomclass,prefix=filkomclass@}
\DeclareBoolOption[true]{preview}
\DeclareComplementaryOption{official}{preview}
\ProcessKeyvalOptions*
\LoadClass[a4paper,12pt,oneside]{report}

\RequirePackage[indonesian]{babel}
\RequirePackage{fontspec}
\RequirePackage{csquotes}
\DeclareQuoteAlias[american]{english}{indonesian}
\RequirePackage[left=4cm,right=3cm,top=3cm,bottom=3cm]{geometry}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\RequirePackage{graphicx}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage[titles]{tocloft}
\RequirePackage{caption}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{array}
\RequirePackage{enumitem}
\RequirePackage[fleqn]{amsmath}
\RequirePackage{xurl}
\RequirePackage{hyperref}
\RequirePackage{xkeyval}

\IfFontExistsTF{Calibri}{
  \setmainfont{Calibri}
}{
  \iffilkomclass@preview
    \IfFontExistsTF{Carlito}{
      \setmainfont{Carlito}
      \ClassWarningNoLine{filkomproposal}{Calibri tidak ditemukan; memakai Carlito untuk preview}
    }{
      \ClassError{filkomproposal}{Calibri dan Carlito tidak ditemukan}{Pasang Carlito untuk preview atau Calibri untuk keluaran resmi.}
    }
  \else
    \ClassError{filkomproposal}{Calibri wajib untuk mode official}{Pasang Calibri secara legal lalu ulangi kompilasi.}
  \fi
}

\newcommand{\filkom@judul}{}
\newcommand{\filkom@nama}{}
\newcommand{\filkom@nim}{}
\newcommand{\filkom@prodi}{}
\newcommand{\filkom@departemen}{}
\newcommand{\filkom@fakultas}{Fakultas Ilmu Komputer}
\newcommand{\filkom@universitas}{Universitas Brawijaya}
\newcommand{\filkom@kota}{Malang}
\newcommand{\filkom@tahun}{\the\year}
\newcommand{\filkom@logo}{assets/logo-ub.png}

\define@key{filkom}{judul}{\renewcommand{\filkom@judul}{#1}}
\define@key{filkom}{nama}{\renewcommand{\filkom@nama}{#1}}
\define@key{filkom}{nim}{\renewcommand{\filkom@nim}{#1}}
\define@key{filkom}{program-studi}{\renewcommand{\filkom@prodi}{#1}}
\define@key{filkom}{departemen}{\renewcommand{\filkom@departemen}{#1}}
\define@key{filkom}{fakultas}{\renewcommand{\filkom@fakultas}{#1}}
\define@key{filkom}{universitas}{\renewcommand{\filkom@universitas}{#1}}
\define@key{filkom}{kota}{\renewcommand{\filkom@kota}{#1}}
\define@key{filkom}{tahun}{\renewcommand{\filkom@tahun}{#1}}
\define@key{filkom}{logo}{\renewcommand{\filkom@logo}{#1}}
\newcommand{\filkomsetup}[1]{\setkeys{filkom}{#1}}

\newcommand{\filkom@require}[2]{%
  \ifx#1\@empty
    \ClassError{filkomproposal}{Metadata #2 belum diisi}{Isi kunci #2 pada metadata.tex.}%
  \fi
}
\AtBeginDocument{%
  \filkom@require{\filkom@judul}{judul}%
  \filkom@require{\filkom@nama}{nama}%
  \filkom@require{\filkom@nim}{nim}%
  \filkom@require{\filkom@prodi}{program-studi}%
  \filkom@require{\filkom@departemen}{departemen}%
}

\setstretch{1}
\setlength{\parindent}{0.6cm}
\setlength{\parskip}{6pt}
\AtBeginDocument{\setlength{\mathindent}{10\fontdimen2\font}}
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\setlist{nosep}
\captionsetup{font={normalsize,bf},labelsep=space}
\hypersetup{hidelinks,pdfauthor={\filkom@nama},pdftitle={\filkom@judul}}

\titleformat{\chapter}[block]
  {\centering\bfseries\fontsize{16pt}{19pt}\selectfont}
  {BAB \thechapter}{0.75em}{\MakeUppercase}
\titlespacing*{\chapter}{0pt}{0pt}{18pt}
\titleformat{name=\chapter,numberless}[block]
  {\centering\bfseries\fontsize{16pt}{19pt}\selectfont}
  {}{0pt}{\MakeUppercase}
\titleformat{\section}{\bfseries\fontsize{14pt}{17pt}\selectfont}{\thesection}{0.75em}{}
\titleformat{\subsection}{\bfseries\fontsize{14pt}{17pt}\selectfont}{\thesubsection}{0.75em}{}
\titleformat{\subsubsection}{\bfseries\itshape\fontsize{12pt}{14pt}\selectfont}{\thesubsubsection}{0.75em}{}
\titlespacing*{\section}{0pt}{12pt}{6pt}
\titlespacing*{\subsection}{0pt}{9pt}{6pt}
\titlespacing*{\subsubsection}{0pt}{9pt}{6pt}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}
\renewcommand{\cftchappresnum}{BAB\space}
\setlength{\cftchapnumwidth}{4.2em}

\pagestyle{fancy}
\fancyhf{}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\newcommand{\makeproposalcover}{%
  \hypersetup{pageanchor=false}%
  \begin{titlepage}
    \thispagestyle{empty}
    \setlength{\parskip}{0pt}
    \centering
    {\bfseries\fontsize{16pt}{19pt}\selectfont\MakeUppercase{\filkom@judul}\par}
    \vspace{1.4cm}
    {\fontsize{14pt}{17pt}\selectfont
    {\bfseries PROPOSAL SKRIPSI\par}
    \vspace{1.1cm}
    {Disusun oleh:\par}
    \vspace{0.25cm}
    {\MakeUppercase{\filkom@nama}\par}
    {NIM: \filkom@nim\par}
    \vfill
    \IfFileExists{\filkom@logo}{\includegraphics[width=5cm]{\filkom@logo}}{%
      \ClassError{filkomproposal}{Logo tidak ditemukan: \filkom@logo}{Periksa kunci logo pada metadata.tex.}}
    \vfill
    {\MakeUppercase{PROGRAM STUDI \filkom@prodi}\par}
    {\MakeUppercase{\filkom@departemen}\par}
    {\MakeUppercase{\filkom@fakultas}\par}
    {\MakeUppercase{\filkom@universitas}\par}
    {\MakeUppercase{\filkom@kota}\par}
    {\filkom@tahun\par}
    }
  \end{titlepage}
  \hypersetup{pageanchor=true}%
}

\addto\captionsindonesian{%
  \renewcommand{\contentsname}{DAFTAR ISI}%
  \renewcommand{\listtablename}{DAFTAR TABEL}%
  \renewcommand{\listfigurename}{DAFTAR GAMBAR}%
}

\newcommand{\makeproposalfrontmatter}{%
  \pagenumbering{roman}
  \setcounter{page}{2}
  \cleardoublepage
  \phantomsection
  \addcontentsline{toc}{chapter}{\contentsname}
  \tableofcontents\clearpage
  \cleardoublepage
  \phantomsection
  \addcontentsline{toc}{chapter}{\listtablename}
  \listoftables\clearpage
  \cleardoublepage
  \phantomsection
  \addcontentsline{toc}{chapter}{\listfigurename}
  \listoffigures\clearpage
  \chapter*{DAFTAR LAMPIRAN}
  \addcontentsline{toc}{chapter}{DAFTAR LAMPIRAN}
  \@starttoc{loa}\clearpage
}
\newcommand{\proposalmainmatter}{\clearpage\pagenumbering{arabic}\setcounter{page}{1}}
\newcommand{\proposalappendix}[1]{%
  \refstepcounter{chapter}%
  \chapter*{LAMPIRAN \thechapter\space \MakeUppercase{#1}}%
  \addcontentsline{toc}{chapter}{LAMPIRAN \thechapter\space #1}%
  \addcontentsline{loa}{chapter}{LAMPIRAN \thechapter\space #1}}

\endinput
