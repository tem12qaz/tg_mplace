from data.config import database_uri
from tortoise import Tortoise

from db.models import Project

TORTOISE_ORM = {
    "connections": {"default": database_uri},
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            " default_connection ": "default",
        },
    },
}


async def db_init():
    await Tortoise.init(
        db_url=database_uri,
        modules={'models': ['db.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def get_all_projects_with_token():
    projects = await Project.filter(bot_token__not_isnull=True)
    return projects
