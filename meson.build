project(
    'fastlr',
    'cpp',
    version: '0.1.0',
    default_options: [
        'cpp_std=c++14',
    ],
)

py = import('python').find_installation(pure: false)
pybind11_dep = dependency('pybind11')
armadillo_dep = dependency('armadillo')

extension_module = py.extension_module(
  '_fastlr',
  sources: [
    'src/py/fastlr.cpp',
    'src/core/irls.cpp',
  ],
  dependencies: [armadillo_dep, pybind11_dep],
  cpp_args: ['-O3', '-std=c++14'],
  install: true,
  install_dir: py.get_install_dir() / 'fastlr'  # ← correct target package
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
