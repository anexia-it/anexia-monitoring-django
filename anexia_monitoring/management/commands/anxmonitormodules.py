import asyncio
import json

from django.core.management.base import BaseCommand, CommandError
from anexia_monitoring.core import get_python_env_info


class Command(BaseCommand):
    help = "Outputs JSON object describing python runtime and modules. Same as /anxapi/vi/modules"

    def handle(self, *args, **kwargs):
        modules_dict = asyncio.run(get_python_env_info())
        modules_json = json.dumps(modules_dict, indent=4)
        self.stdout.write(modules_json)
        self.stdout.flush()
