# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

echo "
	      ╔╦╦╦══╦═╦═╦══╦══╗
	      ║║║╠╗╔╣╬║║╠║║╩╗╗║
	      ║║║╚╣║║╗╣║╠║║╦╩╝║
	      ╚═╩═╩╝╚╩╩═╩══╩══╝
	    °•° Deployment Begins •°•
"
echo '
        •• Getting Packages and Installing
'

export DEBIAN_FRONTEND=noninteractive
export TZ=Asia/Kolkata
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

apt-get update
apt-get upgrade -y
apt-get install -y --no-install-recommends ffmpeg neofetch mediainfo megatools
apt-get autoremove --purge

echo '
        •• Cloning Repository
'
git clone https://github.com/levina-lab/veez_ultrobot.git /root/levina-lab/

echo '
	•• Getting Libraries and Installing
'
pip install --upgrade pip setuptools wheel
pip install -r /root/levina-lab/requirements.txt

echo "
			      ┏┳┓╋┏┓╋╋╋╋┏┓┏┓
			      ┃┃┣┓┃┗┳┳┳━╋╋┛┃
			      ┃┃┃┗┫┏┫┏┫╋┃┃╋┃
			      ┗━┻━┻━┻┛┗━┻┻━┛
			•°• SAKURA DEPLOYMENT SELESAI °•°
		   •• Wait till python images are pushed
	   •• Give build logs in @gcsupportbots if build fails
"
