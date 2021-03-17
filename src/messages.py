class Messages:
    def __init__(self):
        # Links
        self.github = 'https://github.com/uqcybersquad/discord-bot'
        # Generic error messages
        self.err = 'Unknown error, please contact a mod.'
        self.err_parse = 'Failed to parse arguments, please double check your command.'
        self.err_privileges = 'Error: Only an admin/mod can perform this action.'
        self.err_cooldown = 'Command cooldown, please try again in a few seconds.'

        # Command specific help messages
        self.help_commands = {
            'course': [
                '!course <Course Code>',
                '''
                Queries UQ course profiles for course specific data. Displays
                the summary, prerequisites, recommended prerequisites, and
                assessment methods. Also has an embedded link for easy access to
                the course profile online.
                '''
            ],
            'lolcrypto': [
                '!lolcrypto <encrypted string>',
                '''
                Automatically decrypts a specified string without knowing
                the key or cipher.
                '''
            ],
            'remind': [
                '!remind <time> | <event>',
                '''
                Sets a reminder in the message channel which notifies
                users who reacted to the message when the coutndown goes to 0.
                The clock is updated every minute.

                Bug: Reminder will stop working once bot is restarted.
                This is due to how the scheduler is set up and will be fixed
                in a later update.

                Admin/Moderators privileges required.
                '''
            ]
        }

        # General help message
        self.help_title = 'Help'
        self.help_description = f'''
		**Commands**

                `!course <course code>`
                Gets UQ course information based on course code.

                `!remind <time> | <event>`
                Sets a reminder for an event.

		`!help <command>`
		Get command specific help. Available commands:
                    {', '.join([f'`{command}`' for command in self.help_commands])}.

		'''

        self.help_footer = 'Send us feedback or contribute through Github'

        self.source="Source Code"
        self.github=f'[Github]({self.github})'


