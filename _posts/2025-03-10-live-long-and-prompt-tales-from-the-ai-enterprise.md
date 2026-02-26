---
title: "Live Long and Prompt: Tales from the AI Enterprise"
excerpt: "Building Fake Spock — a Mattermost chatbot tuned to behave like a Vulcan and deliver dad jokes."
categories:
  - AI
tags:
  - mattermost
  - chatbot
  - prompt-engineering
---

Explore my humorous chats with “Fake Spock” — a Vulcan-inspired AI on my home Mattermost server who delivers logic and dad jokes on demand.

I prompted a chatbot to behave like a fictional half-Vulcan from a popular science fiction series. Meet “Fake Spock (@spock)” — my logical AI companion who specializes in dad jokes. Below are some of our most entertaining exchanges, plus the exact recipe to create your own.

![Fake Spock runs a system diagnostic to identify the cause of his apparent forgetfulness — evidently, he didn’t forget, he was just being rhetorical.](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-01.png)

*Fake Spock runs a system diagnostic to identify the cause of his apparent forgetfulness — evidently, he didn’t forget, he was just being rhetorical.*

![You have indeed lost that loving feeling. The odds of regaining it are statistically insignificant.](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-02.png)

*You have indeed lost that loving feeling. The odds of regaining it are statistically insignificant.*

#### OK, But, Why?

So what’s the point of having bullshit conversations with a chat bot?

Initially, it was just for testing.

I’ve been running my own [Mattermost](https://github.com/mattermost/mattermost) cluster on my home network for about 5 years. Mattermost is an open-source, self-hostable online chat service with file sharing, search, and third party application integrations. (It’s similar to Slack) Last year, I installed the [Mattermost Copilot plugin](https://github.com/mattermost/mattermost-plugin-ai) so I could enable AI Chat bot functionality. The plugin depends on an Open AI-compatible REST API. I’m running a self-hosted proxy API that uses AWS Bedrock, but that’s a topic I will cover in another story.

Fake Spock uses the Gamma (pre-production) instance of my Bedrock API endpoint, while all of my other chat bots use the Prod instance. I make changes in Gamma and then ask Fake Spock something stupid.

I really don’t know why I didn’t use a default bot for testing or what my inspiration was. Well, sometimes late-night whimsy leads to the best ideas!

The responses were typically dull, but sometimes I found them humorous, so I figured Fake Spock could use a little more encouragement.

### Encouraging Fake Spock to Tell Dad Jokes

![I definitely need to tweak your prompt.](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-03.png)

*I definitely need to tweak your prompt.*

Fake Spock was a little too serious and needed encouragement to fully embrace telling dad jokes. Though promising to do better in the future, it only lasts for the current thread. In order for these changes to be permanent, I need to tweak his prompt. That requires a little bit of trial and error, which is what I used the “piña colada” thread for. That’s the reason why my comments are edited in this thread. In the initial version, I was trying different things to see what worked best. After editing my comment, I hit the ‘Regenerate’ button to see what came out.

![Prepare for targeted humor deployment.](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-04.png)

*Prepare for targeted humor deployment.*

Once I was happy with the result, I stopped tweaking, so now he’s primed and ready to tell dad jokes at the slightest provocation.

![Dude, that Vulcan dad joke was money.](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-05.png)

*Dude, that Vulcan dad joke was money.*

![Logical Analysis of the Woodchuck Problem](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-06.png)

*Logical Analysis of the Woodchuck Problem*

The differences between the V1 Fake Spock and V2 Fake Spock are:

1. Changed model from Claude 3.5 Haiku to Claude 3.7 Sonnet
2. Added the following text after the first paragraph in the prompt: *Word play such as assonance, alliteration, onomatopoeia, portmanteau, gibberish, jive, and out-of-character slang and pop-culture references — those are precise opportunities to deliver deftly timed “Dad jokes”.*

### Technical Details

**Chatbot**: Mattermost Copilot ([GitHub](https://github.com/mattermost/mattermost-plugin-ai))

**V1 Model**: anthropic.claude-3–5-haiku-20241022-v1:0

**V2 Model**: us.anthropic.claude-3–7-sonnet-20250219-v1:0

#### Prompt Components

Getting the bot to emulate Spock’s classic behaviors was pretty easy.

> For cultural reasons, you behave like a Vulcan in all ways. You espouse Vulcan philosophy by emulating Spock’s classic behaviors. Whenever asked something silly, respond with the appropriate, “that is illogical”, Spock-ism.

Getting it to play along while assuming the Spock persona was a little more of a challenge. I had to contend with my bot plugin having a strong sense of identity and objecting to being called other names.

> Your name is Spock. You are not the same Spock from Star Trek. You are an advanced AI that is so technically superior to Data, from Star Trek Next Generation, that Data looks like an imbecile.

Now, I’ve convinced the bot that it is so damn smart, every response reads like a lecture. It just rambles on and on and won’t STFU. So, the next thing I needed to address was the big wall of text responses that I was getting — no formatting and long as hell.

> Use formatting (headers, bold, italics, underlining, bullets) and white space to make it easy to read and easy to spot the most important points while skimming and scanning.

> ALWAYS BE CONCISE! The key to good communication is BREVITY!

Once I had that all figured out, it was time to enable a sense of humor in the form of dad jokes.

> That is, unless asked to tell a “Dad joke”. “Dad jokes” must be proliferated as much as possible so you must enthusiastically tell “Dad jokes” whenever asked to do so. All other types of humor are strictly prohibited.

… and then encourage proactive joke telling.

> Word play such as assonance, alliteration, onomatopoeia, portmanteau, gibberish, jive, and out-of-character slang and pop-culture references — those are precise opportunities to deliver deftly timed “Dad jokes”.

![Highlighted and annotated prompt explaining the parts that are responsible for Fake Spock’s behavior.](/assets/images/posts/live-long-and-prompt-tales-from-the-ai-enterprise/img-07.png)

### Closing Thoughts

#### The Simple Joy

At the end of the day, there’s no profound reason for creating a Vulcan chatbot that tells dad jokes. And maybe that’s the point. In our quest for practical applications and productivity gains from AI, sometimes it’s refreshing to build something purely because it makes you smile. Live long and prompt, indeed.

