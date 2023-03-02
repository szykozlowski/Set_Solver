# Overview

This is a script that solves the daily set puzzle on http://www.setgame.com/set/puzzle.  While far from the fastest way of doing this, I thought that using image recognition would be much more interesting than simply scraping the metadata of the cards from the website.  Using this method also makes the script far more versatile, as it isn't bound to a single website.  With some slight modification it could solve Set puzzles on any website, or even in the physical card game itself. 

## Rules of Set

In order to understand this script, one must first become familiar with the game of "Set".

### Attributes

In "Set", there are four attributes: Shape, Color, Number, and Shade.  For each attribute, there are 3 variations.  These are as follow:

Shape: [Diamond, Oval, Squiggle]

Color: [Red, Green, Purple]

Number: [One, Two, Three]

Shade: [Solid, Hollow, Shaded]

There is a deck of 81 cards, each of which contains a unique combination of the aforementioned attributes.  

### Example

For the card below, the Shape is "Diamond", the Color is "Red", the Number is "One", and the Shade is "Solid".  A more simple notation for this can be [Diamond, Red, One, Solid]

![image](https://user-images.githubusercontent.com/92408910/222538393-5a11a0f6-7668-4d49-9333-b3840b094774.png)

### What Creates a Set?

The goal of the game us to find three cards that create a SET.  In order for three cards to be considered a SET, they need to be either the SAME, or DIFFERENT, for each of the four attributes.

### Example

The three cards below create a SET.

![image](https://user-images.githubusercontent.com/92408910/222541622-a013435a-410e-47b7-aff8-35834a27ad60.png) ![image](https://user-images.githubusercontent.com/92408910/222541543-3718210c-9c18-45df-b066-acdf0f44f816.png) ![image](https://user-images.githubusercontent.com/92408910/222541687-08f873a1-dcd6-4d53-9927-0578d034e5d5.png)

This is due to the fact that they all have:

A DIFFERENT Shape (Diamond, Squiggle, Oval)

The SAME Number (One)

The SAME Color (Red)

A DIFFERENT Shade (Solid, Shaded, Hollow)

# How it Works

The script works through utilzing OpenCV contours to identify the shapes present on the daily set puzzle, and translating that into input through Chrome Selenium.

## Identifying the Attributes of the Card

The script needs to identify the Four attributes of every card.  Below, I will describe how each of the four attributes is detected.

### Shape

In order to identify the shape the script uses the OpenCV "matchShapes()" function, which compares the unknown shape, to an example of a known shape.  If the coefficient of similarity is below a certain threshold, the shape is identified.

### Color

In order to identify the color, RGB bounds for the three colors are established.  If the amount of pixels in the card that fall into that RGB threshold is a non-zero value, the color is identified.

### Number

In order to identify the number, the largest contour in the image is identified by area.  Since the largest contour will always be the shape, the area of that contour is compared to the other contours in the card.  The amount of contours that have a similar area to the largest contour is equivelent to the number of shapes on the card, meaning the number is identified.

### Shade

In order to find the shade, I utilized a correlation between the number of contours in the image, and the previously determined number of shapes in the image.  If the total number of contours in the image is equivelent to the number of shapes, the card is Solid.  If the number of contours is double that of the number of shapes, the card is Hollow.  Finally, if the number of contours is greater than double the number of shapes, the card is deemed to be Shaded.

## Determining if Three Cards Create a Set

This becomes far easier if we assign a number from 0-2 to every variation of an attribute.  For example: we can assign "Diamond" with "0", "Squiggle" with "1", and "Oval" with "2".  If the sum of these numbers is divisible by 3, the attribute is either the same, or different between the set of cards.  
