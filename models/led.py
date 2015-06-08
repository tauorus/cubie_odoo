# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from datetime import date
#import wiringpi2
from subprocess import check_output,call,CalledProcessError



class cubie_odoo_led(models.Model):
    _name = "cubie_odoo.led"

    led_pin = 17

    nombre = fields.Char('nombre',size=256)
    state = fields.Selection(
        [('prendido','Prendido'),('apagado','Apagado')],
        default='apagado',
        string = 'Estado',
        readonly=True,
    )


    @api.model
    def create(self, values):
#         export_= '/sys/class/gpio/export'
#         _cwd = '/sys/class/gpio'
        try:
            check_output('echo {} > /sys/class/gpio/export'.format(self.led_pin), shell=True)
        except CalledProcessError, e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema habilitando el pin.'
            print(message, str(e))

        try:
            check_output('echo out > /sys/class/gpio/gpio{}_pg*/direction'.format(self.led_pin), shell=True)
        except CalledProcessError, e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema configurando el pin.'
            raise exceptions.Warning(message, str(e))
        return super(cubie_odoo_led, self).create(values)


    @api.one
    def action_prender(self):
        self.state = 'prendido'
#         self.date = date.today()
#         wiringpi2.digitalWrite(self.led_pin,1) # Write 1 HIGH to pin 2
#         _cwd = '/sys/class/gpio'
        try:
            check_output('echo 1 > /sys/class/gpio/gpio{}_pg*/value'.format(self.led_pin), shell=True)
        except CalledProcessError, e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema prendiendo el LED.'
            raise exceptions.Warning(message, str(e))


    @api.one
    def action_apagar(self):
        self.state = 'apagado'
        try:
            check_output('echo 0 > /sys/class/gpio/gpio{}_pg*/value'.format(self.led_pin), shell=True)
        except CalledProcessError, e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema apagando el LED.'
            raise exceptions.Warning(message, str(e))

