import numpy as np
from functools import cached_property
import pandas as pd
from sentence_transformers import SentenceTransformer
class TextAnalyzer:
    def __init__(self,sen:str):
        self._sen = sen 
        self._word_list = self._splitter_trimmer() if isinstance(self._sen,str) else []

    def _splitter_trimmer(self)->list:
        words = self._sen.split()
        return [word.lower().strip('!@#$%^&*()_-+=./?,') for word in words]
    @property
    def words(self)->list:
       return self._word_list.copy()
    @cached_property
    def word_lengths(self)->np.ndarray:
       return np.array([len(word) for word in self._word_list])

    def word_count(self)->int:
        return len(self._word_list)

    def _build_counter(self)->dict:
       counter = {} 
       for word in self._word_list:
        counter[word] = counter.get(word,0)+1
       return counter
    
    @cached_property
    def _counter(self):
      return self._build_counter()
  
    def most_frequent_word(self)->dict:
       counter = self._counter
       if not counter:
          return {'most_frequent_word':None,'most_frequent_count':0}
       freq_word = max(counter,key=counter.get)
       freq_word_count = counter.get(freq_word) 
       return {'most_frequent_word':freq_word,'most_frequent_count':freq_word_count}


    def first_non_repeat(self)->str|None:
       counter=self._counter
       for word in self._word_list:
        if counter[word]==1:
            return word 
       return None

    def group_by_frequency(self)->dict:
      counter = self._counter
      freq_counter = {} 
      for k,v in counter.items():
           freq_counter.setdefault(v,[]).append(k) 
      for freq in freq_counter:
        freq_counter[freq].sort()
      return dict(sorted(freq_counter.items(),reverse=True))

    def analyze(self):
       mf = self.most_frequent_word()
       return {'word_count':self.word_count(),
                'most_frequent_word':mf['most_frequent_word'],
                'most_frequent_count':mf['most_frequent_count'],
                'first_non_repeat':self.first_non_repeat(),
                'grouped_frequency':self.group_by_frequency()}

class AdvancedTextAnalyzer(TextAnalyzer):
   def has_words(self)->bool:
      return len(self._word_list)>0
   def unique_words(self)->list:
      if not self.has_words():
         return []      
      return sorted(set(self._word_list))
   def longest_word(self)->str|None:
      if not self.has_words():
         return None
      return max(self._word_list,key=len)
   def average_word_length(self)->float:
      if not self.has_words():
        return 0.0
      return float(np.mean(self.word_lengths))
   def word_length_stats(self)->dict:
      if not self.has_words():
         return {'minimum_word_length':0.0,
         'maximum_word_length':0.0,
         'mean_word_length':0.0,
         'std_word_length':0.0}
      lengths = self.word_lengths
      return {
         'minimum_word_length':float(np.min(lengths)),
         'maximum_word_length':float(np.max(lengths)),
         'mean_word_length':self.average_word_length(),
         'std_word_length':float(np.std(lengths))
      }
   def text_feature_vector(self)->dict:
       stats = self.word_length_stats()
       return {
          'word_count':self.word_count(),
          'average_word_length':self.average_word_length(),
          'unique_word_count':len(self.unique_words()),
          'std_word_length':stats['std_word_length']
       }
   
class BulkTextAnalyzer:
   _embedder = None
   def __init__(self,stream:list[str]):
      self.stream = stream
      if BulkTextAnalyzer._embedder is None:
         BulkTextAnalyzer._embedder = SentenceTransformer("all-MiniLM-L6-v2") 
      self.embedder = BulkTextAnalyzer._embedder
   
   def analyze(self,mode:str="features")->pd.DataFrame:
     valid_sentences = [s for s in self.stream if isinstance(s,str)]
     if mode == 'embeddings':
        embeddings = self.embedder.encode(valid_sentences) 
        df = pd.DataFrame(embeddings) 
        df.insert(0,"sentence",valid_sentences) 
        return df 
     elif mode=='features': 
         d_arr = []
         for sen in self.stream:
            analyzer = AdvancedTextAnalyzer(sen)

            if not isinstance(sen, str) or not analyzer.has_words():
               d_arr.append({
                'sentence': sen,
                'word_count': 0,
                'average_word_length': 0,
                'unique_word_count': 0,
                'std_word_length': 0
            })
            else:
              d_arr.append(
                {'sentence': sen} | analyzer.text_feature_vector()
            )
         df = pd.DataFrame(d_arr)
         return df
     else:
        raise ValueError(f'Invalid value for mode:{mode} it should be either features or embeddings')
        

        
      
      
