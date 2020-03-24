import json

data = json.load(open('../cnn-dailymail/tmp_files/100.json'))

keyphrases = data['keyphrases']
count = 0
file_map = dict()
for kp in keyphrases:
    data_copy = data.copy()
    del data_copy['keyphrases']
    del data_copy['query']
    del data_copy['summary']
    del data_copy['extracted']
    del data_copy['score']
    data_copy['query'] = kp['keyphrase']
    data_copy['summary'] = kp['highlights']
    file_map[count] = kp['keyphrase']
    json.dump(data_copy, open('../cnn-dailymail/tmp_files/val/' + str(count) + '.json', 'w'), indent=4)
    count += 1
json.dump(file_map, open('../cnn-dailymail/tmp_files/100_file_map.json', 'w'), indent=4)