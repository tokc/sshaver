#!/usr/bin/env python3

import curses
import time
import random


def weighted_choice(choice_array):
    """Return a random choice from a list of (choice, weight) tuples."""
    # The total represents 100% probability.
    total = sum(weight for choice, weight in choice_array)

    current_probability = 0
    random_number = random.uniform(0, total)

    for choice, weight in choice_array:
        current_probability += weight
        if (current_probability > random_number):
            return choice


class StringArray:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.length = self.get_length(width, height)
        self.array = [[" " for i in range(self.width)]
                        for j in range(self.height)]
        self.array2 = [[" " for i in range(self.width)]
                        for j in range(self.height)]
        self.array3 = [[" " for i in range(self.width)]
                        for j in range(self.height)]

        self.flipflop = True

    def get_length(self, width, height):
        return (width * height) - 1

    def adjust_resolution(self, width, height):
        if (width, height) != (self.width, self.height):
            width_difference = abs(self.width - width)
            height_difference = abs(self.height - height)

            if width < self.width:
                for array in [self.array, self.array2, self.array3]:
                    for i in range(len(array)):
                        array[i] = array[i][:-width_difference]

            elif width > self.width:
                for array in [self.array, self.array2, self.array3]:
                    for i in range(len(array)):
                        array[i].extend([" " for i in range(width_difference)])

            if height < self.height:
                self.array = self.array[:-height_difference]
                self.array2 = self.array2[:-height_difference]
                self.array3 = self.array3[:-height_difference]

            elif height > self.height:
                self.array.extend([[" " for i in range(width)]
                                    for j in range(height_difference)])
                self.array2.extend([[" " for i in range(width)]
                                    for j in range(height_difference)])
                self.array3.extend([[" " for i in range(width)]
                                    for j in range(height_difference)])

            self.width = width
            self.height = height
            self.length = self.get_length(width, height)

    def scroll_starfield(self, string_array, weighted_stars, scroll_speed):
        """Remove the left-most character from each row,
           and append a character to the right."""

        for row in string_array:
            del row[0:scroll_speed]
            for i in range(scroll_speed):
                row.append(weighted_choice(weighted_stars))

        return string_array

    def update(self, width, height):
        self.adjust_resolution(width, height)

        self.array = self.scroll_starfield(self.array,
                                            [(" ", 100), (".", 1)], 1)
        self.array2 = self.scroll_starfield(self.array2,
                                            [(" ", 100), ("+", 1)], 2)
        self.array3 = self.scroll_starfield(self.array3,
                                            [(" ", 100), ("*", 1)], 3)

    def get_string(self):
        # Flatten each layer to a 1D array.
        top_array = [character for row in self.array3 for character in row]
        middle_array = [character for row in self.array2 for character in row]
        bottom_array = [character for row in self.array for character in row]

        # If the space in the layer above if empty, fill it up.
        for i in range(self.length - 1):
            if top_array[i] == " ":
                top_array[i] = middle_array[i]
        for i in range(self.length - 1):
            if top_array[i] == " ":
                top_array[i] = bottom_array[i]
        top_array.pop()
        return "".join(top_array)


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    starfield = StringArray(width, height)

    stdscr.refresh()
    while True:
        height, width = stdscr.getmaxyx()
        starfield.update(width, height)
        stdscr.addstr(0, 0, starfield.get_string())
        stdscr.refresh()
        time.sleep(1)


# Wrapper stops the terminal from going all goofy if we crash.
curses.wrapper(main)
