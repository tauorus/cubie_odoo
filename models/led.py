# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
# from datetime import date
#import wiringpi2
# from subprocess import check_output,call,CalledProcessError
# import os




class cubie_odoo_led(models.Model):
    _name = "cubie_odoo.led"

    led_pin = '17'

    nombre = fields.Char('nombre',size=256)
    state = fields.Selection(
        [('prendido','Prendido'),('apagado','Apagado')],
        default='apagado',
        string = 'Estado',
        readonly=True,
    )


    @api.model
    def create(self, values):
#         Crear el enlace de configuracion del pin
        try:
            export= open('/sys/class/gpio/export','w')
            export.write(gpio)
            cerrado = False
            while(cerrado == False):
                try:
                    export.close()
                    cerrado = True
                except IOError:
                    print "Aun no se puede cerrar el archivo {}".format(export)
        except IOError:
            message = 'Hubo un problema habilitando el pin.'
            print(message)

#         Configurarlo como salida
        try:
            path = '/sys/class/gpio/gpio' + gpio + '_pg9/direction'
            direction = open (path,'w')
            direction.write('out')
            cerrado = False
            while(cerrado == False):
                try:
                    direction.close()
                    cerrado = True
                except IOError:
                    print "Aun no se puede cerrar el archivo {}".format(direction)
        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema configurando el pin.'
            raise exceptions.Warning(message, str(e))
        return super(cubie_odoo_led, self).create(values)



    @api.one
    def action_prender(self):
        self.state = 'prendido'
        try:
            path = '/sys/class/gpio/gpio' + gpio + '_pg9/value'
            value= open (path,'w')
            value.write('1')
            cerrado = False
            while(cerrado == False):
                try:
                    value.close()
                    cerrado = True
                except IOError:
                    print "Aun no se puede cerrar el archivo {}".format(value)
            

        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema prendiendo el LED.'
            raise exceptions.Warning(message, str(e))


    @api.one
    def action_apagar(self):
        self.state = 'apagado'
        try:
            path = '/sys/class/gpio/gpio' + gpio + '_pg9/value'
            value= open (path,'w')
            value.write('0')
            cerrado = False
            while(cerrado == False):
                try:
                    value.close()
                    cerrado = True
                except IOError:
                    print "Aun no se puede cerrar el archivo {}".format(value)
        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema apagando el LED.'
            raise exceptions.Warning(message, str(e))
