import asyncio
import sys
from os import environ, execle, path, remove
from typing import Tuple
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError


HEROKU_APP_NAME = Var.HEROKU_APP_NAME 
HEROKU_API_KEY = Var.HEROKU_API


requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await event.edit(
                "`mohon atur` **HEROKU_APP_NAME** `Var`"
                " agar dapat mendeploy userbot...`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await event.edit(
                f"{txt}\n" "`Invalid Heroku credentials for deploying userbot dyno.`"
            )
            return repo.__del__()
        await event.edit(
            "`userbot dyno build in progress, please wait until the process finishes it usually takes 4 to 5 minutes .`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/main", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n`here is the error log:\n{error}`")
            return repo.__del__()
        build = app.builds(order_by="created_at", sort="desc")[0]
        if build.status == "failed":
            await event.edit(
                "`build dibatalkan!\n" "terbatalkan atau terjadi suatu error...`"
            )
            await asyncio.sleep(5)
            return await event.delete()
        await event.edit("`berhasil dideploy!\n" "memulai ulang, mohon tunggu...`")
    else:
        await event.edit("`mohon atur`  **HEROKU_API**  ` Var...`")
    return


@ultroid_cmd(pattern=r"xupdate$")

async def upstream(event):
    event = await eor(event, "`pulling the main repo wait a sec...`")
    off_repo = "https://github.com/levina-lab/veez_ultrobot"
    cmd = f"rm -rf .git"
    try:
        await runcmd(cmd)
    except BaseException:
        pass
    try:
        txt = "`oops.. updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`direktori {error} tidak ditemukan`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`terjadi kesalahan! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = "main"
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("`deploying sakura userbot, please wait...`")
    await deploy(event, repo, ups_rem, ac_br, txt)
