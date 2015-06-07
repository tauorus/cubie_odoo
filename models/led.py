# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from datetime import date
#import wiringpi2
import subprocess
from subprocess import CalledProcessError


class led(models.Model):
    _name = "cubie_odoo.led"

    led_pin = 17

    fecha = fields.Date('Fecha')
    state = fields.Selection(
        [('prendido','Prendido'),('apagado','Apagado')],
        default='apagado',
        string = 'Estado',
        readonly=True,
    )


    @api.model
    def create(self, values):
        export_= '/sys/class/gpio/export'
        _cwd = '/sys/class/gpio'
        try:
            subprocess.check_output(['echo', led_pin, '>', fexport_], stderr=subprocess.STDOUT, cwd=_cwd)
        except:
            print('Hubo un problema habilitando el pin.')
        try:
            subprocess.check_output(['echo', 'out', '>', 'gpio{}_pg*/direction'.format(led_pin)], stderr=subprocess.STDOUT, cwd=_cwd)
        except:
            raise exceptions.Warning('Hubo un problema configurando el pin como salida.')
#         wiringpi2.wiringPiSetupPhys() # init pin to phy mode,U14(1~48) U15(49~96)
#         wiringpi2.pinMode(self.led_pin,1) # set pin 17 to output mode 1
        return super(led, self).create(values)


    @api.one
    def action_prender(self):
        self.state = 'prendido'
        self.date = date.today()
#         wiringpi2.digitalWrite(self.led_pin,1) # Write 1 HIGH to pin 2
        _cwd = '/sys/class/gpio'
        try:
            subprocess.check_output(['echo', '1', '>', 'gpio{}_pg*/value'.format(led_pin)], stderr=subprocess.STDOUT, cwd=_cwd)
        except:
            print('Hubo un problema prendiendo el LED.')
#         if wiringpi2.digitalRead(self.led_pin) != 1:
#             raise exceptions.Warning('Hubo un problema encendiando el LED.')


    @api.one
    def action_apagar(self):
        self.state = 'apagado'
        self.date = date.today()
#         wiringpi2.digitalWrite(self.led_pin,0) # Write 0 to pin 17
        _cwd = '/sys/class/gpio'
        try:
            subprocess.check_output(['echo', '0', '>', 'gpio{}_pg*/value'.format(led_pin)], stderr=subprocess.STDOUT, cwd=_cwd)
        except:
            print('Hubo un problema apagando el LED.')
#         if wiringpi2.digitalRead(self.led_pin) != 0:
#             raise exceptions.Warning('Hubo un problema apagando el LED.')