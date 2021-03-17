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

                WORK IN PROGRESS
                '''
            ],
            'remind': [
                '!remind <time> | <event time> | <event details>',
                '''
                Sets a reminder in the message channel which notifies
                interested users who reacted to the message when the
                coutndown timer reaches 0.

                The time remaining is updated every minute.
                Time is based off [dateparser](https://dateparser.readthedocs.io/en/latest/) format.

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

                `!remind <time> | <event name> | <event info>`
                Sets a reminder for an event.

		`!help <command>`
		Get command specific help. Available commands:
                    {', '.join([f'`{command}`' for command in self.help_commands])}.

		'''

        self.help_footer = 'Send us feedback or contribute through Github'

        self.source="Source Code"
        self.github=f'[Github]({self.github})'


