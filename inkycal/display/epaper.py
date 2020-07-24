#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Inky-Calendar epaper functions
Copyright by aceisace
"""
from importlib import import_module
from PIL import Image


class Display:
    """
    Display class for inkycal
    Handles rendering on display
    """
    def __init__(self, epaper_model: str) -> None:
        """
        Load the drivers for this epaper model
        """
        if 'colour' in epaper_model:
            self.supports_colour = True
        else:
            self.supports_colour = False

        try:
            driver_path = 'inkycal.display.drivers.{}'.format(epaper_model)
            driver = import_module(driver_path)
            self._epaper = driver.EPD()

        except ImportError:
            raise Exception('This module is not supported. Check your spellings?')

        except FileNotFoundError:
            raise Exception('SPI could not be found. Please check if SPI is enabled')

    def render(self, im_black: Image.Image, im_colour=None) -> None:
        """
        Render an image on the epaper
        im_colour is required for three-colour epapers
        """
        epaper = self._epaper

        if not self.supports_colour:
            print('Initialising..', end='')
            epaper.init()
            print('Updating display......', end='')
            epaper.display(epaper.getbuffer(im_black))
            print('Done')

        elif self.supports_colour:
            if not im_colour:
                raise Exception('im_colour is required for coloured epaper displays')
            print('Initialising..', end='')
            epaper.init()
            print('Updating display......', end='')
            epaper.display(epaper.getbuffer(im_black), epaper.getbuffer(im_colour))
            print('Done')

        print('Sending E-Paper to deep sleep...', end='')
        epaper.sleep()
        print('Done')

    def calibrate(self, cycles: int = 3) -> None:
        """
        Flush display with single colour to prevent burn-ins (ghosting)
        cycles -> int. How many times should each colour be flushed?
        recommended cycles = 3
        """
        epaper = self._epaper
        epaper.init()

        white = Image.new('1', (epaper.width, epaper.height), 'white')
        black = Image.new('1', (epaper.width, epaper.height), 'black')

        print('----------Started calibration of ePaper display----------')
        if self.supports_colour:
            for _ in range(cycles):
                print('Calibrating...', end=' ')
                print('black...', end=' ')
                epaper.display(epaper.getbuffer(black), epaper.getbuffer(white))
                print('colour...', end=' ')
                epaper.display(epaper.getbuffer(white), epaper.getbuffer(black))
                print('white...')
                epaper.display(epaper.getbuffer(white), epaper.getbuffer(white))
                print('Cycle {0} of {1} complete'.format(_ + 1, cycles))

        if not self.supports_colour:
            for _ in range(cycles):
                print('Calibrating...', end=' ')
                print('black...', end=' ')
                epaper.display(epaper.getbuffer(black))
                print('white...')
                epaper.display(epaper.getbuffer(white)),
                print('Cycle {0} of {1} complete'.format(_ + 1, cycles))

            print('-----------Calibration complete----------')
            epaper.sleep()
