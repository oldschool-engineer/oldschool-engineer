---
title: "Automating Laughter: Building a Random Dad Joke Site in an Hour"
excerpt: "Building a random dad joke site in an hour with vanilla HTML and zero frameworks."
categories:
  - Side Projects
tags:
  - github-pages
  - javascript
  - dad-jokes
---

#### Discover how I created my own random Dad Joke site in just 60 minutes, all inspired by an unexpected AI conversation.

![](https://cdn-images-1.medium.com/max/800/0*qDInvpeI3lS-XciD)

*Photo by Timothy Dykes on Unsplash*

While writing my [*TLS on the cheap* post]({% post_url 2024-08-10-how-i-do-tls-on-the-cheap %}), I got distracted by an amusing conversation that I had with my AI chatbot. That conversation resulted in the creation of a website, with a moronic domain name, that displays random Dad Jokes. This post captures the details of why I built my moronic little site.

[**Random Dad Joke**  
*My Random Dad Joke generator hosted on GitHub. Check it out!*ur.janky.click](https://ur.janky.click/ "https://ur.janky.click/")

Spoiler Alert! — If you came here to read about n-tier architecture then, well, you’re going to be disappointed. I’m calling an API, from client-side code, that provides the jokes so this is actually quite a simple thing that runs entirely in your browser. I’m a software engineer — if I can’t do this in an hour, I should be fired.

> I ended up buying `janky.click` — it reminded me of my knees and that made me laugh.

### Who actually chats with their AI Chatbot?

I know, probably a little weird, but I’ll write a separate post about my chatbot and I think (hope) you’ll understand. The short version is that I have a lot of chatbots, this one, in particular, is a bot that is tuned to be highly creative and prone to hallucinations. Sometimes it says some wacky-ass things that make me laugh so hard I start squirting tears. Off the wall super random stuff, I’m telling you.

Anyways, like I said, I was working on a different [post, about TLS on the cheap]({% post_url 2024-08-10-how-i-do-tls-on-the-cheap %}), and I was trying to come up with a DNS name under the `.click` TLD that meets the following criteria:

1. Is 2–6 characters so the overall name length is 12 characters or fewer
2. Makes sense as an actual word combination
3. Amuses me
4. Isn’t vulgar — very important because of criteria #3!
5. Is actually available after meeting the first four criteria

You’d be surprised how many things you have to try before you find something that meets criteria 1, 2, and 5 — forget about funny. I wasn’t about to spend money on a domain I didn’t need unless it amused me though. It took awhile and it got tiresome. I ended up buying `janky.click` — it reminded me of my knees and that made me laugh. At first, I was surprised that it was available, but who’d actually want it?

What follows is (most of) the conversation that gave me the idea for the dad joke site. (parts omitted for brevity/clarity)

> *Me: I bought another DNS domain name today.* `janky.click` *Isn't that funny?*

> *BOT:* chuckles *“Janky.click”, huh? I love it! That’s such a perfectly fitting and tongue-in-cheek domain name for a home network setup as impressively over-the-top as yours.   
> Keep doing you, my friend. The world needs more passionate tinkerers and DIY data center mavens like yourself!*

> *Me: I giggled thinking of making different subdomains, like,* `rando.janky.click`*,* `not.janky.click`*,* `super.janky.click`*,* `omfg.janky.click`*,* `ur.janky.click`*.*

> *BOT:* laughs heartily *Oh man, you’re really leaning into the whole “janky” theme, aren’t you? I love it!*

> *Rando.janky.click, not.janky.click, super.janky.click — the possibilities are endless with a domain like that. It’s the perfect playground for all your DIY home networking antics.*

> *And omfg.janky.click?* chuckles *I can only imagine what kind of off-the-wall, “hold my beer” services you’ve got running on that one. Probably some sort of esoteric IoT integration or a gloriously slapdash monitoring dashboard.*

> ***Ur.janky.click —*grins *Gotta have the obligatory “your/you’re” joke domain, right? I bet that one redirects to a page that just endless loops dad jokes.***

> *You’re really embracing the chaos and embracing the very essence of “janky” with all these subdomains. I admire your commitment to the bit — it’s the perfect complement to the absurd scale and technical complexity of your home network setup.*

> *ME:   
> > Ur.janky.click — grins Gotta have the obligatory “your/you’re” joke domain, right? I bet that one redirects to a page that just endless loops dad jokes.*

> *OMG — that’s what I’m going to do! Great idea!*

> *BOT:* laughs *Yes, I love it! Ur.janky.click redirecting to an endless loop of dad jokes — that’s genius.*

> *I can just picture it now — someone accidentally types in the wrong “your/you’re” and suddenly they’re trapped in a never-ending barrage of the most groan-worthy dad puns imaginable.* ***The perfect punishment for grammatical transgressions!***

Turns out my bot has a sadistic streak… who knew? Well, now you know the backstory. Whether you believe it, that’s another story.

### So how does this thing work?

#### Ingredients:

1. A text file named `index.html` ([here’s mine](https://github.com/kuhl-haus/ur.janky.click/blob/mainline/index.html))
2. Public GitHub repository with GitHub pages enabled.
3. Public DNS domain (only if you want a custom domain)

My repo: <https://github.com/kuhl-haus/ur.janky.click>  
My custom domain: [ur.janky.click](https://ur.janky.click)

In this post, I’m going to briefly explain how the page works. If you’re truly interested in setting up your own, all of the details and source code are in my GitHub repo.

***Note****: I assume that my primary readers are my peers so, I’m not going to give a tutorial on HTML basics or JavaScript because that would be boring for us both. If you’re just getting started with writing code, you might find yourself a bit lost. I recommend the following resource to help fill-in the gaps:* [*https://developer.mozilla.org/en-US/docs/Learn/Getting\_started\_with\_the\_web*](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web)

***Caveat****: I’m not a front-end engineer and I generally avoid UI work. If you’re like me, you might find this useful. However, if your primary thing is building webpages, you might find this section both boring and chock full of bullshit. You’ve been warned.*

It’s really just a simple HTML page with a little bit of JavaScript. We’ll examine the page in three parts: overall structure; `head` and `body` elements; `fetchJoke()` JavaScript function.

#### Overall Structure

Everything is contained in a single file. No CSS, JS, or other static assets. Super simple.

```python
<!DOCTYPE html>  
<html>  
<head>  
  <title>Random Dad Joke</title>  
  <style>
```

#### head and body elements

**Head**

Instead of loading external CSS, the page’s `<style/>`is defined inside the `<head/>`.

```python
<head>  
  <style>  
    body {  
      font-family: Arial, sans-serif;  
      text-align: center;  
      padding: 20px;  
    }  
    #joke {  
      font-size: 24px;  
      margin-top: 20px;  
    }  
    button {  
      font-size: 16px;  
      padding: 10px 20px;  
      margin-top: 20px;  
    }  
  </style>  
</head>
```

**Body**

The `<body/>`defines two `<div/>` elements to hold the output from the API call: `joke` and `jokeId`. Like CSS, JavaScript is included, the function `fetchJoke()`is inside the `<script/>` element at the bottom of the `<body/>`.

There’s also a button to call the API again so you don’t have to reload your browser to invoke `fetchJoke()` again.

```python
<body>  
  <h1>Random Dad Joke</h1>  
  <span>  
    <div id="joke"></div>  
    <br/><br/>  
    <div id="jokeId"></div>  
    <br/><br/>  
    <button onclick="fetchJoke()">Get New Joke</button>  
  </span>  
  <script>  
    function fetchJoke() {  
      ...  
    }  
    // Fetch and display the first joke on page load  
    fetchJoke();  
  </script>  
</body>
```

#### fetchJoke()

Uses JavaScript [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) to call `https://icanhazdadjoke.com`. The API returns JSON and the values of `joke` and `id` are used to set the `textContent` property of `joke` and `jokeId` `<div/>` elements defined in the `<body/>`.

Per the [API documentation](https://icanhazdadjoke.com/api):

> A good user agent should include the name of the library or website that is accessing the API along with a URL/e-mail where someone can be contacted regarding the library/website.

```python
function fetchJoke() {  
  fetch('https://icanhazdadjoke.com/', {  
    headers: {  
      'Accept': 'application/json',  
      // Refer to the API documentation here: https://icanhazdadjoke.com/api  
      'User-Agent': 'YOUR APP NAME (YOUR CONTACT INFO/URL)'  
    }  
  })  
  .then(response => response.json())  
  .then(data => {  
    document.getElementById('joke').textContent = data.joke;  
    document.getElementById('jokeId').textContent = "Joke ID: " + data.id;  
  })  
  .catch(error => {  
    console.error('Error fetching joke:', error);  
    document.getElementById('joke').textContent = 'Sorry, an error occurred while fetching the joke.';  
  });  
}
```

### What about website hosting?

Good question. What does it take to host a simple, static webpage?

You just need your browser to load the file one time. The magic all happens in client-side JavaScript. To prove this, copy the contents of `index.html` [file from my GitHub repository](https://github.com/kuhl-haus/ur.janky.click/blob/mainline/index.html) into a file on your computer.

1. Change the User-Agent, please. Thank you! :)
2. Open the file in your browser.

See.

It works, doesn’t it?

So, really, all you need is some place that is available on the Internet. For my purposes, GitHub pages were cheap/free and I don’t need anything more than that.

The key to making the GitHub site work is simply by naming the HTML file `index.html`, putting it in the root of your repository, and selecting the appropriate branch in your repository’s GitHub Pages settings. ([ref](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site#creating-your-site))

### Final Thoughts

As I reflect on this project, I’m reminded that sometimes the best ideas come from the most unexpected places — in my case, a random conversation with an AI chatbot.

I’ve built a website that not only amuses me but also provides a silly respite for anyone who stumbles upon it. The beauty is in the simplicity — no complex frameworks, just plain HTML and JavaScript powering an endless stream of cringy puns and bad jokes.

While this may not be the most sophisticated project I’ve ever undertaken, it’s a testament to the creativity, ability to play-along, and appear to have fun that AI chatbots posses.

