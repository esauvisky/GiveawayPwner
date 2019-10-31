#!/usr/bin/env python3.7
__author__ = "Emiliano Sauvisky"
__version__ = "1.0"
__license__ = "MIT"

import argparse
import asyncio
import random
import re
import scipy.stats
import time

# import numpy as np
# import matplotlib.pyplot as plt


from aiorun import run
from logzero import logger
from pyautogui import hotkey, press, typewrite
from num2words import num2words

RE_INTEGER_RANGE = r'[0-9]+\.\.\.[0-9]+'


def trunc_gauss_int(bottom, top):
    '''
    Generates a random integer following a personal gaussian distribution,
    using the mean of both values as mu, and 0.7 as the standard deviation
    whilst truncating values outside the range.
    '''
    lower = -1
    upper = 1
    mu = 0              # 422516lu
    sigma = 0.7

    total_possibilities = abs(top - bottom) / 2
    median_value = (bottom + top) / 2

    return int(median_value + (total_possibilities * scipy.stats.truncnorm.rvs((lower-mu)/sigma,(upper-mu)/sigma,loc=mu,scale=sigma,size=1)))

class AnswerWasAlreadyUsed(Exception):
    pass

class Main(object):
    def __init__(self, args):
        self.items = args.items
        self.ignore_spaces = args.ignore_spaces
        self.time_interval = float(args.time)
        self.write_for_extense = args.write_for_extense
        self.leading_zeroes = args.leading_zeroes
        self.diminishing_time = args.diminishing_time
        self.previous_checks = []
        self.start_time = time.time() - self.time_interval

        self.words = []
        with open(args.file, 'r') as file:
            for line in file:
                if not line.startswith('#') or not line.strip():
                    self.words.append(line.strip('\n '))

    def generate_random_word(self):
        return random.choice(self.words).casefold()

    def generate_random_number(self, full_range):
        try:
            first_number, last_number = str(full_range).split('...', 1)
        except:
            logger.error('I cannot understand what you mean with: ' + str(full_range))
            quit()
        else:
            first_number = min(int(first_number), int(last_number))
            last_number = max(int(first_number), int(last_number))

        if self.write_for_extense:
            return str(num2words(trunc_gauss_int(first_number, last_number))).replace('-', ' ').replace(',', '')
        if self.leading_zeroes:
            integer = trunc_gauss_int(first_number, last_number)
            ret_len = max(len(str(first_number)), len(str(last_number)))
            return str("{:0{precision}d}".format(integer, precision=ret_len))
        else:
            return str(trunc_gauss_int(first_number, last_number))

    async def compile_new_answer(self):
        while True:
            answer_items = []
            for item in self.items:
                if re.match(RE_INTEGER_RANGE, item):
                    answer_items.append(self.generate_random_number(item))
                elif item == '...':
                    answer_items.append(self.generate_random_word())
                else:
                    answer_items.append(item)

            if self.ignore_spaces:
                answer = ''.join(answer_items)
            else:
                answer = ' '.join(answer_items)

            # Bails out if answer was already used and it's on memory (so we don't have to load the file again)
            if answer in self.previous_checks:
                logger.error('Answer {} was already used before (memory)'.format(answer))
                continue

            # Otherwise load messages.log and check if anyone has sent an identical message before.
            # If so, bail out.
            with open('messages.log', 'r') as file:
                try:
                    for line in file:
                        if answer.casefold() == line.casefold().strip():
                            self.previous_checks.append(answer)
                            logger.error('Answer {} was already used before (file)'.format(answer))
                            raise Exception
                        # elif answer.casefold() in line.casefold():
                        #     self.previous_checks.append(answer)
                        #     logger.error('Answer {} was already used before, but partially (file)'.format(answer))
                        #     # print(answer, line)
                        #     # print(answer.casefold(), line.casefold())
                        #     raise Exception
                except:
                    continue

            logger.warning('Generated answer: ' + answer)
            self.previous_checks.append(answer)
            return answer

    async def send_answer(self, answer):
        hotkey('ctrl', 'a')
        typewrite(answer)
        hotkey('Enter')

    async def start(self):
        # while True:
        while True:
            # print(time.time() - self.start_time)
            if time.time() - self.start_time >= self.time_interval:
                # Get a brand new answer that wasn't used before
                self.start_time = time.time()
                answer = await self.compile_new_answer()
                await self.send_answer(answer)
                if self.diminishing_time and self.time_interval > 1.5:
                    self.time_interval = self.time_interval * 0.95


if __name__ == '__main__':
    def cmdline_args():
        p = argparse.ArgumentParser()

        p.add_argument('-f', '--file', help='File from where to pick answers.', default='answers.txt')
        p.add_argument('-x', '--write-for-extense', help='Write numbers for extense.', action='store_true')
        p.add_argument('-z', '--leading-zeroes', help='Keep leading zeroes', action='store_true')
        p.add_argument('-n', '--ignore-spaces', help='Ignore spaces between items (i.e.: "100...300 5" would output numbers from 1000 to 3000 ending in 5.', action='store_true')
        p.add_argument('-d', '--diminishing-time', help='Diminish [default = until 1.5s]', action='store_true')
        p.add_argument('-t', '--time', help='Minimum time to wait between each message (in seconds). Accepts floats. [default = 2]', default=2)
        p.add_argument('items', nargs='+', help='List of items to input. Use three dots (...) as a placeholder for a randomly chosen item.'
                       + ' If one item is of the format of int...int (e.g.: 1000...3000), then the script will fetch a'
                       + ' random integer between the two adjacent numbers.')

        res = p.parse_args()
        return res

    args = cmdline_args()
    asyncio.run(Main(args).start())
