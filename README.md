This is a script that solves the daily set puzzle on http://www.setgame.com/set/puzzle


In order to understand this script, one must first become familiar with the game of "Set".

In "Set", there are four attributes: Shape, Color, Number, and Shade.  For each attribute, there are 3 variations. There is a deck of 81 cards, each of which contains a unique combination of the aforementioned attributes.

For the card below, the Shape is "Diamond", the Color is "Red", the Number is "One", and the Shade is "Solid".  A more simple notation for this can be [Diamond, Red, One, Solid]

![image](https://user-images.githubusercontent.com/92408910/222538393-5a11a0f6-7668-4d49-9333-b3840b094774.png)

The goal of the game us to find three cards that create a SET.  In order for three cards to be considered a SET, they need to be either the SAME, or DIFFERENT, for each of the four attributes.

For example, the three cards below create a SET.

![image](https://user-images.githubusercontent.com/92408910/222541622-a013435a-410e-47b7-aff8-35834a27ad60.png) ![image](https://user-images.githubusercontent.com/92408910/222541543-3718210c-9c18-45df-b066-acdf0f44f816.png) ![image](https://user-images.githubusercontent.com/92408910/222541687-08f873a1-dcd6-4d53-9927-0578d034e5d5.png)

This is due to the fact that they all have:

A DIFFERENT Shape (Diamond, Squiggle, Oval)

The SAME Number (One)

The SAME Color (Red)

A DIFFERENT Shade (Solid, Shaded, Hollow)
