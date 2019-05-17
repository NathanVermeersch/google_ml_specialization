from __future__ import absolute_import

import argparse
import logging
import json

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

import sys




def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        help='Output file to write results to.')

    known_args, pipeline_args = parser.parse_known_args(argv)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    p = beam.Pipeline(options=pipeline_options)

    parser.add_argument('--project',
                        dest='project',
                        required=True,
                        help='Project ID')

    known_args, _ = parser.parse_known_args(argv)

    PROJECT_ID = known_args.project

    table_spec = '{}:blackfriday.full_dataset'.format(PROJECT_ID)

    def sum_purchase(x):
        user, purchases = x
        d = user
        d.update({'VIP_Purchase': int(sum(purchases) > 100000)})
        return d

    # Read the text file[pattern] into a PCollection.
    input = (p
             | 'ReadTable' >> beam.io.Read(beam.io.BigQuerySource(table_spec))
             | 'Format' >> beam.Map(lambda x: ({'User_ID': x['User_ID'],'Gender': x['Gender'], 'Age': x['Age'], 'Occupation': x['Occupation'],
                           'City_Category': x['City_Category'], 'Stay_In_Current_City_Years': x['Stay_In_Current_City_Years'], 'Marital_Status': x['Marital_Status']}, x['Purchase']))
             | 'Group' >> beam.GroupByKey()
             | 'Sum' >> beam.Map(sum_purchase))

    # Write the output using a "Write" transform that has side effects.
    # pylint: disable=expression-not-assigned
    input | 'write' >> WriteToText(known_args.output, file_name_suffix=".json", shard_name_template='')

    table_spec_output = '{}:blackfriday.processed_full_data'.format(PROJECT_ID)

    table_schema = 'User_ID:INTEGER, Gender:STRING, Age:STRING, Occupation:INTEGER, City_Category:STRING, Stay_In_Current_City_Years:STRING, Marital_Status:INTEGER, VIP_Purchase:INTEGER'

    input | 'write_BQ' >> beam.io.WriteToBigQuery(
        table_spec_output,
        schema=table_schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)

    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
