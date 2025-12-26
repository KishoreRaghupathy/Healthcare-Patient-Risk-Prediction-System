import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import argparse
import logging
import csv
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/raw/patients.csv', help='Input file path')
    parser.add_argument('--output', default='data/processed/training_data', help='Output file path prefix')
    known_args, pipeline_args = parser.parse_known_args()
    return known_args, pipeline_args

class CSVToDict(beam.DoFn):
    """Parses CSV line to dictionary."""
    def process(self, element, header):
        import csv
        reader = csv.DictReader([element], fieldnames=header)
        for row in reader:
            yield row

class PreprocessPatient(beam.DoFn):
    """Feature engineering and cleaning."""
    def process(self, element):
        try:
            # Type conversion
            age = int(element['age'])
            sbp = int(element['systolic_bp'])
            dbp = int(element['diastolic_bp'])
            hr = int(element['heart_rate'])
            spo2 = int(element['spo2'])
            los = int(element['length_of_stay'])
            readmitted = int(element['readmitted'])
            
            # Simple Feature Engineering: Vitals risk score
            vitals_risk = 0
            if sbp > 160 or sbp < 90: vitals_risk += 1
            if hr > 100 or hr < 60: vitals_risk += 1
            if spo2 < 95: vitals_risk += 1
            
            # One-hot encoding for gender (binary)
            # 1 for Male, 0 for Female
            is_male = 1 if element['gender'] == 'Male' else 0
            
            # Simplified one-hot encoding for diagnosis (just top categories or specific ones)
            diagnosis_map = {
                'E11.9': 0, 'I10': 1, 'J44.9': 2, 'I25.10': 3,
                'N18.9': 4, 'F41.9': 5, 'E78.5': 6, 'K21.9': 7
            }
            diagnosis_str = element['primary_diagnosis']
            diagnosis_code = diagnosis_map.get(diagnosis_str, -1)
            
            yield {
                'age': age,
                'is_male': is_male,
                'systolic_bp': sbp,
                'diastolic_bp': dbp,
                'heart_rate': hr,
                'spo2': spo2,
                'vitals_risk': vitals_risk,
                'diagnosis_code': diagnosis_code,
                'length_of_stay': los,
                'readmitted': readmitted
            }
        except Exception as e:
            logging.error(f"Error processing record: {element}, Error: {e}")

class DictToCSV(beam.DoFn):
    """Formats dict to CSV string."""
    def process(self, element):
        # Ensure fixed order
        order = ['age', 'is_male', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'spo2', 'vitals_risk', 'diagnosis_code', 'length_of_stay', 'readmitted']
        yield ','.join([str(element[k]) for k in order])

def get_header(file_path):
    with open(file_path, 'r') as f:
        return f.readline().strip().split(',')

def run(argv=None):
    known_args, pipeline_args = parse_args()
    pipeline_options = PipelineOptions(pipeline_args)
    
    # Read header from file locally to pass to worker
    # In distributed beam, this should be handled differently (e.g. read first line)
    # But for local DirectRunner we can just open the file.
    if not os.path.exists(known_args.input):
        print(f"Input file {known_args.input} not found.")
        return

    csv_header = get_header(known_args.input)

    with beam.Pipeline(options=pipeline_options) as p:
        
        # Read from CSV, skip header
        raw_data = (
            p 
            | 'Read CSV' >> beam.io.ReadFromText(known_args.input, skip_header_lines=1)
            | 'Parse CSV' >> beam.ParDo(CSVToDict(), csv_header)
        )
        
        # Transform
        processed_data = (
            raw_data
            | 'Preprocess' >> beam.ParDo(PreprocessPatient())
        )
        
        # Write to CSV
        (
            processed_data
            | 'Format CSV' >> beam.ParDo(DictToCSV())
            | 'Write Output' >> beam.io.WriteToText(known_args.output, file_name_suffix='.csv', header='age,is_male,systolic_bp,diastolic_bp,heart_rate,spo2,vitals_risk,diagnosis_code,length_of_stay,readmitted')
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
