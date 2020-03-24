import glob
import json
import random


class ErrorAnalyzer:
    def __init__(self, dataset_dir, decoded_dir):
        self.dataset_files = glob.glob(dataset_dir + '/*')
        self.decoded_dir = decoded_dir + '/'

    def get_samples_for_analysis(self):
        count = 0
        samples = []
        for dataset_file in self.dataset_files:
            if random.random() > 0.5:
                continue
            if count > 50:
                break
            data = json.load(open(dataset_file, 'r'))
            article_id = data['id']
            query = data['query']
            expected_summary = data['summary']
            file_name = dataset_file.split('/')[-1].split('.')[0]
            with open(self.decoded_dir + file_name + '.dec', 'r') as decoded_file:
                actual_summaries = decoded_file.readlines()
            samples.append({
                'id': article_id,
                'query': query,
                'target_summary': expected_summary,
                'generated_summary': actual_summaries
            })
            count += 1
        return samples


if __name__ == '__main__':
    analyzer = ErrorAnalyzer('/home/ks3740/cnn-dailymail/tmp_files/val', '/home/ks3740/fast_abs_rl/decoded_files/tmp/output')
    samples = analyzer.get_samples_for_analysis()
    json.dump(samples, open('analysis_2.json', 'w'), indent=4)
