from pyvi import ViTokenizer
import node
import vnstoplist
import re
from math import log2



def preprocess(raw_text):
    raw_text = raw_text.lower()
    raw_text = ViTokenizer.tokenize(raw_text)
    stoplist = vnstoplist.stoplist
    for stopword in stoplist:
        raw_text.replace(stopword, "")
    return ' '.join(re.findall(r"[\w']+", raw_text))

def split_into_sentences(text):
    delimiters = '. ', '! ', '? ', '."', '.”', '…', '.)', '\n', '.\n'
    regexPattern = '|'.join(map(re.escape, delimiters))
    text = re.split(regexPattern, text)
    sentences = []
    for sen in text:
        if len(sen) > 5:
            sentences.append(sen)
    return sentences


def create_graph(sentences):
    n = len(sentences)
    graph = []  # graph array contains sentences

    # convert every sentence to node then push to graph
    for i in range(n):
        node = node.Node(preprocess(sentences[i]).split())
        node.set_index(i)
        graph.append(node)

    # detect connection between sentences
    for ni, node in enumerate(graph):
        for i in range(n):
            if ni != i:  # to not connect with itself
                node.detect_connection(graph[i])

        node.sumup_weight()

    return graph


def rank(graph, iteration=13):
    d = 0.85
    n = len(graph)
    W = [node.get_weight() for node in graph] # stores final score.

    for i in range(iteration): # repeat to converage
        PR = [1-d]*n  # initialize page rank score, set all to 0.15

        for ni, node in enumerate(graph):
            for cni, conn_node in enumerate(node.connected_nodes):   # go through its connected nodes
                PR[ni] = PR[ni] + d * W[cni] / len(conn_node[0].connected_nodes)

        for k in range(n): # update final score after each iteration
            W[k] = PR[k]

    return W


def summarize(text, number_of_sen=5):
    sentences = split_into_sentences(text + " ")

    graph = create_graph([preprocess(sen) for sen in sentences])
    sen_order = list(len(sentences))
    score = rank(graph)

    score, sen_order =  zip(*sorted(zip(score, sen_order)))  # order by score ascending
    sen_order = list(sen_order)
    sen_order = sen_order[(-1)*number_of_sen:]   # take sentences that have high score
    sen_order.sort()  # re-arrange sentence to the order of the original text.

    summ_text = []
    for i in sen_order:
        summ_text.append(sentences[i])

    return ". ".join(summ_text) + "."

