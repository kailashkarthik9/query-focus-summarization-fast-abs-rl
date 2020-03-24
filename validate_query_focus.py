import glob
import json
import random


class Validator:
    def __init__(self, dataset_dir, dataset_2_dir, decoded_dir, decoded_2_dir):
        self.dataset_files = glob.glob(dataset_dir + '/*')
        self.dataset_2_dir = dataset_2_dir + '/'
        self.decoded_dir = decoded_dir + '/'
        self.decoded_2_dir = decoded_2_dir + '/'

    def get_samples_for_analysis(self):
        count = 0
        samples = []
        for dataset_file in self.dataset_files:
            if random.random() > 0.2:
                continue
            if count > 100:
                break
            file_name = dataset_file.split('/')[-1].split('.')[0]
            data = json.load(open(dataset_file, 'r'))
            data_2 = json.load(open(self.dataset_2_dir + file_name + '.json', 'r'))
            article_id = data['id']
            query = data['query']
            query_2 = data_2['query']
            expected_summary = data['summary']
            expected_summary_2 = data_2['summary']
            with open(self.decoded_dir + file_name + '.dec', 'r') as decoded_file:
                actual_summaries = decoded_file.readlines()
            with open(self.decoded_2_dir + file_name + '.dec', 'r') as decoded_file:
                actual_summaries_2 = decoded_file.readlines()
            samples.append({
                'id': article_id,
                'query_1': query,
                'target_summary_1': expected_summary,
                'generated_summary_1': actual_summaries,
                'query_2': query_2,
                'target_summary_2': expected_summary_2,
                'generated_summary_2': actual_summaries_2
            })
            count += 1
        return samples


class QueryValidator:
    """
    Find the output in the corresponding dataset folder
    """
    def __init__(self, files_dir, map_file):
        self.files_dir = files_dir
        self.map_file = json.load(open(map_file, 'r'))

    def validate_focus(self):
        results = dict()
        for article, summary_files in self.map_file.items():
            article_summaries = list()
            total_summaries = len(summary_files)
            unique_summaries = 0
            for summary_file in summary_files:
                with open(self.files_dir + '/output/' + str(summary_file) + '.dec') as fp:
                    summary_sentences = set([l.strip() for l in fp.readlines()])  # Can replace with list to see if reordering is something that the model learns to do
                    if summary_sentences not in article_summaries:
                        unique_summaries += 1
                        article_summaries.append(summary_sentences)
            results[article] = (unique_summaries, total_summaries, [list(s) for s in article_summaries])
        return results

    @staticmethod
    def aggregate_results(results):
        article_scores = list()
        total_summaries = 0
        unique_summaries = 0
        for article, result in results.items():
            unique_summaries += result[0]
            total_summaries += result[1]
            article_scores.append(result[0] / result[1])
        equal_weight_aggregate = sum(article_scores) / len(article_scores)
        query_weight_aggregate = unique_summaries / total_summaries
        print('Equal Weight Aggregate : ' + str(equal_weight_aggregate))
        print('Query Weight Aggregate : ' + str(query_weight_aggregate))
        results['equal_weight_aggregate'] = equal_weight_aggregate
        results['query_weight_aggregate'] = query_weight_aggregate


if __name__ == '__main__':
    #analyzer = Validator('/home/ks3740/cnn-dailymail/augmented_files/val',
    #                     '/home/ks3740/cnn-dailymail/augmented_files_test_query/val',
    #                     '/home/ks3740/fast_abs_rl/decoded_files/query_focus_comparison/query_1/output',
    #                     '/home/ks3740/fast_abs_rl/decoded_files/query_focus_comparison/query_2/output')
    #samples = analyzer.get_samples_for_analysis()
    #json.dump(samples, open('comparison_multiple_query.json', 'w'), indent=4)
    validator = QueryValidator('/home/ks3740/fast_abs_rl/decoded_files/new_model/single_queries_also'
                               '/query_focus_dataset_with_single_summary',
                               '/home/ks3740/cnn-dailymail/query_focus_dataset_with_single_summary/val_map.json')
    results = validator.validate_focus()
    validator.aggregate_results(results)
    json.dump(results, open('/home/ks3740/fast_abs_rl/decoded_files/new_model/single_queries_also/query_focus_dataset_with_single_summary/query_focus_results.json', 'w'), indent=4)
