# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
# from datetime import date
#import wiringpi2
# from subprocess import check_output,call,CalledProcessError
import subprocess




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

    def gpio_enable(self, pin):
        gpio_existe = False
        try:
            archivos = subprocess.Popen(['ls','/sys/class/gpio/'], stdout=subprocess.PIPE)
            ls_output = archivos.stdout.read()
            for file in ls_output.split('\n'):
                if file == 'gpio17_pg9':
                    gpio_existe = True
            if gpio_existe == False:
                try:
                    #Crear el enlace de configuracion del pin
                    export = open('/sys/class/gpio/export','w')
                    export.write(pin)
                    cerrado = False
                    while(cerrado == False):
                        try:
                            export.close()
                            cerrado = True
                        except IOError:
                            print "Aun no se puede cerrar el archivo {}".format(export)
                except Exception as e:
                    print 'Error {}'.format(e)
                    message = 'Hubo un problema habilitando el pin.'
                    raise exceptions.Warning(message, str(e))
                try:
                    subprocess.call('sudo chown -R odoo:odoo /sys/class/gpio/gpio17_pg9',shell = True)
                except Exception as e:
                    print 'Error {}'.format(e)
                    message = 'Hubo un problema cambiando propietario a los archivos de configuracion del pin.'
                    raise exceptions.Warning(message, str(e))
            #Se configura como salida el pin
            try:
                path = '/sys/class/gpio/gpio' + pin + '_pg9/direction'
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
        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema prendiendo el LED.'
            raise exceptions.Warning(message, str(e))


    @api.model
    def create(self, values):
        try:
            self.gpio_enable(self.led_pin)
        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema Configurando el pin.'
            raise exceptions.Warning(message, str(e))
        return super(cubie_odoo_led, self).create(values)



    @api.one
    def action_prender(self):
        self.state = 'prendido'
        try:
            gpio_existe = False
            archivos = subprocess.Popen(['ls','/sys/class/gpio/'], stdout=subprocess.PIPE)
            ls_output = archivos.stdout.read()
            for file in ls_output.split('\n'):
                if file == 'gpio17_pg9':
                    gpio_existe = True
            if gpio_existe == False:
                self.gpio_enable(self.led_pin)
        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema configurando el pin.'
            raise exceptions.Warning(message, str(e))
        try:
            path = '/sys/class/gpio/gpio' + self.led_pin + '_pg9/value'
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
            gpio_existe = False
            archivos = subprocess.Popen(['ls','/sys/class/gpio/'], stdout=subprocess.PIPE)
            ls_output = archivos.stdout.read()
            for file in ls_output.split('\n'):
                if file == 'gpio17_pg9':
                    gpio_existe = True
            if gpio_existe == False:
                self.gpio_enable(self.led_pin)
        except Exception as e:
            print 'Error {}'.format(e)
            message = 'Hubo un problema configurando el pin.'
            raise exceptions.Warning(message, str(e))
        try:
            path = '/sys/class/gpio/gpio' + self.led_pin + '_pg9/value'
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
