data = [
# Positive (1)
"I love this product",
"This is amazing",
"Fantastic experience",
"Very good service",
"Absolutely great",
"I really enjoyed this",
"Highly recommend it",
"This works perfectly",
"Super happy with this",
"Exceeded my expectations",
"I’m very satisfied",
"Brilliant quality",
"Really liked it",
"This is awesome",
"Great value for money",
"Loved every bit of it",
"Very impressive",
"This made my day",
"Pretty good overall",
"I would buy this again",

# Negative (0)
"I hate this",
"Terrible product",
"Worst experience ever",
"Very bad",
"Extremely disappointing",
"Not worth the money",
"I regret buying this",
"Awful quality",
"This is horrible",
"Completely useless",
"Very frustrating",
"I’m not happy with this",
"Total waste",
"Bad experience overall",
"Poor performance",
"This broke quickly",
"Really bad service",
"I dislike this",
"This is the worst",
"Highly disappointing",

# Neutral / Mixed (hard cases)
"It was okay",
"Not bad but not great",
"Could be better",
"I don't like it much",
"I kinda enjoyed it",
"This was disappointing",
"Not the worst experience",
"Pretty decent overall",
"It’s fine",
"Average experience",
"Nothing special",
"It works but has issues",
"I expected better",
"Not great, not terrible",
"It’s acceptable",
"Some parts were good",
"I have mixed feelings",
"It’s alright I guess",
"Could be worse",
"Not impressed",

# Slight positive
"I kinda like it",
"It’s actually pretty good",
"I enjoyed it a bit",
"This is not bad",
"Better than expected",
"I like this overall",
"Quite nice",
"This turned out good",
"I’m happy enough",
"Works well for me",

# Slight negative
"This is not very good",
"I wouldn’t recommend it",
"It has many issues",
"Not satisfied",
"Could have been better",
"I’m a bit disappointed",
"Not as expected",
"It didn’t work well",
"I’m not impressed",
"This needs improvement"
]

labels = (
    [1]*20 +   # positive
    [0]*20 +   # negative
    [0]*20 +   # neutral/mixed (lean negative)
    [1]*10 +   # slight positive
    [0]*10     # slight negative
)