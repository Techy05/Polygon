# This file is distributed as a part of the polygon project (justaprudev.github.io/polygon)
# By justaprudev

from pathlib import Path
from os import execl
import sys

@polygon.on(pattern="load")
async def load(e):
    reply = await e.get_reply_message()
    if not reply:
        await e.edit("`Reply to a polygon module to load it.`")
        return
    await e.edit("`Trying to load module..`")
    name = Path(reply.file.name).stem
    path = polygon.location / "modules" / reply.file.name
    if path.exists():
        await e.edit("`Module already exists, overwriting..`")
        polygon.unload(name)
        path.unlink()
    await polygon.download_media(reply, str(polygon.location / "modules"))
    try:
        polygon.load(name)
    except Exception as exc:
        await e.edit(f"The following error occured while unloading the module:\n`{exc}`")
        return
    output = f"Loaded module {name} successfully"
    polygon.log(output)
    await e.edit(f"`{output}!`")


@polygon.on(pattern="unload (.*)")
async def unload(e):
    module = e.pattern_match.group(1)
    path = polygon.location / "modules" / f"{module}.py"
    if not path.exists():
        await e.edit(f"`404: {module} not found!`")
        return
    await e.edit(f"`Trying to unload module {module}..`")
    try:
        polygon.unload(module)
        output = f"Unloaded module {module} successfully"
    except Exception as exc:
        await e.edit(f"The following error occured while unloading the module:\n`{exc}`")
        return
    polygon.log(output)
    await e.edit(f"`{output}!`")

@polygon.on(pattern="reload (.*)")
async def reload(e):
    await e.edit("`Reloading module..`")
    module = e.pattern_match.group(1)
    path = polygon.location / "modules" / f"{module}.py"
    if not path.exists():
        await e.edit("`Can't reload a module that doesnt exist!`")
        return
    if module in polygon.modules:
        await e.edit(f"`Module {module} is already loaded!`")
        return
    polygon.load(path.stem)
    output = f"Reloaded module {module} successfully"
    polygon.log(output)
    await e.edit(f"`{output}!`")

@polygon.on(pattern="restart")
async def restart(e):
    await e.edit("Polygon will be back soon!\nRun .ping to check if its back.")
    execl(sys.executable, sys.executable, *sys.argv)
