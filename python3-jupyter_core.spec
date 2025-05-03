#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Core common functionality of Jupyter projects
Summary(pl.UTF-8):	Główna, wspólna funkcjonalność projektów Jupyter
Name:		python3-jupyter_core
Version:	5.7.2
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jupyter_core/
Source0:	https://files.pythonhosted.org/packages/source/j/jupyter_core/jupyter_core-%{version}.tar.gz
# Source0-md5:	cd669418f83d14d6a1c2140b5fb36391
Patch0:		python-jupyter_core-tests.patch
Patch1:		python-jupyter_core-completions.patch
Patch2:		sphinx8.patch
URL:		https://pypi.org/project/jupyter_core/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling >= 1.4
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-pip
BuildRequires:	python3-pytest
BuildRequires:	python3-traitlets >= 4.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	python3-traitlets >= 4.0
BuildRequires:	sphinx-pdg-3 >= 8
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains base application classes and configuration
inherited by other projects. It doesn't do much on its own.

%description -l pl.UTF-8
Ten pakiet zawiera klasy bazowe aplikacji oraz konfigurację
dziedziczoną przez inne obiekty. Samodzielnie robi niewiele.

%package apidocs
Summary:	API documentation for Python jupyter_core module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jupyter_core
Group:		Documentation

%description apidocs
API documentation for Python jupyter_core module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jupyter_core.

%package -n bash-completion-jupyter
Summary:	Bash completion for jupyter commands
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów poleceń jupyter
Group:		Applications/Shells
Requires:	bash-completion >= 2.0
#Requires:	python-jupyter_core or python3-jupyter_core

%description -n bash-completion-jupyter
Bash completion for jupyter commands.

%description -n bash-completion-jupyter -l pl.UTF-8
Bashowe dopełnianie parametrów poleceń jupyter.

%package -n zsh-completion-jupyter
Summary:	Zsh completion for jupyter commands
Summary(pl.UTF-8):	Dopełnianie parametrów w zsh dla poleceń jupyter
Group:		Applications/Shells
#Requires:	python-jupyter_core or python3-jupyter_core
Requires:	zsh

%description -n zsh-completion-jupyter
Zsh completion for jupyter commands.

%description -n zsh-completion-jupyter -l pl.UTF-8
Dopełnianie parametrów w zsh dla poleceń jupyter.

%prep
%setup -q -n jupyter_core-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' jupyter_core/troubleshoot.py

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest --ignore=tests/test_paths.py tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

for f in $RPM_BUILD_ROOT%{_bindir}/jupyte* ; do
	%{__mv} "$f" "${f}-3"
done

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{zsh_compdir}}
cp -p examples/completions-zsh $RPM_BUILD_ROOT%{zsh_compdir}/_jupyter
cp -p examples/jupyter-completion.bash $RPM_BUILD_ROOT%{bash_compdir}/jupyter

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/jupyter-3
%attr(755,root,root) %{_bindir}/jupyter-migrate-3
%attr(755,root,root) %{_bindir}/jupyter-troubleshoot-3
%{py3_sitescriptdir}/jupyter.py
%{py3_sitescriptdir}/__pycache__/jupyter.cpython-*.py[co]
%{py3_sitescriptdir}/jupyter_core
%{py3_sitescriptdir}/jupyter_core-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif

%if 0
%files -n bash-completion-jupyter
%defattr(644,root,root,755)
%{bash_compdir}/jupyter

%files -n zsh-completion-jupyter
%defattr(644,root,root,755)
%{zsh_compdir}/_jupyter
%endif
