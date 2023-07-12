from MapReduce import MapReduce


class FindCitations(MapReduce):
    def Map(self, l):  #l: list of dictionaries
        d = dict()
        for i in l:
            node = list(i.values())[0]
            if node not in d:
                d[node] = 1
            else:
                d[node] += 1
        return d
        
    def Reduce(self, l): #l : list of dictionaries 
        d = dict()
        for i in l:
            nodes = list(i.keys())
            for node in nodes:
                if node not in d:
                    d[node] = i[node]
                else:
                    d[node] += i[node]
        return d

        