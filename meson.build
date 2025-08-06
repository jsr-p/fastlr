project(
  'fastlr',
  'cpp',
  version: '0.1.0'
)

meson_version = '>=1.1'

if meson.get_compiler('cpp').get_id() == 'msvc'
  cpp_args = []
else
  cpp_args = ['-O3', '-std=c++14']
endif

py = import('python').find_installation(pure: false)
pybind11_dep = dependency('pybind11', required: true)  # keep required

armadillo_dep = dependency('armadillo', required: false)
lapack_dep = dependency('openblas', required: false)


if host_machine.system() == 'windows'
  conda_prefix = get_option('conda_prefix')
  if conda_prefix == ''
    error('On Windows, you must supply -Dconda_prefix=<conda‑env‑path>')
  endif

  inc_dir = join_paths(conda_prefix, 'Library/include')
  lib_dir = join_paths(conda_prefix, 'Library/lib')

  if not armadillo_dep.found()
    armadillo_dep = declare_dependency(
      include_directories: include_directories(inc_dir),
      link_args: ['-L' + lib_dir, '-larmadillo']
    )
    if not armadillo_dep.found()
      error('Armadillo dependency not found in ' + inc_dir + ' and ' + lib_dir)
    endif
  endif

  if not lapack_dep.found()
    lapack_dep = declare_dependency(
      link_args: ['-L' + lib_dir, '-lopenblas']
    )
    if not lapack_dep.found()
      error('OpenBLAS dependency not found in ' + lib_dir)
    endif
  endif

else
  # Linux/macOS fallback
  if not armadillo_dep.found()
    error('Armadillo dependency not found via pkg-config or default locations.')
  endif

  if not lapack_dep.found()
    error('OpenBLAS dependency not found via pkg-config or default locations.')
  endif
endif

extension_module = py.extension_module(
  '_fastlr',
  sources: [
    'src/py/fastlr.cpp',
    'src/core/irls.cpp',
  ],
  dependencies: [armadillo_dep, pybind11_dep, lapack_dep],
  cpp_args: cpp_args,
  install: true,
  install_dir: py.get_install_dir() / 'fastlr',
)

py.install_sources(
  [
    'src/fastlr/__init__.py',
    'src/fastlr/logreg.py',
    'src/fastlr/utils.py',
  ],
  pure: false,
  subdir: 'fastlr',
)
