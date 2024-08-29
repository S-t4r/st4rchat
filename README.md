# st4rchat
A real-time chat application with sentiment values.

## Description:
- This project is kind of a social media. You can submit posts, like posts, follow others, and you can have private chats with other users and in your chat the messages you send are measured for their meaning (good or bad) which comes in three forms, green, red, and gray. Posts are exactly the same as Network project one difference is that I added a delete button for each post. I will explain them one by one.
- Chat messages are analyzed on their sentiment(positive, negative, natural) and displayed with different colors based on their **Sentiment Analysis**.
- A user who is not registered is able to see the messages, but cannot post a message themselves.

- ###### Sentiment Value:
	- Sentiment analysis is the process of determining the emotional tone behind a piece of text.
	- The sentiment analysis would analyze messages in real-time to provide feedback on the emotional tone of the conversation.

### Django:
	- So far this is the most powerfull tool that I have worked with. It was overwhelming at first, but as I worked through the projects I became more and more confortable. This framework has everything ready and is truly a DRY, you just need to have the knowledge of it to use its features.
	- I didn't have to worry about security at All. No SQL injection attacks, No XSS, and for Cross Site Request Forgery I just needed to include a csrf_token into my code.
	- In my opinion this framework is really flexable. After creating a few projects with it your next projects are mostly copy pasting from old applications to make new applications.
	- The most impressive feature is how models and forms work. I didn't need to worry about how my tables structure would look like, everything was in a nice and readable format.
	- ##### Register, Login, Logout:
		- Brian did me a favor by providing me with the necessary components by which a User could register, login, or logout. So everytime I needed to use these functions in my applications I just copied them from previous applications.

### Channels framework:
	- The most significant feature of this application is 'Real-Time Communication' which at first seemed impossible for me, but the Duck introduced me to 'Channels' framework. I read the docs and was totally confused at first, I still am, but I do have a little bit of understanding of how Channels work. Everytime a message is send it goes through a WebSocket and will be received by the consumer and the consumer will trigger an event for all the users in that particular chat room.
	- Routing.py defines how a WebSocket connection is routed to different consumers based on URL patterns, kinda like urls.py, But I think it is mostly used to define WebSocket routing.
	- consumers.py is similar to views.py the difference is, consumers.py is used for WebSockets. In consumers.py we define a consumer class that can handle WebSocket events. It can handle new WebSocket connections or disconnections and handle incoming messages.
	
#### To be honest...
	- To be honest I didn't work as hard as I did on CS50x's final project. It seemed like an easy task. I didn't work on styling my pages, and I know that I also have to be a good designer, but I could learn that later. For now I'm more intrested on logics behind the applications, the main ideas and ways to solve problems.
	- I hope this project is acceptable.
	
Best Regards, Matin.
