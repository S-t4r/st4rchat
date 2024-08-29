# st4rchat
A real-time chat application

## Description:
- This project is kind of a social media. You can submit posts, like posts, follow others, and you can have private chats with other users. Posts are exactly the same as Network project. I will explain them one by one.

### Django:
	- So far this is the most powerfull tool that I have worked with. It was overwhelming at first, but as I worked through the projects I became more and more confortable. This framework has everything ready and is truly a DRY, you just need to have the knowledge of it to use its features.
	- I didn't have to worry about security at All. No SQL injection attacks, No XSS, and for Cross Site Request Forgery I just needed to include a csrf_token into my code.
	- In my opinion this framework is really flexable. After creating a few projects with it your next projects are mostly copy pasting from old applications to make new applications.
	- The most impressive feature is how models and forms work. I didn't need to worry about how my tables structure would look like, everything was in a nice and readable format.


### Channels framework:
	- The most significant feature of this application is 'Real-Time Communication' which at first seemed impossible for me, but the Duck introduced me to Channels framework. I read the docs and was totally confused at first, I still am, but I do have a little bit of understanding of how Channels work. Everytime a message is send it goes through a WebSocket and will be received by the consumer and the consumer will trigger an event for all the users in that particular chat room.

