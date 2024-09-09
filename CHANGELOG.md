# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [1.7.0]

### Added

- Support for Django 5.1
- Management command to export module data

## [1.6.0]

### Added
- Support for Python 3.11 and 3.12
- Support for Django 4.2 and 5.0

### Changed
- Distinguish between errors and warnings on up-check
- Register built-in up-checks via the `monitor_up_check` signal

### Removed
- Support for Python 3.7
- Support for Django 3.2, 4.0, 4.1

## [1.5.0]

### Added
- Support for Django 4.1

### Changed

- Pin updatable to `>=0.7`

## [1.4.1]

### Changed
- Pin updatable to `>=0.6,<0.7`

## [1.4.0]
### Added
- Support for Python 3.10
- Support for Django 4.0

### Removed
- Support for Django 2.2
- Support for Django 3.1
- Support for Python 3.5
- Support for Python 3.6

## [1.3.0]
### Added
- Created CHANGELOG
- Compatibility matrix
- Support for Python 3.9
- Support for Django 3.2

### Changed
- Enhanced README with GitHub shields (badges)

### Removed
- Support for Django 3.0

## [1.2.0]
### Added
- New setting: ANX_MONITORING_TEST_QUERY_USERS (Default: True)
- New setting: ANX_MONITORING_TEST_DB_CONNECTIONS (Default: True)
- Support for Python 3.7
- Support for Python 3.8
- Test project
- GitHub workflow action to run tests

### Changed
- Pinned dependency `updatable` to a version >= 0.4.1 and < 0.5
- Converted README from RST to MD

### Fixed
- README file name in setup

### Removed
- Support for Python 3.4

## [1.1.1]
### Changed
- Pinned dependency `updatable` to a version >= 0.3 and < 0.4

### Removed
- Support for Python 2.6
- Support for Python 3.3

### Fixed
- Removing previous builds in setup

## [1.1.0]
### Added
- License fields to modules endpoint

### Changed
- Pinned dependency `updatable` to a version >= 0.2 and < 0.3
- Overhauled setup.py
- Improved README

### Removed
- Removed file `setup.cfg`

## [1.0.0]
### Changed
- Renamed key `platform` to `runtime` in module response

## [0.1.0]
### Added
- Initial Release

[Unreleased]: https://github.com/anexia-it/anexia-monitoring-django/
[1.7.0]: https://pypi.org/project/django-anexia-monitoring/1.7.0/
[1.6.0]: https://pypi.org/project/django-anexia-monitoring/1.6.0/
[1.5.0]: https://pypi.org/project/django-anexia-monitoring/1.5.0/
[1.4.1]: https://pypi.org/project/django-anexia-monitoring/1.4.1/
[1.4.0]: https://pypi.org/project/django-anexia-monitoring/1.4.0/
[1.3.0]: https://pypi.org/project/django-anexia-monitoring/1.3.0/
[1.2.0]: https://pypi.org/project/django-anexia-monitoring/1.2.0/
[1.1.1]: https://pypi.org/project/django-anexia-monitoring/1.1.1/
[1.1.0]: https://pypi.org/project/django-anexia-monitoring/1.1.0/
[1.0.0]: https://pypi.org/project/django-anexia-monitoring/1.0.0/
[0.1.0]: https://pypi.org/project/django-anexia-monitoring/0.1.0/
