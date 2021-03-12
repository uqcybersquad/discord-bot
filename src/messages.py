class Messages:
    def __init__(self):
        # Links
        self.github = 'https://github.com/uqcybersquad/discord-bot'
        # Generic error messages
        self.err = 'Unknown error, please contact a mod.'
        self.err_privileges = 'Error: Only an admin/mod can perform this action.'
        self.err_cooldown = 'Command cooldown, please try again in a few seconds.'

        # Command specific help messages
        self.help_commands = {
            # WIP
        }

        # General help message
        self.help_title = 'Help'
        self.help_description = f'''
		**Commands**

		`-help <command>`
		Get command specific help. Commands: {', '.join([f'`{command}`' for command in self.help_commands])}.
		'''

        self.help_footer = 'Send us feedback or contribute through Github'

        self.source="Source Code"
        self.github=f'[Github]({self.github})'


