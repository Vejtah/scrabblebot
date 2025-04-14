# documentation #
>In this document is detailed documentation about my project.

## Idea ##
I was playing scrabble when i realised, that the game could be played against a bot and that it wouldnt be even that dificult.
I wanted to build a bot that will be capable of moving its playing pieces to the optimal position on the board.

## Brake down the process ##
The Idea of artifitally playing scrabble needs to be broken down to the most basic components. You have to think what you yourself do when you play scrabble and transform theese processes to a bot.

playing Scrabble as a human:
1) Look at the board
2) Evaluate the letters that you can use
3) Think of the best move
4) Move the tiles to build the word

If you want to build a bot with theese abilities, you can split the process to theese capabilites:
1) Way of knowing what tiles are already on the board
2) To know what letters you can choose from
3) Algorithm to decide on the best move
4) Move the tiles to the chosen position

## 1 + 2: Board ##
to even start playing scrabble you need a board and tiles. I decides on tile dimentions of 20mm x 30mm and the board to be 15 x 10 tiles to make a square. This board size is enough to play a game of scrabble and also not too big for it to be difficult to build a bot of this size.
>
To get the letters you will need a way of transforming real objets to strings (letters in programs). I decided on using a camera maounted on the top of the bot.
> For my camera i calculated, that i will need to position the camera atleast 700mm above the board.
>
I also will need a way of connecting electronics. I decided on using my Raspberry Pi 4 model B, mainly because i already owned it and there are ways to process images and moving servos and other kind of motors using accestories compatible with Raspberry Pi.

