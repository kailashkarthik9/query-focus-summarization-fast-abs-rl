import json

data = json.load(open('analysis/results/with_zero_reward/poor_performers_val_dataset.json'))

data_size = len(data)

print('\n*** Validation Dataset *** : \t\t\t' + str(data_size))

matching_extractions = [key for key, value in data.items() if
                        all([op in value['extractor_output'] for op in value['extractor_targets']])]
print('Matching Targets and Extractions : \t\t' + str(len(matching_extractions)) + '\t' + str(
    round(len(matching_extractions) / data_size, 2)))

matching_extended_extractions = [key for key, value in data.items() if all(
    [op in value['extractor_output'] or op in value['extractor_additional_output'] for op in
     value['extractor_targets']])]
print('Matching Targets and +1 Extractions : \t' + str(len(matching_extended_extractions)) + '\t' + str(
    round(len(matching_extended_extractions) / data_size, 2)))

target_missing_query = [(key,value) for key, value in data.items() if
                        value['query'] not in ' '.join(value['extractor_targets'])]
print('Target missing Query : \t\t\t\t\t' + str(len(target_missing_query)) + '\t' + str(
    round(len(target_missing_query) / data_size, 2)))

from random import sample
sample_ = sample(target_missing_query, 50)

data_dir = '/Users/kailash-karthik/Columbia University/Spring 2020/Summarization/cnn-dailymail/finished_files/val/'

for article_idx, article_data in target_missing_query:
    article = json.load(open(data_dir + str(article_idx) + '.json'))
    article_data['article'] = ' '.join(article['article'])

target_missing_query_with_article_query = [(key, value) for key, value in target_missing_query if value['query'] in value['article']]
print('Target missing Query but in Article : \t' + str(len(target_missing_query_with_article_query)) + '\t' + str(
    round(len(target_missing_query_with_article_query) / len(target_missing_query), 2)))

extraction_missing_query = [key for key, value in data.items() if
                            value['query'] not in ' '.join(value['extractor_output'])]
print('Extraction missing Query : \t\t\t\t' + str(len(extraction_missing_query)) + '\t' + str(
    round(len(extraction_missing_query) / data_size, 2)))

plus_1_extraction_missing_query = [key for key, value in data.items() if
                                   value['query'] not in ' '.join(value['extractor_output']) and value[
                                       'query'] not in ' '.join(
                                       [x for x in value['extractor_additional_output'] if x is not None])]
print('+1 Extraction missing Query : \t\t\t' + str(len(plus_1_extraction_missing_query)) + '\t' + str(
    round(len(plus_1_extraction_missing_query) / data_size, 2)))

both_missing_query = [key for key, value in data.items() if
                      value['query'] not in ' '.join(value['extractor_output']) and value['query'] not in ' '.join(
                          value['extractor_targets']) and value['query'] not in ' '.join(
                          [x for x in value['extractor_additional_output'] if x is not None])]
print('Target and Extraction missing Query : \t' + str(len(both_missing_query)) + '\t' + str(
    round(len(both_missing_query) / data_size, 2)))

target_with_query = {key: value for key, value in data.items() if
                     value['query'] in ' '.join(value['extractor_targets'])}
data_size = len(target_with_query)

print('\n*** Subset with Query in Target *** : \t' + str(len(target_with_query)))

matching_extractions = [key for key, value in target_with_query.items() if
                        all([op in value['extractor_output'] for op in value['extractor_targets']])]
print('Matching Targets and Extractions : \t\t' + str(len(matching_extractions)) + '\t' + str(
    round(len(matching_extractions) / data_size, 2)))

matching_extended_extractions = [key for key, value in target_with_query.items() if all(
    [op in value['extractor_output'] or op in value['extractor_additional_output'] for op in
     value['extractor_targets']])]
print('Matching Targets and +1 Extractions : \t' + str(len(matching_extended_extractions)) + '\t' + str(
    round(len(matching_extended_extractions) / data_size, 2)))

extraction_missing_query = [key for key, value in target_with_query.items() if
                            value['query'] not in ' '.join(value['extractor_output'])]
print('Extraction missing Query : \t\t\t\t' + str(len(extraction_missing_query)) + '\t' + str(
    round(len(extraction_missing_query) / data_size, 2)))

alt_extraction_with_query = [(key, value) for key, value in target_with_query.items() if any(
    [op not in value['extractor_output'] and op not in value['extractor_additional_output'] for op in
     value['extractor_targets']]) and value['query'] in ' '.join(
    value['extractor_output'] + [x for x in value['extractor_additional_output'] if x is not None])]
print('Unmatched Extraction but with Query : \t' + str(len(alt_extraction_with_query)) + '\t' + str(
    round(len(alt_extraction_with_query) / data_size, 2)))

print('ok')
