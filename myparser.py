# wypisywanie linii w informacji o bledzie
# na 29.03
class Parser:

    ##### Parser header #####
    def __init__(self, lexer):
        self.next_token = lexer.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token: " + self.token.type)
        if token_type != 'EOF':
            self.token = self.next_token()

    def error(self, msg):
        raise RuntimeError('Parser error, %s' % msg)

    ##### Parser body #####

    # Starting symbol
    def start(self):
        if self.token.type == 'EOF' or self.token.type == 'version' or self.token.type == 'services' or self.token.type == 'volumes' or self.token.type == 'networks':
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.program()
        elif self.token.type == 'version' or self.token.type == 'services' or self.token.type == 'volumes' or self.token.type == 'networks':
            self.top_element()
            self.program()
        else:
            pass

    def top_element(self):
        if self.token.type == 'version':
            self.take_token('version')
            self.take_token('ASSIGN')
            self.take_token('ID')
            self.take_token('NEWLINE')
            self.top_element()
            print('Version element OK.')
        elif self.token.type == 'services':
            self.take_token('services')
            self.take_token('ASSIGN')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.service_element()
            print('Services element OK.')
        elif self.token.type == 'volumes':
            self.take_token('volumes')
            self.take_token('ASSIGN')
            self.volumes_element()
            print('Volumes element OK.')
        elif self.token.type == 'networks':
            self.take_token('networks')
            self.take_token('ASSIGN')
            self.networks_element()
            print('Networks element OK.')
        elif self.token.type == 'EOF':
            self.take_token('EOF')

    def service_element(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
        if self.token.type == 'image':
            self.service_image()
        elif self.token.type == 'ports':
            self.service_ports()
        elif self.token.type == 'networks':
            self.service_networks()
        elif self.token.type == 'deploy':
            self.service_deploy()
        elif self.token.type == 'volumes':
            self.service_volumes()
        elif self.token.type == 'EOF':
            self.take_token('EOF')
        else:
            self.error('Only service elements allowed')

    def service_image(self):
        self.take_token('image')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.take_token('ID')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
            self.service_element()
        elif self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.top_element()
        else:
            self.error('Assign mark required')

    def service_ports(self):
        self.take_token('ports')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.list_element()
        else:
            self.error('Assign mark required')

    def list_element(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.take_token('LIST_ELEMENT')
                self.take_token('ID')
            self.skip()
            self.service_element()
            self.top_element()
        else:
            self.error('New line required')

    def skip(self):
        if self.token.type == 'SPACE':
            self.take_token('SPACE')
            self.skip()
        if self.token.type == 'INDENTATION':
            self.take_token('INDENTATION')
            self.skip()
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            self.skip()

    def service_networks(self):
        self.take_token('networks')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.list_element()
        else:
            self.error('Assign mark required')

    def service_deploy(self):
        self.take_token('deploy')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.take_token('NEWLINE')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
            self.take_token('INDENTATION')
            self.deploy_element()
        else:
            self.error('Assign mark required')

    def deploy_element(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            if self.token.type == 'ASSIGN':
                self.take_token('ASSIGN')
                self.take_token('ID')
                self.deploy_element()
        elif self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.take_token('INDENTATION')
                self.deploy_element()
            else:
                self.skip()
                self.top_element()
                self.service_element()

        elif self.token.type == 'INDENTATION':
            self.take_token('INDENTATION')
            self.skip()
            self.top_element()
            self.service_element()

    def service_volumes(self):
        self.take_token('volumes')
        if self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.list_element()
        else:
            self.error('Assign mark required')

    def volumes_element(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('ID')
                self.take_token('ASSIGN')
                self.volumes_element()
            else:
                self.volumes_element()
                self.top_element()

    def networks_element(self):
        if self.token.type == 'NEWLINE':
            self.take_token('NEWLINE')
            if self.token.type == 'INDENTATION':
                self.take_token('INDENTATION')
                self.take_token('ID')
                self.take_token('ASSIGN')
                self.networks_element()
            else:
                self.networks_element()
                self.top_element()
