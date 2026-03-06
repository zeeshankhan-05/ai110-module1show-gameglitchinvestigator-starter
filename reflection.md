# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, it appeared to load correctly in the browser, but it became clear quickly that the core logic was broken in multiple ways. The first bug I noticed was that the secret number was not being generated within the intended range of 1 to 100 — it was producing numbers outside that range, which broke the game's premise entirely. The second bug was that the hint logic was inverted: no matter what I guessed, the feedback was always the opposite of what it should have been, so guessing too high would say "Too Low" and vice versa. A third issue was that once the game ended, it would not properly reset — submitting a new guess after a win or loss still showed the end-game message instead of starting fresh.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used GitHub Copilot (Agent mode and Inline Chat) along with Gemini as my primary AI tools on this project. One correct suggestion the AI gave me was to refactor all four logic functions (check_guess, parse_guess, get_range_for_difficulty, update_score) out of app.py and into logic_utils.py to separate the game logic from the Streamlit UI code. I verified this by running pytest on the test suite, which confirmed all 15 tests passed, and by launching the Streamlit app to confirm the game still worked end-to-end. One misleading suggestion was when the AI initially kept the original starter code's TypeError fallback in check_guess that converted the secret to a string for comparison on even attempts. This was actually a hidden bug in the original code, not a safety feature, and it caused the hint logic to sometimes compare an integer guess against a string secret, giving wrong results. I caught it by reading the diff carefully and noticing the str() cast made no sense in a number-guessing game, then confirmed by testing guesses on both even and odd attempts.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by using two methods: automated pytest tests and manual testing in the live Streamlit app. For the inverted hints bug, I wrote two specific pytest cases — one that checks a guess of 60 against a secret of 50 and asserts the message contains "LOWER" (not "HIGHER"), and another that checks a guess of 40 against 50 and asserts the message contains "HIGHER" (not "LOWER"). Both passed, which told me the hint direction was now correct. For the difficulty range bug, I wrote a test asserting that Hard mode's upper bound is larger than Normal's, which confirmed Hard is now genuinely harder. I also ran the app with streamlit run app.py, used the Developer Debug Info panel to peek at the secret number, entered a guess higher than the secret, and confirmed the hint said "Too high — go LOWER!" on screen. The AI helped me design the tests by suggesting the structure of targeted assertions — checking not just the outcome string but also the content of the message string to make sure the player-facing hints were correct.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
