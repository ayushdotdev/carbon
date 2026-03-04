from discord import ButtonStyle, ui, Interaction
from app.i18n.context import ExecutionContext
from app.utils.consts.branding import INVITE_LINK


class InviteView(ui.View):
    def __init__(self, interaction: Interaction, *, timeout: float | None = 180):
        self.interaction = interaction
        ExecutionContext.set_context(self.interaction)
        super().__init__(timeout=timeout)

        self.add_item(
            ui.Button(label="Invite", style=ButtonStyle.link, url=INVITE_LINK)
        )
