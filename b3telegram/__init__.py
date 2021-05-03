# # coding=utf-8
#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 Daniele Pantaleone <fenix@bigbrotherbot.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import os
import urllib2
import b3
import b3.functions
import b3.plugin
import b3.config
import b3.cron


class B3Telegram(b3.plugin.Plugin):
    requiresConfigFile = False

    requiresVersion = '1.10'
    requiresParsers = ['iourt43']
    requiresPlugins = []
    loadAfterPlugins = []

    def __init__(self, console, config=None):
        b3.plugin.Plugin.__init__(self, console, config)

        self.telegram_token=os.getenv("TELEGRAM_TOKEN")
        self.telegram_group_id=os.getenv("TELEGRAM_GROUP_ID")
        self.telegram_message_id=os.getenv("TELEGRAM_MESSAGE_ID")

    def onLoadConfig(self):
        pass

    def onStartup(self):
        self.registerEvent('EVT_CLIENT_CONNECT', self.sendUpdate)
        self.registerEvent('EVT_CLIENT_DISCONNECT', self.sendUpdate)
        self.registerEvent('EVT_GAME_MAP_CHANGE', self.sendUpdate)

    def sendUpdate(self, event):
        clients = self.console.clients.getList()
        mapName = self.console.game.mapName
        server_data = "Map {mapname} with {players} player(s):".format(mapname=mapName, players=len(clients))
        players_data = "\n".join([player.name for player in clients])
        msg = "{server_data}\n{players_data}".format(server_data=server_data, players_data=players_data)
        url = "https://api.telegram.org/bot{token}/editmessagetext?chat_id={group_id}&message_id={message_id}&text={msg}".format(token=self.telegram_token, group_id=self.telegram_group_id, message_id=self.telegram_message_id, msg=urllib2.quote(msg))
        try:
            urllib2.urlopen(url)
        except:
            self.error(e)
