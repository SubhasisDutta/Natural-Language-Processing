# Dependency
Install stopwords and wordnet by using the nltk downloader. Use setup.py if required.
```
> python setup.py
```

# Run

## Help
```
> python Main.py -help
> usage: Main.py [-h] [-word WORD] [-sentense SENTENSE]
```
To run:
```
> python Main.py -word "like" -sentence "Time flies like an arrow"
```

#Report

Sentence : Time flies like an arrow  
## Positive Results

1. Word : Time
```
> python Main.py -word "Time" -sentence "Time flies like an arrow"
WORD:  Time
SYNSET:  Synset('time.n.05')
DEFINATION:  the continuum of experience in which events pass from the future through the present to the past
EXAMPLE:  []
```

2. Word : like
```
> python Main.py -word "like" -sentence "Time flies like an arrow"
WORD:  like
SYNSET:  Synset('like.a.01')
DEFINATION:  resembling or similar; having the same or some of the same characteristics; often used in combination
EXAMPLE:  [u'suits of like design', u'a limited circle of like minds',
 u'members of the cat family have like dispositions',
  u'as like as two peas in a pod', u'doglike devotion', u'a dreamlike quality']
```

## Negative Result

1. Word : flies
```
> python Main.py -word "flies" -sentence "Time flies like an arrow"
WORD:  flies
SYNSET:  Synset('fly.n.03')
DEFINATION:  an opening in a garment that is closed by a zipper or by buttons concealed under a fold of cloth
EXAMPLE:  []
```




