import glob
import json
from rouge import Rouge

rouge = Rouge()


class DecodedFilesComparison:
    """
    Find the output in the corresponding dataset folder
    """
    def __init__(self, dataset, decoded_model_1, decoded_model_2):
        self.dataset = glob.glob(dataset + '/*')
        self.decoded_model_1 = decoded_model_1 + '/output/'
        self.decoded_model_2 = decoded_model_2 + '/output/'

    def compare_models(self):
        comparison = dict()
        for data_file in self.dataset:
            file_name = data_file.split('/')[-1].split('.')[0]
            data = json.load(open(data_file))
            query = data['query']
            summary = data['summary']
            with open(self.decoded_model_1 + file_name + '.dec') as model_1_file:
                model_1_decoding = model_1_file.read().splitlines()
            with open(self.decoded_model_2 + file_name + '.dec') as model_2_file:
                model_2_decoding = model_2_file.read().splitlines()
            reference = ' . '.join(summary)
            hypothesis_1 = ' . '.join(model_1_decoding)
            hypothesis_2 = ' . '.join(model_2_decoding)
            score_1 = rouge.get_scores(hypothesis_1, reference)
            score_2 = rouge.get_scores(hypothesis_2, reference)
            comparison[file_name] = {
                'query': query,
                'reference': summary,
                'model_1_summary': model_1_decoding,
                'model_1_score': score_1[0]['rouge-1']['f'],
                'model_2_summary': model_2_decoding,
                'model_2_score': score_2[0]['rouge-1']['f'],
            }
        return comparison


if __name__ == '__main__':
    comparison = DecodedFilesComparison('/home/ks3740/cnn-dailymail/augmented_files/val',
                                        '/home/ks3740/unmodified_fast_abs_rl/fast_abs_rl/decoded_files/query_agnostic',
                                        '/home/ks3740/fast_abs_rl/decoded_files/new_model/single_queries_also'
                                        '/augmented_dataset')
    comparison_results = comparison.compare_models()
    json.dump(comparison_results, open('/home/ks3740/fast_abs_rl/decoded_files/new_model/single_queries_also/augmented_dataset/model_comparison.json', 'w'), indent=4)
