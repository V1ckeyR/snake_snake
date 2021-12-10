# Design Document

## Context and scope 🐍

People love to play mini-games on their browsers. You will probably find browser-based games on almost every genre from FPS, RPG, Arcade, to city building, war games, and so on. I would like to make my own variant of the famous Snake game with the opportunity to play with other people.

## Goals and non-goals 🐍

### Goals 🐍
* Invent game algorithm
* Create game server
* Create adaptive website prototype
* Create game client
* Compose all parts with websockets

### Non-goals 🐍
* Rooms for private games
* Authorization
* Chats

## The actual design 🐍

A dynamic game hosted on a website assumes a Client-Server architecture using websockets that allow server and client to communicate in real time. Server will be written in Python, Client in JS.

The game is multiplayer, which means that the MVC architecture (model-view-controller) will be used. Logical part has to be processed on the server, and all the Client has to do is send user input to the server and display the information it receives from the server.
Clients should only send information about their intentions to the server, which will then be processed and used to change the state of the players if they are valid.

### System-context-diagram 🐍

### APIs 🐍

### Data storage 🐍

### Degree of constraint

1. No full screen mode
2. Only WASD to control snake
3. No music
4. No super cool graphic (Only HTML and CSS)
5. No super cool animations (Only CSS and JS)
6. No gamepad mode
7. No text/voice chats

## Alternatives considered 🐍 

Technology for browser-based Python game development:
1. Full Screen API – If you want your browser game to run over the entire screen.

2. Gamepad API – For providing gamepads or other game controllers support to your browser game.

3. Web Audio API – Games without audio are pretty dull, and no one would like to play it. Use Web Audio API for controlling playback and manipulation of audio from JS code. You can add cool sound effects and apply them in real-time.

4. HTML and CSS – Most important to learn if you want to build your own browser game. Using HTML and CSS, you can design the interface of your browser game. <canvas> HTML tag provides an easy way to do 2D graphics.

5. JavaScript – Modern-day programming language of the web, which is fast. Using it, you can apply Python logic from the backend to control the gameplay.

6. HTML Audio – If you only require basic audio for your browser game, then you can simply apply the <audio> HTML element.

7. WebGL – Create high-performance and hardware-accelerated 3D and 2D graphics from web content.

8. WebRTC – WebRTC or Web Real-Time Communications API supports the transfer of video and audio data, including teleconferencing back and forth between multiple users. So, if you want to build an online multiplayer game and allow players to talk with each other while they are busy killing zombies, then this is the API for you.

9. WebSockets – Connect your browser game to the server and facilitate real-time data transfer to support gameplay actions, chat services, and so on.

10. Web Workers – Take advantage of modern-day multicore processors using Web Workers. Spawn background game threads running their own JS code to enhance the performance of your Python-based online game.

11. Pointer Lock API – Get exact coordinates of your user’s cursor to do accurate measurements of what players are doing in the game.

## Cross-cutting concerns 🐍 
  
The security and privacy issues are not prioritized because of following considerations:

  * The system will have limited number of users (max 7)
  * No user information will be stored
  * Developing a complex security system would require an unreasonably large amount of time and effort
  * Developing a private game rooms is excellent idea, but it would require a security system

