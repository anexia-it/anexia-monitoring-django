import asyncio
import sys

from updatable import get_package_update_list, get_parsed_environment_package_list


async def get_python_env_info() -> dict:
    runtime = {
        'platform': 'python',
        'platform_version': sys.version,
        'framework': 'django',
        'framework_installed_version': None,
        'framework_newest_version': None,
    }
    modules = []
    packages = get_parsed_environment_package_list()

    for package in packages:
        package['_data'] = asyncio.create_task(
            get_package_update_list(package['package'], package['version'])
        )

    for package in packages:
        package_data = await package['_data']

        modules.append({
            'name': package['package'],
            'installed_version': package['version'],
            'installed_version_licences': [
                package_data['current_release_license'],
            ],
            'newest_version': package_data['latest_release'],
            'newest_version_licences': [
                package_data['latest_release_license'],
            ],
        })

        if package['package'] == 'Django':
            runtime['framework_installed_version'] = package['version']
            runtime['framework_newest_version'] = package_data['latest_release']

    return {
        'runtime': runtime,
        'modules': modules,
    }
