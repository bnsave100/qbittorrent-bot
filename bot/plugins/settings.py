import logging

# noinspection PyPackageRequirements
from telegram.ext import CommandHandler, CallbackQueryHandler
# noinspection PyPackageRequirements
from telegram import ParseMode

from bot import qb
from bot import updater
from utils import u
from utils import kb
from utils import Permissions

logger = logging.getLogger(__name__)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_settings_command(_, update):
    logger.info('/settings from %s', update.effective_user.first_name)

    preferences = qb.preferences()
    lines = sorted(['{}: <code>{}</code>'.format(k, v) for k, v in preferences.items()])

    for strings_chunk in u.split_text(lines):
        update.message.reply_html('\n'.join(strings_chunk), disable_web_page_preview=True)


@u.check_permissions(required_permission=Permissions.EDIT)
@u.failwithmessage
def change_setting(_, update, args):
    logger.info('/set from %s', update.effective_user.first_name)

    if len(args) < 2:
        update.message.reply_html('Usage: /set <code>[setting] [value]</code>')
        return

    key = args[0].lower()
    val = args[1]

    qb.set_preferences(**{key: val})

    update.message.reply_html('<b>Setting changed</b>:\n\n<code>{}</code>'.format(val))


updater.add_handler(CommandHandler(['settings', 's'], on_settings_command))
updater.add_handler(CommandHandler(['set'], change_setting, pass_args=True))
