# This file is distributed as a part of the polygon project (justaprudev.github.io/polygon)
# By justaprudev

import sys
import io
from pathlib import Path
import asyncio
import traceback
from functools import wraps

@polygon.on(prefix=">")
async def python(e):
    await e.edit("`Hmm, nice code..`")
    reply = await e.get_reply_message()
    code = e.text[1:]
    try:
        stdout, stderr = await async_exec(code, e)
    except:
        await e.edit(f"**Code**:\n```{code}```\n\n**Error**:\n```{traceback.format_exc()}```")
        return
    output = f"**Code**:\n```{code}```\n\n**stderr**:\n{stderr}\n\n**stdout**:\n```{stdout}```"
    if len(output) > 4096:
        with io.BytesIO(str.encode(output)) as f:
            f.name = "python.txt"
            await polygon.send_file(
                e.chat_id,
                f,
                force_document=True,
                caption=code,
                reply_to=reply
            )
            await e.delete()
            return
    await e.edit(output)

def redirect_console_output(func):
    """ Makes a function always return console output (ignores returned output) """

    def set_out():
        defaults = (sys.stdout, sys.stderr)
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        return defaults

    def reset_out(defaults):
        output = (sys.stdout.getvalue() or None, sys.stderr.getvalue() or None)
        sys.stdout, sys.stderr = defaults
        return output

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            defaults = set_out()
            await func(*args, **kwargs)
            return reset_out(defaults)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            defaults = set_out()
            func(*args, **kwargs)
            return reset_out(defaults)
    return wrapper

@redirect_console_output
async def async_exec(code, e):
    func = "__async_exec"
    formatted_code = f"async def {func}(e):" + "".join([f"\n    {l}" for l in code.split("\n")])
    exec(formatted_code)
    await locals()[func](e)
