# -*- coding: utf-8 -*-
#
# Tuxemon
# Copyright (c) 2014-2017 William Edwards <shadowapex@gmail.com>,
#                         Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from tuxemon.core.components.locale import T
from tuxemon.core.states.combat.combat import fainted_party

logger = logging.getLogger(__name__)


def process_translate_text(game, text_slug, parameters):
    replace_values = {}

    # extract INI-style params
    for param in parameters:
        key, value = param.split("=")

        # TODO: is this code still valid? Translator class is NOT iterable
        """
        # Check to see if param_value is translatable
        if value in translator:
            value = trans(value)
        """
        # match special placeholders like ${{name}}
        replace_values[key] = replace_text(game, value)

    # generate translation
    text = T.format(text_slug, replace_values)

    # clear the terminal end-line symbol (multi-line translation records)
    text = text.rstrip("\n")

    # split text into pages for scrolling
    pages = text.split("\n")

    # generate scrollable text
    return [replace_text(game, page) for page in pages]


def check_battle_legal(player):
    """ Checks to see if the player has any monsters fit for battle.

    :type player: core.components.player.Player

    :rtype: bool
    """
    # Don't start a battle if we don't even have monsters in our party yet.
    if len(player.monsters) < 1:
        logger.warning("Cannot start battle, player has no monsters!")
        return False
    else:
        if fainted_party(player.monsters):
            logger.warning("Cannot start battle, player's monsters are all DEAD")
            return False
        else:
            return True


def replace_text(game, text):
    """ Replaces ${{var}} tiled variables with their in-game value.

    :param game: The main game object that contains all the game's variables.
    :param text: Raw text from the map

    :type game: core.control.Control
    :type text: str

    :rtype: str

    **Examples:**

    >>> replace_text("${{name}} is running away!")
    'Red is running away!'

    """
    text = text.replace("${{name}}", game.player1.name)
    text = text.replace(r"\n", "\n")

    for i in range(len(game.player1.monsters)):
        monster = game.player1.monsters[i]
        text = text.replace("${{monster_" + str(i) + "_name}}", monster.name)
        text = text.replace("${{monster_" + str(i) + "_desc}}", monster.description)
        text = text.replace("${{monster_" + str(i) + "_type}}", monster.slug)
        text = text.replace("${{monster_" + str(i) + "_hp}}", str(monster.current_hp))
        text = text.replace("${{monster_" + str(i) + "_hp_max}}", str(monster.hp))
        text = text.replace("${{monster_" + str(i) + "_level}}", str(monster.level))

    return text
